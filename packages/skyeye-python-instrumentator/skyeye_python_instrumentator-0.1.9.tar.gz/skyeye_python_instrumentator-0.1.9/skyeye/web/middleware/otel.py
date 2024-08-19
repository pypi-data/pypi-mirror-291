# hotel.py
from opentelemetry import trace
from opentelemetry import metrics
from common.constants import *
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

tracer = trace.get_tracer("skyeye.web.server.tracer")
meter = metrics.get_meter("skyeye.web.server.meter")

qps_counter = meter.create_counter(
    WEB_SERVER_QPS,
    description="web.server.qps",
)

latency_histogram = meter.create_histogram(
    WEB_SERVER_LATENCY,
    description="web.server.latency",
)
# get service.name

service_name = "unknown_service"
if SERVICE_NAME in Resource.attributes:
    service_name = Resource.attributes[SERVICE_NAME]


async def metrics_function(reqPath: str, status_code: int):
    qps_counter.add(1, {METRICS_ATTR_RET_CODE: status_code, METRICS_ATTR_APPLICATION_NAME: service_name,
                        METRICS_ATTR_CALLEE_ENDPOINT: reqPath})
    latency_histogram.record(1, {METRICS_ATTR_RET_CODE: status_code, METRICS_ATTR_APPLICATION_NAME: service_name,
                                 METRICS_ATTR_CALLEE_ENDPOINT: reqPath})
