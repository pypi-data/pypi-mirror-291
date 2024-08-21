import json
from typing import Optional, Sequence, Tuple, List, Dict

from google.ai.generativelanguage_v1beta.services.generative_service.transports.rest import (
    OptionalRetry,
)
from google.ai.generativelanguage_v1beta.types import generative_service
from google.api_core import rest_streaming, gapic_v1, path_template, rest_helpers
from google.ai.generativelanguage_v1beta.services.generative_service.transports import \
    GenerativeServiceRestTransport as GenerativeServiceRestTransport_
from google.protobuf import json_format
from google.api_core import exceptions as core_exceptions


class GenerativeServiceRestTransport(GenerativeServiceRestTransport_):
    # The original implementation of _StreamGenerateContent is missing the stream=True parameter in the call to the
    # proxy. This is necessary to enable streaming responses from the API.
    class _StreamGenerateContent(GenerativeServiceRestTransport_._StreamGenerateContent):

        def __call__(
                self,
                request: generative_service.GenerateContentRequest,
                *,
                retry: OptionalRetry = gapic_v1.method.DEFAULT,
                timeout: Optional[float] = None,
                metadata: Sequence[Tuple[str, str]] = (),
        ) -> rest_streaming.ResponseIterator:
            r"""Call the stream generate content method over HTTP.

            Args:
                request (~.generative_service.GenerateContentRequest):
                    The request object. Request to generate a completion from
                the model.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.generative_service.GenerateContentResponse:
                    Response from the model supporting multiple candidates.

                Note on safety ratings and content filtering. They are
                reported for both prompt in
                ``GenerateContentResponse.prompt_feedback`` and for each
                candidate in ``finish_reason`` and in
                ``safety_ratings``. The API contract is that:

                -  either all requested candidates are returned or no
                   candidates at all
                -  no candidates are returned only if there was
                   something wrong with the prompt (see
                   ``prompt_feedback``)
                -  feedback on each candidate is reported on
                   ``finish_reason`` and ``safety_ratings``.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1beta/{model=models/*}:streamGenerateContent",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_stream_generate_content(
                request, metadata
            )
            pb_request = generative_service.GenerateContentRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                stream=True
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = rest_streaming.ResponseIterator(
                response, generative_service.GenerateContentResponse
            )
            resp = self._interceptor.post_stream_generate_content(resp)
            return resp
