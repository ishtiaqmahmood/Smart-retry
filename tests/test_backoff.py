from smart_retry.backoff import exponential_backoff, fixed_backoff, linear_backoff

def test_fixed_backoff():
    assert fixed_backoff(1, delay=2) == 2
    assert fixed_backoff(5, delay=2) == 2

def test_linear_backoff():
    assert linear_backoff(1, base=1) == 1
    assert linear_backoff(5, base=1) == 5
    assert linear_backoff(3, base=2) == 6

def test_exponential_backoff():
    # Test without jitter for predictability
    assert exponential_backoff(1, base=1, factor=2, jitter=0) == 1
    assert exponential_backoff(2, base=1, factor=2, jitter=0) == 2
    assert exponential_backoff(3, base=1, factor=2, jitter=0) == 4

    # Test max_delay
    assert exponential_backoff(10, base=1, factor=2, max_delay=10, jitter=0) == 10
