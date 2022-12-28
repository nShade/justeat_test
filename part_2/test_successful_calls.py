import http
import pytest
from json_checker import Or
from api_wrapper.wrapper import BarnApiWrapper
from utils.timer import repeat_until
from utils.assertions import assert_json


@pytest.fixture(scope='session')
def user(configuration):
    api_wrapper = BarnApiWrapper(configuration['base_url'], configuration['user_info']['id'])
    api_wrapper.authenticate(configuration['auth_url'], configuration['client_id'], configuration['client_secret'])
    return api_wrapper


@pytest.mark.usefixtures('debug')
class TestBarn:
    def test_userinfo(self, user, configuration):
        """
        User requests their user info
        Operation should be successful
        Response should contain requested information
        """
        resp = user.get_user()
        assert resp.status_code == http.HTTPStatus.OK
        userinfo = configuration['user_info']
        assert_json({'email': userinfo['email'],
                     'firstName': userinfo['first_name'],
                     'id': userinfo['id'],
                     'lastName': userinfo['last_name']},
                    resp.json(),
                    '/me call response is not as expected')

    def test_unlock_barn(self, user, configuration):
        """
        User requests to unlock the barn
        Operation should be successful
        """
        resp = user.unlock_barn()
        assert resp.status_code == http.HTTPStatus.OK
        assert_json({'action': 'barn-unlock',
                     'success': True,
                     'message': str,
                     'data': None},
                    resp.json(),
                    '/barn-unlock call response is not as expected')

    def test_count_eggs(self, user, configuration):
        """
        User requests amount of eggs collected today
        Operation should be successful
        Response should contain amount of eggs collected today (None if nothing was collected)
        """
        resp = user.count_eggs()
        assert resp.status_code == http.HTTPStatus.OK
        assert_json({'action': 'eggs-count',
                     'success': True,
                     'message': str,
                     'data': int},
                    resp.json(),
                    '/eggs-count call response is not as expected')

    def test_count_after_collect(self, user, configuration):
        """
        User requests to collect the eggs
        After the eggs are collected, User requests amount of eggs collected today
        Amount of eggs collected through the day should increase by the amount of eggs collected
        """
        # this test is susceptible for false negative if someone uses the same user account in parallel and
        # calls /eggs-collect. The best way to avoid it is to generate unique user before the test and delete
        # it afterwards to guarantee no other test uses the same user in parallel. Or have a centralized test user
        # orchestrator.
        count_1_resp = user.count_eggs()
        eggs_before_collect = count_1_resp.json()['data'] or 0

        eggs_collected = repeat_until(
            lambda: user.collect_eggs().json()['data'] or 0,
            lambda res: res > 0,
            timeout=30,
            poll_frequency=1,
        )

        if eggs_collected == 0:
            pytest.skip("No eggs collected within 30 seconds.")

        count_2_resp = user.count_eggs()
        eggs_after_collect = count_2_resp.json()['data'] or 0
        assert eggs_after_collect == eggs_before_collect + eggs_collected, \
            "/eggs-count method returned wrong count of egss"

    def test_collect_eggs(self, user, configuration):
        """
        User requests to collect the eggs
        Operation should be successful
        Response should contain the amount of eggs collected (None if nothing is collected)
        """
        resp = user.collect_eggs()
        assert resp.status_code == http.HTTPStatus.OK
        assert_json({'action': 'eggs-collect',
                     'success': True,
                     'message': str,
                     'data': Or(int, None)},
                    resp.json(),
                    '/eggs-collect call response is not as expected')

    def test_feed_chickens(self, user, configuration):
        """
        User requests to feed the chickens
        Operation should be successful
        """
        resp = user.feed_chickens()
        assert resp.status_code == http.HTTPStatus.OK
        assert_json({'action': 'chickens-feed',
                     'success': True,
                     'message': str,
                     'data': None},
                    resp.json(),
                    '/chickens-feed call response is not as expected')

    def test_put_down_toilet_seat(self, user, configuration):
        """
        User requests to put down the toilet seat
        Operation should be successful
        """
        resp = user.put_down_toilet_seat()
        assert resp.status_code == http.HTTPStatus.OK
        assert_json({'action': 'toiletseat-down',
                     'success': True,
                     'message': str,
                     'data': None},
                    resp.json(),
                    '/toiletseat-down call response is not as expected')
