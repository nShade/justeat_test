from pages.base import Base


class BaseElement(Base):
    _locators = {}

    def __init__(self, locator_by, locator_value, parent=None):
        self._locator = locator_by, locator_value
        self._element = None
        self._parent = parent
        self._default_element_class = BaseElement

    @property
    def element(self):
        if not self._element:
            element = self._parent.find_element(*self._locator)
            self._element = element
        return self._element

    @property
    def driver(self):
        return self.element

    def exists(self):
        elements = self._parent.find_elements(*self._locator)
        return len(elements) > 0

    def click(self):
        self.element.click()

    @property
    def text(self):
        return self.element.text

    def send_keys(self, *args):
        self.element.send_keys(*args)

    def scroll_into_view(self):
        self._element.parent.execute_script("arguments[0].scrollIntoView();", self._element)


class BaseListElement(BaseElement):
    def __init__(self, element, parent=None):
        super().__init__(None, None, parent)
        self._element = element


class BaseElementList(BaseElement):
    _element_class = BaseListElement

    @property
    def _elements(self):
        return [self._element_class(element, self._parent) for element in self._parent.find_elements(*self._locator)]

    def __getitem__(self, item):
        return self._elements[item]

    def __len__(self):
        return len(self._elements)
