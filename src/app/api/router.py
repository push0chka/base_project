from fastapi import APIRouter

from src.app.api.system.router import router as system_router
from src.app.api.v1.router import router as v1_router

router = APIRouter()

router.include_router(system_router)
router.include_router(v1_router, prefix="/api/v1")
