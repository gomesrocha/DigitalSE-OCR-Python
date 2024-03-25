import logging
from functools import lru_cache

from pydantic_settings import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = False
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672"
    MINIO_URL: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "digitalse"
    MINIO_SECRET_KEY: str = "digitalse"
    MINIO_SECURE: bool = False
    MINIO_BUCKET: str = "images"
    SECRET_KEY: str = "digitalse"
    MONGODB_URL: str = "mongodb://mongo:27017/"
    MONGODB_DB: str = "document_db"
    MONGODB_COLLECTION: str = "documents"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()


settings = get_settings()