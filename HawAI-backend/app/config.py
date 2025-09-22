from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "HawAI API"
    MONGO_URL: str = "mongodb://localhost:27017"
    MONGO_DB: str = "hawai"

    JWT_SECRET: str = "change-me"
    JWT_ALG: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7

    CORS_ORIGINS: str = "http://localhost:5173"

    OAI_BASE_URL: str = "http://localhost:11434/v1"
    OAI_MODEL: str = "llava:7b"

    class Config:
        env_file = ".env"


settings = Settings()


