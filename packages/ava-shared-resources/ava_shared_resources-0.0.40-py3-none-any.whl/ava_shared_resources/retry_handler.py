"""Retry Handler.

Script contains uniform format for retrying a function with given delay.
"""

import asyncio
import logging
import time

log = logging.getLogger(__name__)


# ToDo: current implementation retries for all Exceptions. In future we can update the logic
#  to retry for only specific Exception types if needed.
def retry(min_delay, max_delay, delay_step, custom_exception: Exception = Exception):
    """Retries the function with given delay using blocking sleep.

    Setting min_delay, max_delay, delay_step to zero disables the retries.
    :param min_delay: minimum delay in seconds
    :param max_delay: maximum delay in seconds
    :param delay_step: the increment in delay between two retries in seconds
    """

    def function_for_try(func):
        """Retries the function with provided delay.

        :param func: function for retry
        """

        def f(*args):
            exception_msg = ""
            delay = min_delay
            while True:
                try:
                    return func(*args)
                except Exception as e:
                    exception_msg = e
                    if delay >= max_delay:
                        break
                    log.warning(
                        f"Processing {func.__name__} failed with message:{e}. "
                        f"will try again after {delay}sec..."
                    )
                    time.sleep(delay)
                    delay += delay_step

            raise custom_exception(
                f"Processing function '{func.__name__}' failed with message:{exception_msg}."
            )

        return f

    return function_for_try


async def async_retry(args, func, min_delay, max_delay, delay_step):
    """Retries the function with provided delay using non-blocking sleep.

    Setting min_delay, max_delay, delay_step to zero disables the retries.
    :param args: arguments to be passed to the function
    :param func: name of the function to be called
    :param min_delay: minimum delay in seconds
    :param max_delay: maximum delay in seconds
    :param delay_step: the increment in delay between two retries in seconds
    """
    exception_msg = ""
    delay = min_delay
    while True:
        try:
            return func(**args)
        except Exception as e:
            exception_msg = e
            if delay >= max_delay:
                break
            log.warning(
                f"Processing {func.__name__} failed with message:{e}. "
                f"will try again after {delay}sec..."
            )
            await asyncio.sleep(delay)
            delay += delay_step

    raise Exception(
        f"Processing function '{func.__name__}' failed with message:{exception_msg}."
    )
