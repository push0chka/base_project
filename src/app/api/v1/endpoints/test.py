from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute

router = APIRouter(tags=["test"], route_class=DishkaRoute)


@router.get("/ping")
async def ping_pong() -> str:
    return "pong"
