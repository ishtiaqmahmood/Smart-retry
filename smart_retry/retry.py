# decorator + wrapper API

import functools
from typing import Any, Callable, Optional, Tuple, Type, Union

from .core import RetryEngine
from .utils import is_async_callable


def retry(
    max_attempts: int = 3,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = (Exception,),
    backoff: Callable[[int], float] = None,
    on_retry: Optional[Callable[[Exception, int], None]] = None,
    on_success: Optional[Callable[[Any], None]] = None,
    on_fail: Optional[Callable[[Exception], None]] = None,
):
    """
    Decorator to retry a function or coroutine.
    """
    # Initialize engine with provided arguments
    kwargs = {
        "max_attempts": max_attempts,
        "exceptions": exceptions,
        "on_retry": on_retry,
        "on_success": on_success,
        "on_fail": on_fail,
    }
    if backoff:
        kwargs["backoff"] = backoff

    engine = RetryEngine(**kwargs)

    def decorator(func: Callable):
        if is_async_callable(func):

            @functools.wraps(func)
            async def wrapper(*args, **kwargs2):
                return await engine.run_async(func, *args, **kwargs2)

            return wrapper

        @functools.wraps(func)
        def wrapper(*args, **kwargs2):
            return engine.run_sync(func, *args, **kwargs2)

        return wrapper

    return decorator
