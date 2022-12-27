from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.base_element import BaseElementWrapper, BaseElementList


class SearchPanel(BaseElementWrapper):
    _locators = {
        'locations': (BaseElementList, By.XPATH, './/li[@data-qa="location-panel-results-item-element"]')
    }


class MainPage(BasePage):
    _locators = {
        'search_input': (By.XPATH, '//input[@data-qa="location-panel-search-input-address-element"]'),
        'search_panel': (SearchPanel, By.XPATH, '//div[@data-qa="location-panel-search-panel"]'),
    }

    def search_address(self, address):
        self.search_input.send_keys(address)
        self.wait(3).until(lambda driver: len(self.search_panel.locations) > 0)
        self.search_panel.locations[0].click()
