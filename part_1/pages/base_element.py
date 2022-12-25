from pages.base import Base


class BaseElement(Base):
    _locators = {}

    def __init__(self, locator_by, locator_value, parent=None):
        self._locator = locator_by, locator_value
        self._element = None
        self._parent = parent

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

        raise AttributeError(item)

    def scroll_into_view(self):
        self._element.parent.execute_script("arguments[0].scrollIntoView();", self._element)


class BaseListElement(BaseElement):
    _locators = {}

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
