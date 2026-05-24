import asyncio
import pytest
from smart_retry import retry, RetryError

@pytest.mark.asyncio
async def test_retry_async_success():
    call_count = 0

    @retry(max_attempts=3)
    async def task():
        nonlocal call_count
        call_count += 1
        return "success"

    result = await task()
    assert result == "success"
    assert call_count == 1

@pytest.mark.asyncio
async def test_retry_async_eventual_success():
    call_count = 0

    @retry(max_attempts=3, backoff=lambda x: 0)
    async def task():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("fail")
        return "success"

    result = await task()
    assert result == "success"
    assert call_count == 3

@pytest.mark.asyncio
async def test_retry_async_exhaustion():
    call_count = 0

    @retry(max_attempts=3, backoff=lambda x: 0)
    async def task():
        nonlocal call_count
        call_count += 1
        raise ValueError("always fail")

    with pytest.raises(RetryError) as excinfo:
        await task()

    assert "Retry attempts (3) exhausted" in str(excinfo.value)
    assert call_count == 3

@pytest.mark.asyncio
async def test_retry_async_hooks():
    retries = []

    def on_retry(e, attempt):
        retries.append(attempt)

    @retry(max_attempts=3, on_retry=on_retry, backoff=lambda x: 0)
    async def task():
        raise ValueError("fail")

    with pytest.raises(RetryError):
        await task()

    assert retries == [1, 2]
