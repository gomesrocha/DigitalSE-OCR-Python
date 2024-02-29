import logging
from functools import lru_cache
from pydantic_settings import BaseSettings  # Alteração aqui


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = False
    RABBITMQ_URL: str = ""
    DB_URL: str = ""
    MINIO_URL: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "digitalse
    MINIO_SECRET_KEY: str = "digitalse
    MINIO_SECURE: bool = False
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
