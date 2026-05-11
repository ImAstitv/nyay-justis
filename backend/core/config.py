from typing import List

from pydantic import ConfigDict, Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "dev-secret"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 8
    ALLOW_LOCAL_BOOTSTRAP: bool = False
    OPENAI_API_KEY: str | None = None
    OPENAI_EXTRACTION_MODEL: str = "gpt-4.1"
    OPENAI_TIMEOUT_SECONDS: int = 90
    ENABLE_MULTILINGUAL_PIPELINE: bool = True
    MULTILINGUAL_TARGET_LANGUAGE: str = "English"
    SUPPORTED_DOCUMENT_LANGUAGES: List[str] = Field(default_factory=lambda: ["English", "Hindi"])
    CORS_ALLOWED_ORIGINS: List[str] = Field(default_factory=list)
    COOKIE_SECURE: bool = True
    COOKIE_SAMESITE: str = "none"
    COOKIE_DOMAIN: str | None = None
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT_SECONDS: int = 30
    DB_POOL_RECYCLE_SECONDS: int = 1800

    @field_validator("CORS_ALLOWED_ORIGINS", "SUPPORTED_DOCUMENT_LANGUAGES", mode="before")
    @classmethod
    def parse_list_values(cls, value):
        if value in (None, "", []):
            return []
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def normalize_database_url(cls, value):
        if isinstance(value, str) and value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql+psycopg2://", 1)
        if isinstance(value, str) and value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg2://", 1)
        return value

    model_config = ConfigDict(env_file=".env")


settings = Settings()
