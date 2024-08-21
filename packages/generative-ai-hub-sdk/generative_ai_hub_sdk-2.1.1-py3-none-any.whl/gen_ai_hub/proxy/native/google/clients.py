import contextvars
from contextlib import contextmanager
from typing import Optional, Sequence, Tuple, cast

import google.api_core.path_template
import google.auth.transport.requests
from google.ai.generativelanguage_v1beta import GenerativeServiceClient
from google.ai.generativelanguage_v1beta.services.generative_service.transports.rest import (
    GenerativeServiceRestInterceptor,
)
from google.ai.generativelanguage_v1beta.types import generative_service
from google.api_core import rest_streaming
from google.api_core.path_template import transcode as transcode_
from google.generativeai import GenerativeModel as GenerativeModel_
from google.generativeai.protos import GenerateContentRequest
from google.oauth2.credentials import Credentials

from gen_ai_hub.proxy.core import get_proxy_client
from gen_ai_hub.proxy.core.base import BaseProxyClient
from gen_ai_hub.proxy.core.utils import if_str_set, kwargs_if_set
from gen_ai_hub.proxy.gen_ai_hub_proxy.client import Deployment
from gen_ai_hub.proxy.native.google.streaming import ServerSentEventsResponseIterator
from gen_ai_hub.proxy.native.google.transport import GenerativeServiceRestTransport

# required for testing framework in llm-commons
_current_deployment = contextvars.ContextVar("current_deployment")


@contextmanager
def set_deployment(value):
    token = _current_deployment.set(value)
    try:
        yield
    finally:
        _current_deployment.reset(token)


def get_current_deployment() -> Deployment:
    return _current_deployment.get(None)


def transcode(http_options, message=None, **request_kwargs):
    """transcode adjusts the original transcode method to remove google
    API specific URL portions in a minimally intrusive way. The function
    is monkey patched into the import hierarchy in the constructor of
    GenerativeModel.
    """
    for http_opt in http_options:
        http_opt["uri"] = http_opt["uri"].replace("/v1beta", "")
    transcoded = transcode_(http_options, message=message, **request_kwargs)
    return transcoded


class GenAIHubGenerativeServiceRestInterceptor(GenerativeServiceRestInterceptor):
    """GenAIHubGenerativeServiceRestInterceptor is responsible for adding
    all headers required by AI Core to the request and replace the auth
    token. The interceptor is triggered on every call.
    """

    def __init__(
        self,
        aicore_proxy_client,
        credentials_reference,
        *args,
        **kwargs,
    ) -> None:
        # AI Core specific header and credentials source.
        self.aicore_proxy_client = aicore_proxy_client
        # Reference to credentials object contained in GenerativeModel._client._transport._session.credentials.
        self.credentials_reference = credentials_reference
        super().__init__(*args, **kwargs)

    def _extend_metadata_with_proxy_headers(
        self, metadata: Sequence[Tuple[str, str]]
    ) -> Sequence[Tuple[str, str]]:
        proxy_header = self.aicore_proxy_client.request_header

        # Move auth token from header to credentials object.
        token = proxy_header["Authorization"].removeprefix("Bearer ")
        self.credentials_reference.token = token
        del proxy_header["Authorization"]

        metadata_extension = [
            (header_key, header_value)
            for header_key, header_value in proxy_header.items()
        ]
        metadata_list = list(metadata)
        metadata_list.extend(metadata_extension)
        metadata = cast(Sequence[Tuple[str, str]], metadata_list)
        return metadata

    def pre_generate_content(
        self, request: GenerateContentRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[GenerateContentRequest, Sequence[Tuple[str, str]]]:
        metadata = self._extend_metadata_with_proxy_headers(metadata)
        return request, metadata

    def pre_stream_generate_content(
        self,
        request: generative_service.GenerateContentRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[generative_service.GenerateContentRequest, Sequence[Tuple[str, str]]]:
        metadata = self._extend_metadata_with_proxy_headers(metadata)
        return request, metadata

    def post_stream_generate_content(
        self, response: rest_streaming.ResponseIterator
    ) -> rest_streaming.ResponseIterator:
        # The AI Core proxy returns the streamed response as server-sent events (SSE) in the format: data: {payload}.
        # This is configured using the alt=sse flag on the Google endpoint.
        # As the Gemini SDK does not inherently support this streaming type, we need to replace the default response
        # iterator with a custom one.
        return ServerSentEventsResponseIterator(
            response._response, generative_service.GenerateContentResponse
        )


class GenerativeModel(GenerativeModel_):
    """Drop-in replacement for google.generativeai.GenerativeModel."""

    def __init__(
        self,
        model: str = "",
        deployment_id: str = "",
        model_name: str = "",
        config_id: str = "",
        config_name: str = "",
        proxy_client: Optional[BaseProxyClient] = None,
        *args,
        **kwargs,
    ):
        # Replaces original transcode import with adjusted transcode function.
        google.api_core.path_template.transcode = transcode

        aicore_proxy_client = proxy_client or get_proxy_client()

        # Gets model_name from either of the supported parameters in the correct order.
        model_name = if_str_set(model_name, if_str_set(model))

        model_identification = kwargs_if_set(
            deployment_id=deployment_id,
            model_name=model_name,
            config_id=config_id,
            config_name=config_name,
        )
        aicore_deployment = aicore_proxy_client.select_deployment(
            **model_identification
        )

        # Credentials token will be replaced on every request by GenAIHubGenerativeServiceRestInterceptor.
        # For this purpose a reference to this object is passed to the interceptor.
        credentials = Credentials(
            token="Placeholder: This token will be replaced by interceptor on every call.",
        )
        with set_deployment(aicore_deployment):
            deployment_url = get_current_deployment().url
            deployment_url = deployment_url.removeprefix("https://")
            deployment_url = deployment_url.removeprefix("http://")
            generativeServiceRestTransport = GenerativeServiceRestTransport(
                host=deployment_url,
                interceptor=GenAIHubGenerativeServiceRestInterceptor(
                    aicore_proxy_client=aicore_proxy_client,
                    credentials_reference=credentials,  # Passes credentials reference to interceptor.
                ),
                credentials=credentials,
            )
            client = GenerativeServiceClient(transport=generativeServiceRestTransport)
            # Replaces client attribute of GenerativeModel object with AI Core specific implementation.
            self._client = client
            super().__init__(*args, model_name=model_name, **kwargs)
            self._client = client
