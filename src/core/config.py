from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / ".env")
    )


settings = Settings()
