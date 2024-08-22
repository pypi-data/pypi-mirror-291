import logging

import requests


class HTTP(object):
    def __init__(self, base_url: str = None, **kwargs):
        self.base_url = base_url
        self.session = requests.Session()
        for key, value in kwargs.items():
            setattr(self.session, key, value)

    def request(self, method, url, **kwargs):
        if self.base_url and not url.startswith('http'):
            url = '%s/%s' % (self.base_url.lstrip('/'), url.rstrip('/'))

        logging.debug(f"Request: GET {url} {kwargs}")
        res = self.session.request(method, url, **kwargs)
        logging.debug(f"Response: {res.text}")
        return res

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)

    def options(self, url, **kwargs):
        return self.request('OPTIONS', url, **kwargs)


http = HTTP()
