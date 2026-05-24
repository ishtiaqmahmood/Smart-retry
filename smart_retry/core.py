# main retry engine

import asyncio
import time
from .exceptions import RetryError
from .backoff import exponential_backoff
from .config import DEFAULT_MAX_ATTEMPTS


class RetryEngine:
    def __init__(
        self,
        max_attempts=DEFAULT_MAX_ATTEMPTS,
        exceptions=(Exception,),
        backoff=exponential_backoff,
        on_retry=None,
        on_success=None,
        on_fail=None,
    ):
        if not isinstance(max_attempts, int) or max_attempts < 1:
            raise ValueError("max_attempts must be a positive integer")

        self.max_attempts = max_attempts
        self.exceptions = exceptions
        self.backoff = backoff
        self.on_retry = on_retry
        self.on_success = on_success
        self.on_fail = on_fail

    # -------- SYNC --------
    def run_sync(self, func, *args, **kwargs):
        last_err = None

        for attempt in range(1, self.max_attempts + 1):
            try:
                result = func(*args, **kwargs)

                if self.on_success:
                    self.on_success(result)

                return result

            except self.exceptions as e:
                last_err = e

                if attempt < self.max_attempts:
                    if self.on_retry:
                        self.on_retry(e, attempt)

                    time.sleep(self.backoff(attempt))

        if self.on_fail:
            self.on_fail(last_err)

        raise RetryError(f"Retry attempts ({self.max_attempts}) exhausted") from last_err

    # -------- ASYNC --------
    async def run_async(self, func, *args, **kwargs):
        last_err = None

        for attempt in range(1, self.max_attempts + 1):
            try:
                result = await func(*args, **kwargs)

                if self.on_success:
                    self.on_success(result)

                return result

            except self.exceptions as e:
                last_err = e

                if attempt < self.max_attempts:
                    if self.on_retry:
                        self.on_retry(e, attempt)

                    await asyncio.sleep(self.backoff(attempt))

        if self.on_fail:
            self.on_fail(last_err)

        raise RetryError(f"Retry attempts ({self.max_attempts}) exhausted") from last_err
