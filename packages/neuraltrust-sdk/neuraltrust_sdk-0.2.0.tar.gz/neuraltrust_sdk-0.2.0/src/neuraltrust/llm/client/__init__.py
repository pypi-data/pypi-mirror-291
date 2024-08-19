from .base import ChatMessage, LLMClient
from .logger import LLMLogger
from ...utils.config import ConfigHelper

_default_client = None

def set_default_client(client: LLMClient):
    global _default_client
    _default_client = client


def get_default_client() -> LLMClient:
    global _default_client

    if _default_client is not None:
        return _default_client

    from .openai import OpenAIClient

    default_llm_api = ConfigHelper.load_llm_provider()
    default_llm_judge_model = ConfigHelper.load_llm_judge_model()

    try:
        from openai import AzureOpenAI, OpenAI

        client = AzureOpenAI() if default_llm_api == "azure" else OpenAI()

        _default_client = OpenAIClient(model=default_llm_judge_model, client=client)
    except ImportError:
        raise ValueError(f"LLM scan using {default_llm_api.name} require openai>=1.0.0")

    return _default_client


__all__ = [
    "LLMClient",
    "ChatMessage",
    "LLMLogger",
    "get_default_client",
    "set_default_client",
]
