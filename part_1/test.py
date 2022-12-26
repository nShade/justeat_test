import pytest
import selenium.webdriver
from pages.main_page import MainPage
from pages.search_page import SearchPage


@pytest.fixture(scope='session')
def configuration():
    return {
        'url': 'https://www.lieferando.de/en/'
    }


@pytest.fixture(scope='session')
def browser():
    with selenium.webdriver.Firefox() as driver:
        yield driver


@pytest.fixture(scope='function')
def main_page(browser, configuration):
    return MainPage(browser)


@pytest.fixture(scope='function')
def open_main_page(browser, configuration):
    browser.get(configuration['url'])


@pytest.fixture(scope='function')
def search_page(browser):
    page = SearchPage(browser)
    return page


@pytest.fixture(scope='function')
def search_address(open_main_page, main_page):
    main_page.search_address("Pannierstrasse 16")


class TestSearchAddress:
    @pytest.mark.usefixtures('search_address')
    def test_minimum_order_value(self, main_page, search_page):
        search_page.order_value_filter_options.less_10_eur.click()

        assert search_page.open_section.exists()
        search_page.open_section.restaurants.scroll_until_loaded()

        for restaurant in search_page.open_section.restaurants:
            assert restaurant.min_order_value <= 10
            assert not restaurant.shipping_time_indicator.exists()

        assert search_page.pre_order_section.exists()
        search_page.pre_order_section.restaurants.scroll_until_loaded()

        for restaurant in search_page.pre_order_section.restaurants:
            assert restaurant.min_order_value <= 10

    @pytest.mark.usefixtures('search_address')
    @pytest.mark.parametrize('cuisine_name', ['Italian'])
    def test_category(self, cuisine_name, main_page, search_page):
        italian_cuisine = search_page.cuisine_filter.get_cuisine(cuisine_name)

        if not italian_cuisine:
            search_page.cuisine_filter.more.click()
            search_page.cuisine_modal.search_input.send_keys(cuisine_name)
            italian_cuisine = search_page.cuisine_modal.get_cuisine(cuisine_name)

        assert italian_cuisine, f'{cuisine_name} cuisine not found.'
        italian_cuisine.click()

        if search_page.open_section.exists():
            search_page.open_section.restaurants.scroll_until_loaded()
            for restaurant in search_page.open_section.restaurants:
                assert cuisine_name in restaurant.cuisines

        if search_page.pre_order_section.exists():
            search_page.pre_order_section.restaurants.scroll_until_loaded()
            for restaurant in search_page.pre_order_section.restaurants:
                assert cuisine_name in restaurant.cuisines

        if search_page.closed_section.exists():
            search_page.closed_section.restaurants.scroll_until_loaded()
            for restaurant in search_page.closed_section.restaurants:
                assert cuisine_name in restaurant.cuisines
