from motor.motor_asyncio import AsyncIOMotorClient
from sqlmodel import create_engine, SQLModel, Session
from fastapi import Depends
from app.infra.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


ActiveSession = Depends(get_session)


async def get_mongodb_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(settings.MONGODB_URL)
