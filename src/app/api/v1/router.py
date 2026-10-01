from fastapi import APIRouter

from src.app.api.v1.endpoints import users

router = APIRouter()

router.include_router(users.router)
