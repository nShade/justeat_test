from pages.base_element import BaseElementWrapper, BaseElementList
from pages.base import BaseLocatorHolder
from selenium.webdriver.support.expected_conditions import presence_of_element_located


class BasePage(BaseLocatorHolder):
    _locators = {}

    def __init__(self, driver):
        super().__init__(driver)
        self.default_wrapper_class = BaseElementWrapper

    def find_element(self, *args):
        self.wait(10).until(presence_of_element_located(args))
        return self.driver.find_element(*args)

    def find_elements(self, *args):
        return self.driver.find_elements(*args)
