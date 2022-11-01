from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    TOKEN: str

    class Config:
        """Pydantic BaseSettings config"""

        case_sensitive = True
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
