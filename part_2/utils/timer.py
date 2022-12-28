import time


class Timer:
    def __init__(self, timeout):
        self._timeout = timeout
        self._started = time.monotonic()

    def is_running(self):
        return time.monotonic() < self._started + self._timeout


def repeat_until(action, validation, timeout=60, poll_frequency=10, error_to_raise=None):
    timer = Timer(timeout)
    result = action()

    while not validation(result) and timer.is_running():
        time.sleep(poll_frequency)
        result = action()

    if not validation(result) and error_to_raise:
        raise error_to_raise

    return result