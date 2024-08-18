# otel.py
from opentelemetry import trace
from opentelemetry import metrics
from .constants import *


tracer = trace.get_tracer("diceroller.tracer")
meter = metrics.get_meter("diceroller.meter")


roll_counter = meter.create_counter(
    WEB_SERVER_QPS,
    description="counter value",
)


roll_histogram = meter.create_histogram(
    WEB_SERVER_LATENCY,
    description="histogram  value",
)

tracer_provider = trace.get_tracer_provider()
resourceHandle = tracer_provider.resource



async def metrics_function(reqPath: str, status_code: int):
    roll_counter.add(1, {METRICS_ATTR_RET_CODE: status_code,METRICS_ATTR_APPLICATION_NAME: resourceHandle.attributes['service.name'],METRICS_ATTR_CALLEE_ENDPOINT: reqPath})
    roll_histogram.record(1, {METRICS_ATTR_RET_CODE: status_code, METRICS_ATTR_APPLICATION_NAME: resourceHandle.attributes['service.name'], METRICS_ATTR_CALLEE_ENDPOINT: reqPath})
    return {"message": "This is from test.py"}