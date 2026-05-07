from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "dev-secret"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 8
    ALLOW_LOCAL_BOOTSTRAP: bool = False
    OPENAI_API_KEY: str | None = None
    OPENAI_EXTRACTION_MODEL: str = "gpt-4.1"
    OPENAI_TIMEOUT_SECONDS: int = 90
    CORS_ALLOWED_ORIGINS: List[str] = Field(default_factory=list)
    COOKIE_SECURE: bool = True
    COOKIE_SAMESITE: str = "none"
    COOKIE_DOMAIN: str | None = None

    @field_validator("CORS_ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_cors_allowed_origins(cls, value):
        if value in (None, "", []):
            return []
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    class Config:
        env_file = ".env"


settings = Settings()
