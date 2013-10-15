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
        if path:
            url = "{}/{}".format(url, path)
        return url
