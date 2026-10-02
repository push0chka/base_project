from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.core.shared.metrics.prometheus import PrometheusHttpMetrics

router = APIRouter(route_class=DishkaRoute)


@router.get("/metrics", include_in_schema=False)
async def get_metrics(metrics: FromDishka[PrometheusHttpMetrics]) -> Response:
    return Response(
        content=generate_latest(metrics.registry),
        media_type=CONTENT_TYPE_LATEST,
    )
