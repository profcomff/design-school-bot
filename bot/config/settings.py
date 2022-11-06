from pydantic import BaseSettings, RedisDsn, AnyHttpUrl
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    TOKEN: str
    BACKEND_URL: AnyHttpUrl = 'https://designschool.api.test.profcomff.com'
    BACKEND_USER: str = 'admin'
    BACKEND_PASSWORD: str = '42'
    SPAM_MODE: str = 'spam'
    REGISTRY_MODE: str = 'registry'
    WORKFLOW_MODE: str = 'workflow'
    SUMMARY_MODE: str = 'summary'
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
