from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()
