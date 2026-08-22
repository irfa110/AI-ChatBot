import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str

    langsmith_api_key: str | None = None
    langsmith_tracing: bool = True
    langsmith_project: str = "ai-chatbot"

    redis_host: str = "localhost"
    redis_port: int = 6380

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

if settings.langsmith_api_key:
    os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key

os.environ["LANGSMITH_TRACING"] = str(
    settings.langsmith_tracing
).lower()

os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project