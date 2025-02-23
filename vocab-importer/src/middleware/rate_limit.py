from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Callable
import time
import asyncio
from ..config import Settings

settings = Settings()

class RateLimiter:
    def __init__(self):
        self.requests = {}
        self.lock = asyncio.Lock()

    async def __call__(
        self, request: Request, call_next: Callable
    ) -> JSONResponse:
        client_ip = request.client.host

        async with self.lock:
            now = time.time()
            if client_ip in self.requests:
                last_time, count = self.requests[client_ip]
                if now - last_time < 60:  # 1 minute window
                    if count >= settings.RATE_LIMIT:
                        raise HTTPException(
                            status_code=429, 
                            detail="Too many requests"
                        )
                    self.requests[client_ip] = (last_time, count + 1)
                else:
                    self.requests[client_ip] = (now, 1)
            else:
                self.requests[client_ip] = (now, 1)

        response = await call_next(request)
        return response 