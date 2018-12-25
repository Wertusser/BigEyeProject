from typing import Dict
from urllib.parse import urlencode, urljoin
import websockets
import asyncio
import uvloop
import aiojobs
import json

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class PureWsListener:
    def __init__(self, ws_url):
        self.url = ws_url

    async def auth(self):
        return await self.create_connection(self.url)

    @staticmethod
    async def create_connection(url):
        return await websockets.connect(url)

    def handler(self, data):
        pass


class MultipleWsListener:
    def __init__(self, *listeners):
        self.listeners = listeners
        self.conn = {}

    async def connect(self):
        self.conn = {listener.name: (await listener.auth(), listener.handler) for listener in self.listeners}

    @staticmethod
    async def listen(name, websocket, listener_handler, output):
        try:
            while True:
                msg = await websocket.recv()
                resp = json.loads(msg)
                resp = listener_handler(resp)
                await output(resp)
        except KeyboardInterrupt:
            websocket.close()

    async def recv(self, output):
        scheduler = await aiojobs.create_scheduler()
        try:
            for name, data in self.conn.items():
                conn, handler = data
                await scheduler.spawn(self.listen(name, conn, handler, output))
        except KeyboardInterrupt:
            scheduler.close()


class WsListener:
    def __init__(self, api_url: str, methods: Dict[str, str]):
        self.methods = methods
        self.api_url = api_url

    @staticmethod
    def build(url: str, method: str, **query_params):
        return f"{urljoin(url, method)}?{urlencode(query_params)}"

    @staticmethod
    async def create_connection(url):
        return await websockets.connect(url)

    async def auth(self):
        pass

    def get_rules(self, *args, **kwargs):
        pass

    def add_rules(self, *args, **kwargs):
        pass

    def delete_rules(self, *args, **kwargs):
        pass

    def create_listener(self, *args, **kwargs):
        pass

    def handler(self, data):
        pass
