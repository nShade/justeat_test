import pytest
import selenium
from pages.main_page import MainPage
from pages.search_page import SearchPage


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        help="Browser to use",
        default='chrome',
    )


@pytest.fixture(scope='session')
def configuration(pytestconfig):
    """
    This fixture returns configuration dictionary. Now this dictionary is hardcoded in it, but in real test framework
    it could be loaded from config file or any other configuration storage
    """
    return {
        'browser': pytestconfig.getoption('browser'),
        'url': 'https://www.lieferando.de/en/',
        'default_test_address': 'Alexanderplatz'
    }


@pytest.fixture(scope='session')
def browser(configuration):
    BROWSERS = {
        'firefox': selenium.webdriver.Firefox,
        'chrome': selenium.webdriver.Chrome,
        'safari': selenium.webdriver.Safari
    }
    driver_class = BROWSERS[configuration['browser']]

    with driver_class() as driver:
        driver.set_window_size(1200, 1000)
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
