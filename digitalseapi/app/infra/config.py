import logging
from functools import lru_cache
from pydantic_settings import BaseSettings  # Alteração aqui
from minio import Minio
from fastapi import Depends
log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = False
    RABBITMQ_URL: str = ""
    DB_URL: str = ""
    MINIO_URL: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "digitalse"
    MINIO_SECRET_KEY: str = "digitalse"
    MINIO_SECURE: bool = False
    SECRET_KEY: str = "digitalse"
    #ALGORITHM: str = "HS256"
    #ACCESS_TOKEN_EXPIRE_MINUTES: str = 30
    #REFRESH_TOKEN_EXPIRE_MINUTES: str = 600

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()


settings = get_settings()


# Configurações do Minio
def get_minio_client() -> Minio:

    return Minio(settings.MINIO_URL,
                      access_key=settings.MINIO_ACCESS_KEY,
                      secret_key=settings.MINIO_SECRET_KEY,
                      secure=settings.MINIO_SECURE)