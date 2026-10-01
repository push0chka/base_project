from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram

HTTP_DURATION_BUCKETS = (
    0.005,
    0.01,
    0.025,
    0.05,
    0.1,
    0.25,
    0.5,
    1.0,
    2.5,
    5.0,
    10.0,
)


class PrometheusHttpMetrics:
    def __init__(self, namespace: str = "app") -> None:
        self.registry = CollectorRegistry()

        self._requests = Counter(
            name="http_requests_total",
            documentation="Total number of HTTP requests",
            labelnames=("method", "route", "status_code"),
            namespace=namespace,
            registry=self.registry,
        )

        self._request_duration = Histogram(
            name="http_request_duration_seconds",
            documentation="HTTP request duration in seconds",
            labelnames=("method", "route"),
            namespace=namespace,
            buckets=HTTP_DURATION_BUCKETS,
            registry=self.registry,
        )

        self._requests_in_progress = Gauge(
            name="http_requests_in_progress",
            documentation="Number of HTTP requests currently being processed",
            labelnames=("method",),
            namespace=namespace,
            registry=self.registry,
        )

    def request_started(self, method: str) -> None:
        self._requests_in_progress.labels(method=method).inc()

    def request_finished(
        self, *, method: str, route: str, status_code: int, duration: float
    ) -> None:
        self._requests_in_progress.labels(method=method).dec()

        self._requests.labels(
            method=method, route=route, status_code=str(status_code)
        ).inc()

        self._request_duration.labels(method=method, route=route).observe(
            duration
        )
