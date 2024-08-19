# hotel.py
import os
from opentelemetry import trace
from opentelemetry import metrics
from common.constants import *

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
service_name = "no_service"
tracer_provider = trace.get_tracer_provider()
skyeye_resource = tracer_provider.resource

service_name = skyeye_resource.attributes['service.name']

# 从环境变量中获取服务名
# otel_resource_attributes = os.getenv('OTEL_RESOURCE_ATTRIBUTES')
#
# if otel_resource_attributes:
#     # 按逗号分割属性字符串，然后遍历每个属性
#     for attr in otel_resource_attributes.split(','):
#         # 分割键和值
#         key, value = attr.strip().split('=', 1)
#         if key == 'service.name':
#             service_name = value


async def metrics_function(reqPath: str, status_code: int):
    qps_counter.add(1, {METRICS_ATTR_RET_CODE: status_code, METRICS_ATTR_APPLICATION_NAME: service_name,
                        METRICS_ATTR_CALLEE_ENDPOINT: reqPath})
    latency_histogram.record(1, {METRICS_ATTR_RET_CODE: status_code, METRICS_ATTR_APPLICATION_NAME: service_name,
                                 METRICS_ATTR_CALLEE_ENDPOINT: reqPath})
