from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    TOKEN: str
    BACKEND_URL: str
    SPAM_MODE: str
    REGISTRY_MODE: str
    WORKFLOW_MODE: str
    SUMMARY_MODE: str
    CURRENT_MODE: str = "Not stated"

    class Config:
        """Pydantic BaseSettings config"""

        case_sensitive = True
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
