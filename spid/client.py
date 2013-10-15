import requests
from spid import __version__
from spid.url_builder import SPiDUrlBuilder

class RequiredArgumentMissing(Exception): pass
class InvalidHTTPMethod(Exception): pass
class SPiDAPIException(Exception): pass

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

    def __http_get(self, uri, params={}, **kwargs):
        return requests.get(uri, params=params, timeout=self.options.get("timeout"), **kwargs)

    def __http_post(self, uri, data={}, **kwargs):
        return requests.post(uri, data=data, timeout=self.options.get("timeout"), **kwargs)

    def __http_delete(self, uri, data={}, **kwargs):
        return requests.delete(uri, data=data, timeout=self.options.get("timeout"), **kwargs)

    def make_request(self, uri, method="GET", **kwargs):
        http_call_dict = {
            "GET":    self.__http_get,
            "POST":   self.__http_post,
            "DELETE": self.__http_delete
        }
        default_headers = {
            "User-Agent": "sdk-python-{}".format(__version__),
        }
        method = method.upper()
        if not method in http_call_dict.keys():
            raise InvalidHTTPMethod(method)

        kwargs["headers"] = default_headers
        if "headers" in kwargs.keys():
            kwargs["headers"] = dict(default_headers, **kwargs["headers"])

        resp = http_call_dict[method](uri, **kwargs)
        if resp.status_code >= 400 and "error" in resp.json().keys():
            raise SPiDAPIException(resp.json())

        return resp

    def auth(self):
        payload = {
            "client_id":     self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "redirect_uri":  self.config["redirect_uri"],
            "grant_type":    "client_credentials",
            "scope":         "",
            "state":         ""
        }
        return self.make_request(self.url_builder.get_url("token"), "POST", data=payload)

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
        return self.make_request(self.url_builder.get_url("token"), "POST", data=payload)

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
        return self.make_request(self.url_builder.get_url("token"), "POST", data=payload)

    def api(self, path, method="GET", params={}):
        return self.make_request(self.url_builder.get_url("api", path), method, params=params)