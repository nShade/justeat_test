from selenium.webdriver.support.wait import WebDriverWait


class WaitChange:
    def __init__(self, func, timeout=10):
        self._func = func
        self._timeout = timeout
        self._initial_value = func()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        WebDriverWait(None, self._timeout).until(lambda driver: self._func() != self._initial_value)
