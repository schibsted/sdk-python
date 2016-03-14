import urllib

class SPiDUrlBuilder(object):
    def __init__(self, **client_config):
        self.client_config = client_config

    def build_base_url(self):
        conf = self.client_config
        url = ""
        if conf.get("https") or conf.get("production"):
            url = "https"
        else:
            url = "http"
        url += "://{}".format(conf.get("server"))
        return url

    def build_api_url(self):
        conf = self.client_config
        return "{}/api/{}".format(self.build_base_url(), str(conf.get("api_version")))

    def build_token_url(self):
        return "{}/oauth/token".format(self.build_base_url())

    def get_url(self, name="www", path=""):
        base_url_dict = {
            "api":      self.build_api_url,
            "api_read": self.build_api_url,
            "token":    self.build_token_url,
            "www":      self.build_base_url,
            "default":  self.build_base_url
        }
        url = ""
        if not name in base_url_dict:
            url = base_url_dict["default"]()
        else:
            url = base_url_dict[name]()
        return url+path

    def get_login_url(self, params={}):
        default = {
            'client_id'     : self.client_config.get('client_id'),
            'response_type' : 'code',
            'redirect_uri'  : self.client_config.get('redirect_uri')
        }
        combined = dict(default, **params)
        return self.get_url(path="/flow/login")+"?"+urllib.urlencode(combined)

    def get_logout_url(self, params={}):
        default = {
            'client_id'     : self.client_config.get('client_id'),
            'redirect_uri'  : self.client_config.get('redirect_uri'),
        }
        combined = dict(default, **params)
        return self.get_url(path="/logout")+"?"+urllib.urlencode(combined)

    def get_signup_url(self, params={}):
        default = {
            'client_id'     : self.client_config.get('client_id'),
            'response_type' : 'code',
            'redirect_uri'  : self.client_config.get('redirect_uri')
        }
        combined = dict(default, **params)
        return self.get_url(path="/flow/signup")+"?"+urllib.urlencode(combined)

    def get_auth_url(self, params={}):
        default = {
            'client_id'     : self.client_config.get('client_id'),
            'response_type' : 'code',
            'redirect_uri'  : self.client_config.get('redirect_uri'),
        }
        combined = dict(default, **params)
        return self.get_url(path="/flow/auth")+"?"+urllib.urlencode(combined)

    def get_purchase_url(self, params={}):
        default = {
            'client_id'     : self.client_config.get('client_id'),
            'response_type' : 'code',
            'redirect_uri'  : self.client_config.get('redirect_uri'),
            'flow'          : 'payment'
        }
        combined = dict(default, **params)
        return self.get_url(path="/flow/checkout")+"?"+urllib.urlencode(combined)

    def get_account_url(self, params={}):
        default = {
            'client_id'     : self.client_config.get('client_id'),
            'redirect_uri'  : self.client_config.get('redirect_uri'),
        }
        combined = dict(default, **params)
        return self.get_url(path="/account/summary")+"?"+urllib.urlencode(combined)
