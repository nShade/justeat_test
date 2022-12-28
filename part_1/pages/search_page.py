import re
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from utils.wait import WaitChange
from pages.base_page import BasePage
from pages.base_element import BaseElementWrapper, BaseElementList

PRICE_PATTERN = re.compile(r'(\d+),(\d+) €')


class OrderValueFilterOptions(BaseElementWrapper):
    _locators = {
        'less_10_eur': (By.XPATH, './/input[@value="1000" and @data-qa="radio-element"]/..'),
        'less_15_eur': (By.XPATH, './/input[@value="1500" and @data-qa="radio-element"]/..')
    }


class Restaurant(BaseElementWrapper):
    _locators = {
        '_name': (By.XPATH, './/h3[@data-qa="restaurant-info-name"]'),
        '_min_order_value': (By.XPATH, './/div[@data-qa="mov-indicator-content"]/span[@data-qa="text"]'),
        'shipping_time_indicator': (By.XPATH, 'div[@data-qa="shipping-time-indicator"]'),
        '_cuisines': (BaseElementList, By.XPATH, './/div[@data-qa="restaurant-cuisines"]/span[@data-qa="cuisine"]'),
        'stamp_card_badge': (By.XPATH, './/div[@data-qa="restaurant-badge-stampCards"]'),
        'delivery_costs_indicator': (By.XPATH, './/div[@data-qa="delivery-costs-indicator-content"]')
    }

    @property
    def name(self):
        return self._name.text

    @property
    def min_order_value(self):
        mov_eur, mov_cents = PRICE_PATTERN.match(self._min_order_value.text).groups()
        return int(mov_eur) + int(mov_cents) / 100

    @property
    def cuisines(self):
        return [el.text for el in self._cuisines]

    @property
    def has_offer(self):
        return "Offer" in self.text

    @property
    def has_stamp_card_badge(self):
        return self.stamp_card_badge.exists()

    @property
    def delivery_costs(self):
        return self.delivery_costs_indicator.text


class Restaurants(BaseElementList):
    _element_class = Restaurant

    def scroll_until_loaded(self):
        try:
            while True:
                with WaitChange(lambda: len(self), timeout=1):
                    self[-1].scroll_into_view()
        except TimeoutException:
            pass


class RestaurantsSection(BaseElementWrapper):
    _locators = {
        'restaurants': (Restaurants, By.XPATH, './/div[@data-qa="restaurant-card-element"]')
    }


class CuisineFilter(BaseElementWrapper):
    _locators = {
        '_categories': (BaseElementList, By.XPATH, './/div[@data-qa="swipe-navigation-item"]'),
        'swipe_next': (By.XPATH, '//div[@data-qa="swipe-navigation-action-next"]'),
        'more': (BaseElementWrapper, By.XPATH, './/button[@data-qa="swipe-navigation-item"]')
    }

    def get_category(self, name):
        return BaseElementWrapper(
            (By.XPATH, f'.//div[@data-qa="swipe-navigation-item" and .//text()="{name}"]'),
            self.driver,
            self)

    @property
    def categories(self):
        self.wait(10).until(lambda driver: len(self._categories) > 0)
        return self._categories


class CuisineModal(BaseElementWrapper):
    _locators = {
        'search_input': (By.XPATH,
                         './/input[@data-qa="cuisine-search-element" or @data-qa="cuisine-search-element-focused"]'),
        'categories': (BaseElementList, By.XPATH, './/div[@data-qa="cuisine-filter-modal-item-element"]')
    }

    CUISINE_PATTERN = re.compile(r'(.*) (\(\d+\))')

    def get_category(self, name):
        return BaseElementWrapper(
            (By.XPATH, f'.//div[@data-qa="cuisine-filter-modal-item-element" and contains(.//text(), "{name}")]'),
            self.driver,
            self)

    def select_category(self, name):
        with WaitChange(lambda: self.text, timeout=3):
            self.search_input.send_keys(name)
        self.get_category(name).click()


class SearchPage(BasePage):
    _locators = {
        'order_value_filter_options': (
            OrderValueFilterOptions, By.XPATH, '//fieldset[@data-qa="minimum-order-value-filter-options"]'),
        'open_section': (RestaurantsSection, By.XPATH, '//section[@data-qa="restaurant-list-open-section"]'),
        'pre_order_section': (RestaurantsSection, By.XPATH, '//section[@data-qa="restaurant-list-pre-order-section"]'),
        'closed_section': (RestaurantsSection, By.XPATH, '//section[@data-qa="restaurant-list-closed-section"]'),
        'restaurants': (Restaurants, By.XPATH, './/div[@data-qa="restaurant-card-element"]'),
        'cuisine_filter': (CuisineFilter, By.XPATH, '//div[@data-qa="cuisine-filter"]'),
        'cuisine_modal': (CuisineModal, By.XPATH, '//div[@data-qa="cuisine-filter-modal"]'),
        'offers_checkbox': (By.XPATH, '(//fieldset[@data-qa="discount-filter"]//div[@data-qa="checkbox"])[1]/..//span'),
        'stamp_cards_checkbox': (By.XPATH, '(//fieldset[@data-qa="discount-filter"]//div[@data-qa="checkbox"])[2]/..//span'),
        'free_delivery_switch': (By.XPATH, '//div[@data-qa="free-delivery-filter-switch"]'),
        'open_now_switch': (By.XPATH, '//div[@data-qa="availability-filter-switch"]'),
        'skeleton_bar': (By.XPATH, '//div[@data-qa="skeleton-bar"]')
    }

    def loaded(self):
        return len(self.find_elements(By.XPATH, '//div[@data-qa="skeleton-bar"]')) == 0

    def wait_loaded(self):
        try:
            self.wait(2).until(lambda driver: not self.loaded())
        except TimeoutException:
            pass

        self.wait(10).until(lambda driver: self.loaded())

    def select_category_modal(self, name):
        """
        Click "Show More" button, search restaurant category in the modal, select it.
        """
        self.cuisine_filter.more.click()
        self.cuisine_modal.select_category(name)

    def select_category_filter(self, name):
        """
        Select restaurant category clicking it on the filter
        """
        cuisine_button = self.cuisine_filter.get_category(name)
        cuisine_button.click()

