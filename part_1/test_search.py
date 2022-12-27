import pytest


@pytest.fixture(scope='function')
def search_address(open_main_page, main_page, search_page, configuration):
    """
    Open main page and search an address.
    """
    main_page.search_address(configuration['default_test_address'])
    search_page.wait_loaded()


class TestSearchRestaurants:
    def __get_open_and_opening_soon_restaurants(self, search_page):
        skip = True
        restaurants = []

        # I can not guarantee that at the time of test execution any restaurants are open unless I mock the API call
        # so that test has to have this bit of logic to not fail when all restaurants are closed
        if search_page.open_section.exists():
            search_page.open_section.restaurants.scroll_until_loaded()
            restaurants += [r for r in search_page.open_section.restaurants]
            skip = False

        if search_page.pre_order_section.exists():
            search_page.pre_order_section.restaurants.scroll_until_loaded()
            restaurants += [r for r in search_page.pre_order_section.restaurants]
            skip = False

        # if all restaurants are closed and no restaurants are opening soon, this test can not be executed as
        # minimal order value is not displayed on closed restaurants.
        if skip:
            pytest.skip("There is no open or pre order restaurants available at this address.")

        return restaurants


    @pytest.mark.usefixtures('search_address')
    @pytest.mark.parametrize('rado_element_name, expected_mov', (
            ('less_10_eur', 10),
            ('less_15_eur', 15)
    ))
    def test_minimum_order_value(self, rado_element_name, expected_mov, search_page):
        """
        User searches restaurants at their address
        User selects one of Minimum order amount options
        Only restaurants which have Minimum order amount less than the selected option are displayed
        """
        search_page.order_value_filter_options.get_element_wrapper(rado_element_name).click()
        restaurants = self.__get_open_and_opening_soon_restaurants(search_page)
        wrong_restaurants = [(restaurant.name.text, restaurant.min_order_value)
                             for restaurant in restaurants
                             if restaurant.min_order_value > expected_mov]

        error_rest_list = '\n'.join([f'{name}, mov={mov}' for name, mov in wrong_restaurants])

        assert len(wrong_restaurants) == 0, \
            f"Expected order value is {expected_mov} Following restaurants have minimum " \
            f"order value above that: \n" \
            f"{error_rest_list}"

    def __check_restaurants_have_cuisine(self, search_page, category_name):
        search_page.restaurants.scroll_until_loaded()
        wrong_restaurants = [restaurant.name
                             for restaurant in search_page.restaurants
                             if category_name not in restaurant.cuisines]

        error_rest_list = '\n'.join(wrong_restaurants)

        assert len(wrong_restaurants) == 0, \
            f"Expected having {category_name} in cuisines list. Following restaurants don't have it:\n" \
            f"{error_rest_list}"

    @pytest.mark.usefixtures('search_address')
    @pytest.mark.parametrize('category_name', (
            'Chinese',
            'Indonesian',
    ))
    def test_category_filter(self, category_name, search_page):
        """
        User searches restaurants at their address
        User selects one of restaurant categories using category filter (category available directly on the filter)
        Only restaurants which have selected food category are displayed
        """
        search_page.select_category_filter(category_name)
        self.__check_restaurants_have_cuisine(search_page, category_name)

    @pytest.mark.usefixtures('search_address')
    @pytest.mark.parametrize('category_name', (
            'Korean',
            'African',
    ))
    def test_category_more(self, category_name, search_page):
        """
        User searches restaurants at their address
        User selects one of restaurant categories using category filter (category is not available directly on the
            filter, user clicks Show More button)
        Only restaurants which have selected food category are displayed
        """
        search_page.select_category_modal(category_name)
        self.__check_restaurants_have_cuisine(search_page, category_name)

    @pytest.mark.usefixtures('search_address')
    def test_open_now(self, search_page):
        """
        User searches restaurants at their address
        User switches "Open now" toggle in the restaurant filter
        Only open restaurants are displayed
        """
        search_page.open_now_switch.click()
        assert not search_page.pre_order_section.exists()
        assert not search_page.closed_section.exists()

    @pytest.mark.usefixtures('search_address')
    def test_offers(self, search_page):
        """
        User searches restaurants at their address
        User checks "Offers" checkbox in the restaurant filter
        Only restaurants with offer badge are displayed
        """
        search_page.offers_checkbox.click()
        restaurants = self.__get_open_and_opening_soon_restaurants(search_page)
        wrong_restaurants = [restaurant.name
                             for restaurant in restaurants
                             if not restaurant.has_offer]

        error_rest_list = '\n'.join(wrong_restaurants)

        # not sure what happening here, but looks like a bug. Those badges are not shown in Crome, but are shown in Opera.
        assert len(wrong_restaurants) == 0, \
            f"Expected offer badge on all restaurants. Following restaurants don't have it:\n" \
            f"{error_rest_list}"

    @pytest.mark.usefixtures('search_address')
    def test_stamp_cards(self, search_page):
        """
        User searches restaurants at their address
        User checks "StampCards" checkbox in the restaurant filter
        Only restaurants with "StampCard" badge are displayed
        """
        search_page.stamp_cards_checkbox.click()
        search_page.restaurants.scroll_until_loaded()
        wrong_restaurants = [restaurant.name
                             for restaurant in search_page.restaurants
                             if not restaurant.has_stamp_card_badge]

        error_rest_list = '\n'.join(wrong_restaurants)

        assert len(wrong_restaurants) == 0, \
            f"Expected offer badge on all restaurants. Following restaurants don't have it:\n" \
            f"{error_rest_list}"
