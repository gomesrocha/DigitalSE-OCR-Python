from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infra.db import init_db

from app.infra.config import get_settings
from app.routers import main_router


app = FastAPI(
    title="DigitalSE",
    version="0.1.0",
    description="Sistema de gestão documental com extração de dados por OCR",
)
allow_origin = ["*"]

settings = get_settings()


app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origin,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.include_router(main_router)


@app.on_event("startup")
def on_startup():
    init_db()
