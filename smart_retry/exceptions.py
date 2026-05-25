# smart_retry/exceptions.py

class RetryError(Exception):
    def __init__(self, attempts: int, last_error: Exception):
        self.attempts = attempts
        self.last_error = last_error

        message = (
            f"Retry attempts ({attempts}) exhausted. "
            f"Last error: {repr(last_error)}"
        )

        super().__init__(message)

        # Preserve original exception context
        self.__cause__ = last_error