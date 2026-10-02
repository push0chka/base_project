from fastapi import APIRouter

from src.app.api.v1.endpoints import users, test

router = APIRouter()

router.include_router(test.router)
router.include_router(users.router)
