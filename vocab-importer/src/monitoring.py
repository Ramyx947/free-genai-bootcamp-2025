import time

from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "vocab_importer_requests_total",
    "Total requests processed",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "vocab_importer_request_latency_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
)


class MetricsMiddleware:
    async def __call__(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method, endpoint=request.url.path
        ).observe(time.time() - start_time)

        return response
