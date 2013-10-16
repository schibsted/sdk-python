import requests
class InvalidHTTPMethod(Exception): pass

class RequestsClient(object):
    def dispatch(self, uri, method="GET", **kwargs):
        http_call_dict = {
            "GET":    self.__http_get,
            "POST":   self.__http_post,
            "DELETE": self.__http_delete
        }
        method = method.upper()
        if not method in http_call_dict.keys():
            raise InvalidHTTPMethod(method)
        return http_call_dict[method](uri, **kwargs)

    def __http_get(self, uri, params={}, **kwargs):
        return requests.get(uri, params=params, **kwargs)

    def __http_post(self, uri, data={}, **kwargs):
        return requests.post(uri, data=data, **kwargs)

    def __http_delete(self, uri, data={}, **kwargs):
        return requests.delete(uri, data=data, **kwargs)

