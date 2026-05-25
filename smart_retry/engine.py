# smart_retry/engine.py
import time
import asyncio
from typing import Callable, Tuple, Optional
from .exceptions import RetryError


class RetryEngine:
    def __init__(self, max_attempts=3, exceptions=(Exception,), backoff=lambda x: 1):
        self.max_attempts = max_attempts
        self.exceptions = exceptions
        self.backoff = backoff

    # ---------------- SYNC ----------------
    def run_sync(self, func, *args, **kwargs):
        last_error = None

        for attempt in range(1, self.max_attempts + 1):
            try:
                return func(*args, **kwargs)

            except self.exceptions as e:
                last_error = e

                if attempt == self.max_attempts:
                    break

                time.sleep(self.backoff(attempt))

        raise RetryError(self.max_attempts, last_error)

    # ---------------- ASYNC ----------------
    async def run_async(self, func, *args, **kwargs):
        last_error = None

        for attempt in range(1, self.max_attempts + 1):
            try:
                return await func(*args, **kwargs)

            except self.exceptions as e:
                last_error = e

                if attempt == self.max_attempts:
                    break

                await asyncio.sleep(self.backoff(attempt))

        raise RetryError(self.max_attempts, last_error)