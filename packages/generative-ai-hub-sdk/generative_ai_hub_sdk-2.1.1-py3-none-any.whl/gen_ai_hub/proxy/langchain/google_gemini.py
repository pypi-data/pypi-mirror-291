from typing import Dict, Optional

from langchain_google_genai import ChatGoogleGenerativeAI as ChatGoogleGenerativeAI_
from pydantic.v1 import Extra, root_validator

from gen_ai_hub.proxy.core.base import BaseProxyClient
from gen_ai_hub.proxy.core.utils import if_str_set
from gen_ai_hub.proxy.gen_ai_hub_proxy.client import Deployment
from gen_ai_hub.proxy.langchain.init_models import catalog
from gen_ai_hub.proxy.native.google.clients import GenerativeModel


class ChatGoogleGenerativeAI(ChatGoogleGenerativeAI_):
    """Drop-in replacement for langchain_google_genai.ChatGoogleGenerativeAI."""

    def __init__(
        self,
        *args,
        model: str = "",  # model parameter from google library.
        proxy_model_name: str = "",  # model parameter for old versions.
        model_id: str = "",
        deployment_id: str = "",
        model_name: str = "",
        config_id: str = "",
        config_name: str = "",
        proxy_client: Optional[BaseProxyClient] = None,
        **kwargs,
    ):
        # Correct model_id fitting to deployment is selected in validate_environment.
        if model_id != "":
            raise ValueError(
                "Parameter not supported. Please use a variation of deployment_id, model_name, config_id and config_name to identify a deployment."
            )

        # Gets model_name from either of the supported parameters in the correct order.
        model_name = if_str_set(
            model_name, if_str_set(model, if_str_set(proxy_model_name))
        )
        # Remove models/ prefix from model_name in case set due to langchain documentation.
        model_name = model_name.removeprefix("models/")

        client_params = {
            "deployment_id": deployment_id,
            "model_name": model_name,
            "config_id": config_id,
            "config_name": config_name,
            "proxy_client": proxy_client,
        }
        kwargs["client_params"] = client_params

        # Configures pydantic to allow additional attributes.
        setattr(self.Config, "extra", Extra.allow)

        # Models prefix required by langchain implementation. If not set rpc to rest transformation fails due to mapping issue.
        super().__init__(*args, model="models/" + model_name, **kwargs)

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        client_params = values["client_params"]
        if not values.get("client"):
            generative_model = GenerativeModel(**client_params)
            values["client"] = generative_model._client
        return values


@catalog.register(
    "gen-ai-hub",
    ChatGoogleGenerativeAI,
    "gemini-1.0-pro",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
)
def init_chat_model(
    proxy_client: BaseProxyClient,
    deployment: Deployment,
    temperature: float = 0.0,
    max_tokens: int = 256,
    top_k: Optional[int] = None,
    top_p: float = 1.0,
):
    return ChatGoogleGenerativeAI(
        model_name=deployment.model_name,
        deployment_id=deployment.deployment_id,
        proxy_client=proxy_client,
        temperature=temperature,
        max_output_tokens=max_tokens,
        top_k=top_k,
        top_p=top_p,
    )
