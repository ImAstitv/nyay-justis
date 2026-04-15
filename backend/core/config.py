from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "dev-secret"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 8
    
    class Config:
        env_file = ".env"

settings = Settings()