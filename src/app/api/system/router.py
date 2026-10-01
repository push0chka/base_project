from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute

from src.app.api.system.metrics import router as metrics_router
from src.app.api.system.schemas import SystemInfoResponse

router = APIRouter(tags=["system"], route_class=DishkaRoute)

router.include_router(metrics_router)


@router.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get(
    "/system-info", include_in_schema=False, response_model=SystemInfoResponse
)
async def system_info() -> SystemInfoResponse:
    return SystemInfoResponse()
