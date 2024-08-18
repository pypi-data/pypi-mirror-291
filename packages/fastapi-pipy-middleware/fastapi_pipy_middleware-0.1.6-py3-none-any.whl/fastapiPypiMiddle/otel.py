# otel.py
import os
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

# 获取环境变量OTEL_RESOURCE_ATTRIBUTES的值
otel_resource_attributes = os.getenv('OTEL_RESOURCE_ATTRIBUTES')

service_name = ""


if otel_resource_attributes:
    # 创建一个字典来存储解析后的属性
    attributes_dict = {}
    # 按逗号分割属性字符串，然后遍历每个属性
    for attr in otel_resource_attributes.split(','):
        # 分割键和值
        key, value = attr.strip().split('=', 1)
        attributes_dict[key] = value

        # 从字典中获取service.name的值
    service_name = attributes_dict.get('service.name')


async def metrics_function(reqPath: str, status_code: int):
    roll_counter.add(1, {METRICS_ATTR_RET_CODE: status_code,METRICS_ATTR_APPLICATION_NAME: service_name,METRICS_ATTR_CALLEE_ENDPOINT: reqPath})
    roll_histogram.record(1, {METRICS_ATTR_RET_CODE: status_code, METRICS_ATTR_APPLICATION_NAME: service_name, METRICS_ATTR_CALLEE_ENDPOINT: reqPath})
    return {"message": "This is from test.py"}