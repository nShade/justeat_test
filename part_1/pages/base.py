from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait


class Base:
    _locators = {}

    @property
    def driver(self):
        pass

    def find_element(self, *args):
        WebDriverWait(self.driver, 10).until(presence_of_element_located(args))
        return self.driver.find_element(*args)

    def find_elements(self, *args):
        return self.driver.find_elements(*args)

    def __getattr__(self, item):
        locator = self._locators.get(item)

        if not locator:
            raise AttributeError(item)

        if len(locator) == 3:
            element_class, locator_by, locator_value = locator
            return element_class(locator_by, locator_value, self)
        else:
            locator_by, locator_value = locator
            return self._default_element_class(locator_by, locator_value, self)
