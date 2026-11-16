from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Havencrest Realty API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    DATABASE_URL: str = "sqlite+aiosqlite:///./havencrest.db"
    CORS_ORIGINS: list[str] = ["*"]

settings = Settings()
