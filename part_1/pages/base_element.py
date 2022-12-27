from pages.base import BaseLocatorHolder, BaseDriverHolder
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable


class BaseElementWrapper(BaseLocatorHolder):
    def __init__(self, locator_or_element, driver, parent):
        super().__init__(driver)
        if isinstance(locator_or_element, WebElement):
            self._element = locator_or_element
            self._locator = None, None
        else:
            self._element = None
            self._locator = locator_or_element
        self._parent = parent
        self.default_wrapper_class = BaseElementWrapper

    @property
    def element(self):
        if not self._element:
            element = self._parent.find_element(*self._locator)
            self._element = element
        return self._element

    def find_element(self, *args):
        self.wait(10).until(presence_of_element_located(args))
        return self.element.find_element(*args)

    def find_elements(self, *args):
        return self.element.find_elements(*args)

    def exists(self, timeout=0):
        if self._element and self._locator == (None, None):
            try:
                self._element.is_displayed()
                return True
            except StaleElementReferenceException:
                return False

        def _exists(driver):
            return len(self._parent.find_elements(*self._locator)) > 0

        if timeout != 0:
            try:
                self.wait(timeout).until(_exists)
                return True
            except TimeoutException:
                return False

        return _exists(None)

    def click(self):
        self.scroll_into_view()
        self.wait(5).until(element_to_be_clickable(self.element))
        self.element.click()

    @property
    def text(self):
        return self.element.text

    def send_keys(self, *args):
        self.scroll_into_view()
        self.element.click()
        self.element.send_keys(*args)

    def scroll_into_view(self):
        super().scroll_into_view(self.element)


class BaseElementList(BaseDriverHolder):
    _element_class = BaseElementWrapper

    def __init__(self, items_locator, driver, parent):
        super().__init__(driver)
        self._locator = items_locator
        self._parent = parent

    @property
    def _elements(self):
        return [self._element_class(element, self.driver, self._parent) for element in
                self._parent.find_elements(*self._locator)]

    def __getitem__(self, item):
        return self._elements[item]

    def __len__(self):
        return len(self._elements)
