from pages.base_element import BaseElement, BaseElementList
from pages.base import Base


class BasePage(Base):
    _locators = {}

    def __init__(self, driver):
        self._driver = driver

    @property
    def driver(self):
        return self._driver

    def __getattr__(self, item):
        locator = self._locators.get(item)

        if not locator:
            raise AttributeError(item)

        if len(locator) == 3:
            element_class, locator_by, locator_value = locator
            return element_class(locator_by, locator_value, self)
        else:
            locator_by, locator_value = locator
            return BaseElement(locator_by, locator_value, self)

    def open(self, url):
        self.driver.get(url)
