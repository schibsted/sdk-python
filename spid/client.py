import requests
from spid.url_builder import SPiDUrlBuilder

class RequiredArgumentMissing(Exception): pass
class InvalidHTTPMethod(Exception): pass

class SPiDClient(object):
    options = {}
    default_options = {
        "timeout": 5.0
    }
    required_args = [
        "client_id",
        "client_secret",
        "client_sign_secret",
        "server",
        "https",
        "redirect_uri",
        "domain",
        "cookie",
        "api_version",
        "production"
    ]

    def __init__(self, url_builder=SPiDUrlBuilder, **config):
        for argument in self.required_args:
            if not argument in config.keys():
                raise RequiredArgumentMissing(argument)
        self.config = dict(self.default_options, **config)
        self.url_builder = url_builder(**config)

    def __http_get(self, uri, payload={}):
        return requests.get(uri, params=payload, timeout=self.options.get("timeout"))

    def __http_post(self, uri, payload={}):
        return requests.post(uri, data=payload, timeout=self.options.get("timeout"))

    def __http_delete(self, uri, payload={}):
        return requests.delete(uri, params=payload, timeout=self.options.get("timeout"))

    def make_request(self, uri, method="GET", payload={}, ch=None):
        http_call_dict = {
            "GET":    self.__http_get,
            "POST":   self.__http_post,
            "DELETE": self.__http_delete
        }
        method = method.upper()
        if not method in http_call_dict.keys():
            raise InvalidHTTPMethod(method)
        return http_call_dict[method](uri, payload=payload)

    def auth(self):
        payload = {
            "client_id":     self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "redirect_uri":  self.config["redirect_uri"],
            "grant_type":    "client_credentials",
            "scope":         "",
            "state":         ""
        }
        return self.make_request(self.url_builder.get_url("token"), "POST", payload=payload)

    def get_access_token(self, code):
        payload = {
            "client_id":     self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "redirect_uri":  self.config["redirect_uri"],
            "code":          code,
            "grant_type":    "authorization_code",
            "scope":         "",
            "state":         ""
        }
        return self.make_request(self.url_builder.get_url("token"), "POST", payload=payload)

    def refresh_access_token(self, refresh_token):
        payload = {
            "client_id":     self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "redirect_uri":  self.config["redirect_uri"],
            "refresh_token": refresh_token,
            "grant_type":    "refresh_token",
            "scope":         "",
            "state":         ""
        }
        return self.make_request(self.url_builder.get_url("token"), "POST", payload=payload)