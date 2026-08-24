import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    APP_NAME: str = os.getenv(
        "APP_NAME",
        "Architecture Copilot",
    )

    GROQ_API_KEY: str = os.getenv(
        "GROQ_API_KEY",
        "",
    )

    GROQ_MODEL: str = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-120b",
    )

    GROQ_BASE_URL: str = os.getenv(
        "GROQ_BASE_URL",
        "https://api.groq.com/openai/v1",
    )

    MCP_SERVER_URL: str = os.getenv(
        "MCP_SERVER_URL",
        "http://localhost:8001/mcp",
    )


settings = Settings()
