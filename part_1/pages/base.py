from selenium.webdriver.support.wait import WebDriverWait


class BaseDriverHolder:
    def __init__(self, driver):
        self._driver = driver

    @property
    def driver(self):
        return self._driver

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def wait(self, timeout=5):
        return WebDriverWait(self.driver, timeout)


class BaseLocatorHolder(BaseDriverHolder):
    _locators = {}

    def get_element_wrapper(self, name):
        locator = self._locators.get(name)

        if not locator:
            raise ValueError(name)

        if len(locator) == 3:
            element_class, locator_by, locator_value = locator
            return element_class((locator_by, locator_value), self.driver, self)
        else:
            return self.default_wrapper_class(locator, self.driver, self)

    def __getattr__(self, item):
        try:
            return self.get_element_wrapper(item)
        except ValueError:
            raise AttributeError(item)
