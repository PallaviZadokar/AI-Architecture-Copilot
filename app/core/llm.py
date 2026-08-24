from agent_framework.openai import OpenAIChatCompletionClient

from app.core.config import settings


def get_chat_client() -> OpenAIChatCompletionClient:

    if not settings.GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not configured. "
            "Add it to your .env file."
        )

    return OpenAIChatCompletionClient(
        model=settings.GROQ_MODEL,
        api_key=settings.GROQ_API_KEY,
        base_url=settings.GROQ_BASE_URL,
    )
