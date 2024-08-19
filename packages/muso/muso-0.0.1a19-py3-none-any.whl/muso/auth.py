# -*- coding: UTF-8 -*-

from muso.request import MusoRequest


class AuthBase:

    def __init__(self):
        self.uri = None
        self.method = None

    def fill_uri_and_method(self, *, uri: str, method: str):
        self.uri = uri
        self.method = method

    @property
    def auth_name(self):
        raise NotImplementedError

    @property
    def auth_type(self):
        raise NotImplementedError

    def __call__(self, *, request: MusoRequest):
        raise NotImplementedError
