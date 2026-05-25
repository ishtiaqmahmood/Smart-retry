# smart_retry/retry.py

import asyncio
import functools
import time
from .exceptions import RetryError


def retry(
    max_attempts=3,
    exceptions=(Exception,),
    backoff=lambda x: 1,
    on_retry=None,
    on_success=None,
    on_fail=None,
):
    def decorator(func):

        # -------------------------
        # ASYNC WRAPPER
        # -------------------------
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                last_error = None

                for attempt in range(1, max_attempts + 1):
                    try:
                        result = await func(*args, **kwargs)

                        if on_success:
                            on_success(result)

                        return result

                    # IMPORTANT FIX: only catch allowed exceptions
                    except exceptions as e:
                        last_error = e

                        if attempt < max_attempts and on_retry:
                            on_retry(e, attempt)

                        if attempt < max_attempts:
                            await asyncio.sleep(backoff(attempt))

                if on_fail:
                    on_fail(last_error)

                raise RetryError(max_attempts, last_error)

            return wrapper

        # -------------------------
        # SYNC WRAPPER
        # -------------------------
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)

                    if on_success:
                        on_success(result)

                    return result

                # IMPORTANT FIX: only catch allowed exceptions
                except exceptions as e:
                    last_error = e

                    if attempt < max_attempts and on_retry:
                        on_retry(e, attempt)

                    if attempt < max_attempts:
                        time.sleep(backoff(attempt))

            if on_fail:
                on_fail(last_error)

            raise RetryError(max_attempts, last_error)

        return wrapper

    return decorator