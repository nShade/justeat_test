import http
import pytest
from api_wrapper.wrapper import BarnApiWrapper
from utils.assertions import assert_json


@pytest.mark.usefixtures('debug')
class TestAuthFail:
    def test_wrong_token(self, configuration):
        """
        User requests their user info with invalid token
        Response should fail with 401 http code
        """
        user = BarnApiWrapper(configuration['base_url'], configuration['user_info']['id'])
        user._token = 'Bearer 3f50ca22d8806f49c0db2ea9e217b1fe43765429'
        resp = user.get_user()
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED, \
            'Response code when calling the API with invalid token is not 401'
        assert_json({'error': 'invalid_token',
                     'error_description': 'The access token provided is invalid'},
                    resp.json(),
                    'Call response with invalid token is not as expected')

    def test_no_token(self, configuration):
        """
        User requests their user info without authorization token
        Response should fail with 401 http code
        """
        user = BarnApiWrapper(configuration['base_url'], configuration['user_info']['id'])
        resp = user.send_request('GET', 'me')
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED, \
            'Response code when calling the API with invalid token is not 401'
        assert_json({'error': 'access_denied', 'error_description': 'an access token is required'},
                    resp.json(),
                    'Call response with invalid token is not as expected')

    def test_valid_token_wrong_user_id(self, configuration):
        """
        User requests their user info with invalid token
        Response should fail with 401 http code
        """
        user = BarnApiWrapper(configuration['base_url'], configuration['user_info']['id'])
        user.authenticate(configuration['auth_url'], configuration['client_id'], configuration['client_secret'])
        user._user_id = '3333'
        resp = user.unlock_barn()
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED, \
            'Response code when calling the API with invalid token is not 401'
        assert_json({'error': 'access_denied',
                     'error_message': 'You do not have access to take this action on behalf of this user'},
                    resp.json(),
                    'Call response with invalid token is not as expected')
