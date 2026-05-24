# helper functions for the library

import asyncio

def is_async_callable(func):
    """
    Returns True if the given function is an asynchronous callable.
    Handles both coroutine functions and objects with an async __call__.
    """
    if asyncio.iscoroutinefunction(func):
        return True

    # Handle classes/instances with async __call__
    if hasattr(func, "__call__") and asyncio.iscoroutinefunction(func.__call__):
        return True

    return False
