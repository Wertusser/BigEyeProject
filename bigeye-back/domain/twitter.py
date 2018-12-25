from domain.base import WsListener


class TwitterListener(WsListener):
    def __init__(self, consumer_key, consumer_secret, name="Twitter"):
        _api_url = ""
        _methods = {"auth": ""}
        super().__init__(api_url=_api_url, methods=_methods)
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.name = name
