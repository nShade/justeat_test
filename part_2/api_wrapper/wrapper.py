from functools import reduce
from urllib.parse import urljoin
import requests


def join(*parts):
    return reduce(urljoin, parts)


class BarnApiWrapper:

    def __init__(self, base_url, user_id):
        self._base_url = base_url
        self._token = ''
        self._user_id = user_id

    def authenticate(self, auth_url, client_id, client_secret):
        resp = requests.request("POST", auth_url, data={'client_id': client_id,
                                                        'client_secret': client_secret,
                                                        'grant_type': 'client_credentials'})
        resp_json = resp.json()
        self._token = f'{resp_json["token_type"]} {resp_json["access_token"]}'

    def send_request(self, method, path, **kwargs):
        return requests.request(method, urljoin(self._base_url, path), **kwargs)

    def send_authorized_request(self, *args, **kwargs):
        headers = {}
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])

        headers.update({'Authorization': self._token})
        new_kwargs = {}
        new_kwargs.update(kwargs)
        new_kwargs['headers'] = headers
        return self.send_request(*args, **new_kwargs)

    def get_user(self):
        return self.send_authorized_request('GET', 'me')

    def unlock_barn(self):
        return self.send_authorized_request('POST', urljoin(f'{self._user_id}/', 'barn-unlock'))

    def put_down_toilet_seat(self):
        return self.send_authorized_request('POST', urljoin(f'{self._user_id}/', 'toiletseat-down'))

    def feed_chickens(self):
        return self.send_authorized_request('POST', urljoin(f'{self._user_id}/', 'chickens-feed'))

    def collect_eggs(self):
        return self.send_authorized_request('POST', urljoin(f'{self._user_id}/', 'eggs-collect'))

    def count_eggs(self):
        return self.send_authorized_request('POST', urljoin(f'{self._user_id}/', 'eggs-count'))
