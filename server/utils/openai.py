from openai import AsyncOpenAI

from agents import (
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)
from config import settings
client = AsyncOpenAI(
        base_url=settings.LITELLM_API_BASE,
        api_key=settings.LITELLM_KEY)


set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)

def get_client():
    return client
