from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait


class Base:
    @property
    def driver(self):
        pass

    def find_element(self, *args):
        WebDriverWait(self.driver, 10).until(presence_of_element_located(args))
        return self.driver.find_element(*args)

    def find_elements(self, *args):
        return self.driver.find_elements(*args)
