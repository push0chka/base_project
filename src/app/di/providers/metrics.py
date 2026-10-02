from dishka import Provider, Scope, alias, provide

from src.core.shared.metrics import HttpMetrics
from src.core.shared.metrics.prometheus import PrometheusHttpMetrics


class MetricsProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_prometheus_metrics(self) -> PrometheusHttpMetrics:
        return PrometheusHttpMetrics(namespace="app")

    http_metrics = alias(source=PrometheusHttpMetrics, provides=HttpMetrics)
