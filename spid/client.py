class RequiredArgumentMissing(Exception): pass

class SPiDClient(object):
    required_args = [
        "client_id",
        "client_secret",
        "client_sign_secret",
        "staging_domain",
        "https",
        "redirect_uri",
        "domain",
        "cookie",
        "api_version",
        "production"
    ]

    def __init__(self, **config):
        for argument in self.required_args:
            if not argument in config.keys():
                raise RequiredArgumentMissing(argument)
        self.config = config
