"Decorators used throughout the package"

import time
from functools import wraps


def retry_decorator(*exception_types, max_attempts=3, wait_seconds=2):
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
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except tuple(exception_types) as e:  # Using the tuple of exceptions directly
                    attempts += 1
                    if attempts >= max_attempts:
                        raise
                    print(f"Retrying... Attempt {attempts}/{max_attempts} failed due to {e}")
                    time.sleep(wait_seconds)
        return wrapper
    return decorator
