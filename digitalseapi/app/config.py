import logging
from functools import lru_cache
from pydantic_settings import BaseSettings  # Alteração aqui


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = False
    RABBITMQ_URL: str = ""
    DB_URL: str = ""

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
