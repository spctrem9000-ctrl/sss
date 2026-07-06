from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    API_TITLE: str = "Restaurant Cloud Platform API"
    API_VERSION: str = "1.0.0"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def fix_database_url(cls, v: str) -> str:
        if not v or not isinstance(v, str):
            return v

        # Normalize scheme for psycopg
        if v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql+psycopg://", 1)
        elif v.startswith("postgresql://"):
            v = v.replace("postgresql://", "postgresql+psycopg://", 1)

        # Strip any existing ssl/sslmode query params
        if "postgresql+psycopg://" in v:
            if "?" in v:
                base, params = v.split("?", 1)
                cleaned = "&".join(
                    p for p in params.split("&")
                    if not p.lower().startswith("ssl")
                    and not p.lower().startswith("sslmode")
                )
                v = f"{base}?{cleaned}" if cleaned else base

        return v

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
