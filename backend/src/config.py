from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Todo AI Chatbot"
    DATABASE_URL: str
    COHERE_API_KEY: str  # Required for AI Agent
    # OPENAI_AGENT_API_KEY: Optional[str] = None # In case agents sdk needs its own key, though we use Cohere map

    class Config:
        env_file = ".env"
        extra = "ignore" # Ignore other env vars

@lru_cache()
def get_settings():
    return Settings()
