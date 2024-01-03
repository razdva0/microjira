from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    debug: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


CONFIG = Settings()
