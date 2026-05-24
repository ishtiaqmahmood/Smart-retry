# delay strategies

import random

def exponential_backoff(attempt: int, base=0.5, factor=2, max_delay=10, jitter=0.2):
    delay = min(base * (factor ** (attempt - 1)), max_delay)
    return delay + random.uniform(0, delay * jitter)


def fixed_backoff(attempt: int, delay=1):
    return delay


def linear_backoff(attempt: int, base=1):
    return base * attempt