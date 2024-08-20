"Decorators used throughout the package"

import time
from functools import wraps


def retry_decorator(*exception_types, max_attempts: int = 3, wait_seconds: int = 2):
    """
    A decorator that retries a function if specified exceptions are raised.

    @params:
    - exception_types:
        Variable number of exception classes to catch.
    - max_attempts (int):
        Maximum number of retry attempts.
    - wait_seconds (int):
        Number of seconds to wait between attempts.

    @returns:
    - Decorator function that handles retries.
    """
    if not exception_types:
        raise ValueError("At least one exception type must be specified")

    for exc in exception_types:
        if not issubclass(exc, BaseException):
            raise TypeError(f"{exc} is not an exception type")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            last_exception = None
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except tuple(exception_types) as e:
                    attempts += 1
                    last_exception = e
                    if attempts >= max_attempts:
                        raise
                    print(f"Retrying... Attempt {attempts}/{max_attempts} failed due to {e}")
                    time.sleep(wait_seconds)
            raise last_exception  # Raise the last caught exception if all attempts fail
        return wrapper
    return decorator
