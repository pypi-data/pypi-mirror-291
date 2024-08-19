import requests
from datetime import datetime, tzinfo, timedelta
from copy import deepcopy


class Session(requests.Session):
    _def_headers = {
        "Accept": "application/json"
    }

    def __init__(self, api=None, token=None, headers=None, timeout=None, base_url=None, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self._api = api

        if api is not None:
            self.set_base_url(api.base_url)
        if base_url is not None:
            self.set_base_url(base_url)

        self.headers = headers if headers is not None else Session._def_headers
        self.timeout = timeout

        self.auth = EvvaAuth(token)


    def set_base_url(self, url=None):
        self._base_url = url


    def send(self, *args, timeout=None, **kwargs):
        timout = timeout if timeout is not None else self.timeout
        
        return super().send(*args, timeout=timeout, **kwargs)


    def psend(self, req, *args, **kwargs):
        
        return super().send(self.prepare_request(req), *args, **kwargs)


    def prepare_request(self, request):
        """
        Perpare a request.

        `request.url` is preprocessed by `Session.make_url`.

        Return a `PreparedRequest` according to `requests.Session.prepare_request`.
        """
        req = deepcopy(request)

        if self._base_url is not None:
            req.url = self._base_url + req.url
        
        return super().prepare_request(req)


class EvvaAuth(object):
    def __init__(self, token=None):
        self.set_apikey(token)

    def set_apikey(self, key):
        self._token = key

    def __call__(self, r):
        if self._token is not None:
            r.headers.update({'X-API-Key': self._token})
        return r


class Zulu(tzinfo):
    """
    Dummy timezone class with name "Z" and null delta over UTC

    Todo: check if this is correct.
    """
    def utcoffset(self, dt):
        return timedelta(0)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "Z"
