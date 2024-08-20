# fastapi.py
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
from .otel import report_red


class APMReporter(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = (time.perf_counter() - start_time)

        if isinstance(response.status_code, int):
            await report_red(request.url.path, response.status_code, process_time)
        else:
            await report_red(request.url.path, 0, process_time)

        return response
