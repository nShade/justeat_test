import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import TimeoutException
from pages.base_page import BasePage
from pages.base_element import BaseElement, BaseElementList, BaseListElement

PRICE_PATTERN = re.compile(r'(\d+),(\d+) €')


class OrderValueFilterOptions(BaseElement):
    _locators = {
        'less_10_eur': (By.XPATH, './/input[@value="1000" and @data-qa="radio-element"]/..')
    }


class Restaurant(BaseListElement):
    _locators = {
        '_min_order_value': (By.XPATH, './/div[@data-qa="mov-indicator-content"]/span[@data-qa="text"]'),
        'shipping_time_indicator': (By.XPATH, 'div[@data-qa="shipping-time-indicator"]'),
        '_cuisines': (BaseElementList, By.XPATH, './/div[@data-qa="restaurant-cuisines"]/span[@data-qa="cuisine"]')
    }

    @property
    def min_order_value(self):
        mov_eur, mov_cents = PRICE_PATTERN.match(self._min_order_value.text).groups()
        return int(mov_eur) + int(mov_cents) / 100

    @property
    def cuisines(self):
        return [el.text for el in self._cuisines]


class Restaurants(BaseElementList):
    _element_class = Restaurant

    def scroll_until_loaded(self):
        prev_len = -1
        while len(self) != prev_len:
            prev_len = len(self)
            self[-1].scroll_into_view()
            try:
                WebDriverWait(self.driver, 0.5).until(lambda driver: len(self) > prev_len)
            except TimeoutException:
                pass


class RestaurantsSection(BaseElement):
    _locators = {
        'restaurants': (Restaurants, By.XPATH, './/div[@data-qa="restaurant-card-element"]')
    }


class CuisineFilter(BaseElement):
    _locators = {
        '_cuisines': (BaseElementList, By.XPATH, './/div[@data-qa="swipe-navigation-item"]')
    }

    def get_cuisine(self, name):
        for cuisine in self.cuisines:
            if cuisine.text == name:
                return cuisine

    @property
    def more(self):
        return self.cuisines[-1]

    @property
    def cuisines(self):
        WebDriverWait(self.driver, 10).until(lambda driver: len(self._cuisines) > 0)
        return self._cuisines


class CuisineModal(BaseElement):
    _locators = {
        'search_input': (By.XPATH, './/input[@data-qa="cuisine-search-element"]'),
        'cuisines': (By.XPATH, '//div[@data-qa="cuisine-filter-modal-item-element"]')
    }

    CUISINE_PATTERN = re.compile(r'(.*) (\(\d+\))')

    def get_cuisine(self, name):
        for cuisine in self.cuisines:
            cuisine_name, cuisine_number = self.CUISINE_PATTERN.match(cuisine.text).groups()
            if cuisine_name == name:
                return cuisine


class SearchPage(BasePage):
    _locators = {
        'order_value_filter_options': (
            OrderValueFilterOptions, By.XPATH, '//fieldset[@data-qa="minimum-order-value-filter-options"]'),
        'open_section': (RestaurantsSection, By.XPATH, '//section[@data-qa="restaurant-list-open-section"]'),
        'pre_order_section': (RestaurantsSection, By.XPATH, '//section[@data-qa="restaurant-list-pre-order-section"]'),
        'closed_section': (RestaurantsSection, By.XPATH, '//section[@data-qa="restaurant-list-closed-section"]'),
        'cuisine_filter': (CuisineFilter, By.XPATH, '//div[@data-qa="cuisine-filter"]'),
        'cuisine_modal': (CuisineModal, By.XPATH, '//div[@data-qa="cuisine-filter-modal"]')
    }
