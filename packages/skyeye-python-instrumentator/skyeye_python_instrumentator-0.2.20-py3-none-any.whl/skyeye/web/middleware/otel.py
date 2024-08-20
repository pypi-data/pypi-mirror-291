# hotel.py
from opentelemetry import trace
from opentelemetry import metrics
from common.constants import *
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
import time  # 导入时间模块，用于测量延迟

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

# get service.name by opentelemetry.sdk.resources
service_name = "unknown_service"
skyeye_resource = Resource.create()
if SERVICE_NAME in skyeye_resource.attributes:
    service_name = skyeye_resource.attributes[SERVICE_NAME]


async def report_red(reqPath: str, status_code: int, latency_in_milliseconds: float):
    qps_counter.add(1, {METRICS_ATTR_RET_CODE: status_code, METRICS_ATTR_APPLICATION_NAME: service_name,
                        METRICS_ATTR_CALLEE_ENDPOINT: reqPath})
    latency_histogram.record(latency_in_milliseconds,
                             {METRICS_ATTR_RET_CODE: status_code, METRICS_ATTR_APPLICATION_NAME: service_name,
                              METRICS_ATTR_CALLEE_ENDPOINT: reqPath})
