from fastapi import APIRouter

from .documents import router as documents_router
from .user import router as user_router
from .auth import router as auth_router

main_router = APIRouter()

main_router.include_router(documents_router,
                           prefix="/documents",
                           tags=["Documents"])

main_router.include_router(user_router,
                           prefix="/users",
                           tags=["Users"])

main_router.include_router(auth_router,
                           prefix="/auth",
                           tags=["Auth"])