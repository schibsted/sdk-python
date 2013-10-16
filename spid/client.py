from spid import __version__
from spid.url_builder import SPiDUrlBuilder
from spid.http import RequestsClient

class RequiredArgumentMissing(Exception): pass
class SPiDAPIException(Exception): pass

class SPiDClient(object):
    config = {}
    default_options = {
        "timeout": 5.0,
        "headers": {
            "User-Agent": "sdk-python-{}".format(__version__)
        }
    }
    required_args = [
        "client_id",
        "client_secret",
        "client_sign_secret",
        "server",
        "https",
        "redirect_uri",
        "api_version",
        "production"
    ]

    def __init__(self, url_builder=SPiDUrlBuilder, http_client=RequestsClient, **config):
        for argument in self.required_args:
            if not argument in config.keys():
                raise RequiredArgumentMissing(argument)
        self.config = dict(self.default_options, **config)
        self.http_client = http_client()
        self.url_builder = url_builder(**config)

    def make_request(self, uri, method="GET", **kwargs):
        http_options = ["headers", "timeout", "proxies"]
        for option in http_options:
            if option in self.config and option not in kwargs:
                kwargs[option] = self.config[option]

        resp = self.http_client.dispatch(uri, method, **kwargs)

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
