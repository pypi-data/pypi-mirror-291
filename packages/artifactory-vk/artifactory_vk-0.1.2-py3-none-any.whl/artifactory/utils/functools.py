import functools
import time
from typing import Any, Callable, Tuple


class MaxRetriesReachedError(Exception):
    def __init__(self, last_retry_error: Exception):
        self._last_retry_error = last_retry_error
        super().__init__()
    
    def __str__(self):
        return f'Max retries reached. Last error: `{self.last_retry_error}`'

    @property
    def last_retry_error(self):
        return self._last_retry_error


def retry(
    fn: Callable[[], Tuple[Any, ...]],
    *,
    max_retries: int = 3,
    sleep_time_base_s: int = 1,
    sleep_time_factor: int = 2,
    on_error: Callable[[Exception], None] = lambda err: None,
):
    retry_index = 0
    last_error = None
    for retry_index in range(max_retries+1):
        try:
            return fn()
        except Exception as error:
            on_error(error)
            last_error = error
            time.sleep(sleep_time_base_s * (sleep_time_factor ** retry_index))
    raise MaxRetriesReachedError(last_error)


def apply(*nargs):
    "NOTE: deprecated, use functools.partial instead"
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*nargs, *args, **kwargs)
        return wrapper
    return decorator


def try_while(*, while_=lambda: False, sleep_time_s=60, max_retries=120, max_retries_error_msg=''):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retry_index = 0
            while while_():
                if retry_index >= max_retries:
                    raise RuntimeError('Max retries reached: {}'.format(max_retries_error_msg))
                if retry_index > 0:
                    time.sleep(sleep_time_s)
                func(*args, **kwargs)
                retry_index += 1
        return wrapper
    return decorator


def call_delay(*, seconds=0, minutes=0, hours=0):
    delay_s = seconds + minutes * 60 + hours * 3600
    call_delay.last_call = -1

    def decorator(func):

        def wait_delay():
            now = int(time.time())
            time.sleep(max(call_delay.last_call + delay_s - now, 0))

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait_delay()
            call_delay.last_call = int(time.time())
            return func(*args, **kwargs)

        return wrapper
    return decorator


def max_calls_per_second(count):
    return call_delay(seconds = 1.0 / count)
