from pydantic import BaseSettings, RedisDsn, AnyHttpUrl
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    TOKEN: str
    BACKEND_URL: AnyHttpUrl
    BACKEND_USER: str
    BACKEND_PASSWORD: str
    SPAM_MODE: str
    REGISTRY_MODE: str
    WORKFLOW_MODE: str
    SUMMARY_MODE: str
    CURRENT_MODE: str = "Not stated"
    REDIS_DSN: RedisDsn

    @property
    def auth_headers(self):
        return {
            "accept": "application/json",
            "Authorization": f"Bearer {self.BACKEND_PASSWORD}",
        }

    class Config:
        """Pydantic BaseSettings config"""

        case_sensitive = True
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
