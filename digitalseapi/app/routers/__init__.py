from fastapi import APIRouter

from .documents import router as documents_router

main_router = APIRouter()

main_router.include_router(documents_router, tags=["Documents"])

