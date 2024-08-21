import functools
import time
import logging

logger_timeit = logging.getLogger("gcviz.timeit")


def timeit(func):
    """Decorator to time a function's execution."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.time()
        execution_time = (end_time - start_time) * 1e3
        logger_timeit.info(
            f"Function {func.__name__!r} executed in {execution_time:.2f} ms"
        )
        return result

    return wrapper
