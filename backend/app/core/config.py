from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "智农粮"
    DEBUG: bool = False

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "znl"
    DB_PASSWORD: str = "znl123"
    DB_NAME: str = "znl_db"

    SECRET_KEY: str = "change-this-in-production-znl-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    CORS_ORIGINS: str = "http://127.0.0.1:5173,http://localhost:5173"

    BACKUP_DIR: str = "/data/backup"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    class Config:
        env_file = ".env"


settings = Settings()
