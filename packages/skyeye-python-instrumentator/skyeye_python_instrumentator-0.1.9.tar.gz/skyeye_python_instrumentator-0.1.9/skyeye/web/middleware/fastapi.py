# fastapi.py
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
from .otel import metrics_function

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 设置日志级别

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI()


class APMReporter(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        response.headers["X-Process-Time"] = str(process_time)

        if isinstance(response.status_code, int):
            await metrics_function(request.url.path, response.status_code)
        else:
            await metrics_function(request.url.path, 0)

        return response


@app.get("/skyeye")
async def sky_function1():
    logger.info("log-test")
    return {"skyeye-R.E.D"}
