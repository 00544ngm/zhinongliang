from pydantic_settings import BaseSettings

INSECURE_SECRET_KEYS = {
    "",
    "change-this-in-production-znl-2024",
}


class Settings(BaseSettings):
    APP_NAME: str = "智农粮"
    DEBUG: bool = False

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "znl"
    DB_PASSWORD: str = "znl123"
    DB_NAME: str = "znl_db"

    SECRET_KEY: str = ""
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

    def validate_security(self) -> None:
        if self.SECRET_KEY.strip() in INSECURE_SECRET_KEYS or len(self.SECRET_KEY.strip()) < 32:
            raise RuntimeError("SECRET_KEY must be set in backend/.env and be at least 32 characters long.")

    class Config:
        env_file = ".env"


settings = Settings()
settings.validate_security()
