from pages.base_element import BaseElement, BaseElementList
from pages.base import Base


class BasePage(Base):
    _locators = {}

    def __init__(self, driver):
        self._driver = driver
        self._default_element_class = BaseElement

    @property
    def driver(self):
        return self._driver

    def open(self, url):
        self.driver.get(url)
