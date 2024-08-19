# otel.py
import os
from opentelemetry import metrics
from common.constants import *


meter = metrics.get_meter("diceroller.meter")


roll_counter = meter.create_counter(
    WEB_SERVER_QPS,
    description="counter value",
)


roll_histogram = meter.create_histogram(
    WEB_SERVER_LATENCY,
    description="histogram  value",
)

# 从环境变量中获取服务名
otel_resource_attributes = os.getenv('OTEL_RESOURCE_ATTRIBUTES')

service_name = "no_service"

if otel_resource_attributes:
    # 按逗号分割属性字符串，然后遍历每个属性
    for attr in otel_resource_attributes.split(','):
        # 分割键和值
        key, value = attr.strip().split('=', 1)
        if key == 'service.name':
            service_name = value


async def metrics_function(reqPath: str, status_code: int):
    roll_counter.add(1, {METRICS_ATTR_RET_CODE: status_code,METRICS_ATTR_APPLICATION_NAME:service_name,METRICS_ATTR_CALLEE_ENDPOINT: reqPath})
    roll_histogram.record(1, {METRICS_ATTR_RET_CODE: status_code, METRICS_ATTR_APPLICATION_NAME: service_name, METRICS_ATTR_CALLEE_ENDPOINT: reqPath})
    return {"message": "This is from test.py"}