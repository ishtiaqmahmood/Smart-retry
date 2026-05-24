import pytest
from smart_retry import retry, RetryError

def test_retry_sync_success():
    call_count = 0

    @retry(max_attempts=3)
    def task():
        nonlocal call_count
        call_count += 1
        return "success"

    result = task()
    assert result == "success"
    assert call_count == 1

def test_retry_sync_eventual_success():
    call_count = 0

    @retry(max_attempts=3)
    def task():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("fail")
        return "success"

    # We need to mock backoff to avoid sleeping in tests
    from smart_retry.backoff import fixed_backoff

    @retry(max_attempts=3, backoff=lambda x: 0)
    def task_no_sleep():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("fail")
        return "success"

    result = task_no_sleep()
    assert result == "success"
    assert call_count == 3

def test_retry_sync_exhaustion():
    call_count = 0

    @retry(max_attempts=3, backoff=lambda x: 0)
    def task():
        nonlocal call_count
        call_count += 1
        raise ValueError("always fail")

    with pytest.raises(RetryError) as excinfo:
        task()

    assert "Retry attempts (3) exhausted" in str(excinfo.value)
    assert call_count == 3

def test_retry_sync_specific_exceptions():
    call_count = 0

    @retry(max_attempts=3, exceptions=(ValueError,), backoff=lambda x: 0)
    def task():
        nonlocal call_count
        call_count += 1
        raise TypeError("unexpected")

    with pytest.raises(TypeError):
        task()

    assert call_count == 1
