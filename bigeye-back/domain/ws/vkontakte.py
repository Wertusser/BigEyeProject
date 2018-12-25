from domain.base import WsListener
import requests
from analytics.sentiment import get_sentiment_map
import math


class VkListener(WsListener):
    def __init__(self, token, v=5.92, name="Vkontakte"):
        _api_url = "https://api.vk.com/"
        _methods = {"auth": "method/streaming.getServerUrl",
                    "rules": "https://{url}/rules?key={key}",
                    "stream": "wss://{url}/stream?key={key}"}
        super().__init__(api_url=_api_url, methods=_methods)
        self.token = token
        self.v = v
        self.name = name
        self.auth_data = self._vk_auth()

    def _vk_auth(self):
        url: str = self.build(self.api_url, self.methods.get("auth", ""), v=self.v, access_token=self.token)
        resp = requests.get(url).json()
        return resp.get("response")

    async def auth(self):
        return await self.create_listener()

    def get_rules(self):
        url = self.auth_data.get("endpoint")
        key = self.auth_data.get("key")
        builded_url = self.methods.get("rules").format(url=url, key=key)
        return requests.get(builded_url).json()

    def add_rules(self, rules):
        result = []
        url = self.auth_data.get("endpoint")
        key = self.auth_data.get("key")
        for rule in rules:
            builded_url = self.methods.get("rules").format(url=url, key=key)
            resp = requests.post(builded_url, json=rule).json()
            result.append(resp)
        return result

    def delete_rules(self, rules):
        result = []
        url = self.auth_data.get("endpoint")
        key = self.auth_data.get("key")
        for rule in rules:
            builded_url = self.methods.get("rules").format(url=url, key=key)
            resp = requests.delete(builded_url, json=rule).json()
            result.append(resp)
        return result

    async def create_listener(self):
        url = self.auth_data.get("endpoint")
        key = self.auth_data.get("key")
        base = self.methods.get("stream").format(url=url, key=key)
        return await self.create_connection(base)

    def handler(self, data):
        text = get_sentiment_map(data["event"]["text"])
        url = data['event']['author']['author_url']
        f = [f"<a href='{url}' target='_blank'>{url} </a>"]
        for word in text:
            style = ''
            if word[1] < 0:
                style = "background-color: rgba(255, 0, 0, %s);" % math.fabs(word[1])
            if word[1] > 0:
                style = "background-color: rgba(0, 255, 0, %s);" % word[1]
            if word[1] == 0:
                style = ''
            p = f"<span style='{style}'>{word[0]} </span>"
            f.append(p)
        return "".join(f)
