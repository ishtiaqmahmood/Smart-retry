# custom exceptions

class RetryError(Exception):
    """Raised when retry attempts are exhausted."""
    pass