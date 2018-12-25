import unittest
from domain.base import WsListener, MultipleWsListener
from domain.ws.vkontakte import VkListener
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.base = WsListener("", {})

    def test_build(self):
        actual = self.base.build("http://api.vk.com/", "auth", hello="world", isgood=1)
        self.assertEqual("http://api.vk.com/auth?hello=world&isgood=1", actual)

    def test_create_listener(self):
        loop = asyncio.get_event_loop()
        f = loop.run_until_complete(self.base.create_connection("wss://echo.websocket.org/"))
        self.assertTrue(f.is_client)


async def aprint(*args):
    print(*args)


class MultipleListenerTest(unittest.TestCase):
    def setUp(self):
        l = VkListener(token="5ac516e15ac516e15ac516e1015aa3d1e455ac55ac516e1011237fda012082912d0f0c5")
        # t = TwitterListener(consumer_key="", consumer_secret="")
        # rules = l.get_rules()
        # print(rules)
        # l.add_rules(
        #     [{"rule": {"value": f"{item}", "tag": f'tag_{i}'}} for i, item in enumerate(["я", "ты", "он", "типо"])])
        self.listener = MultipleWsListener(l)

    def test_connection(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.listener.connect())
        loop.run_until_complete(self.listener.recv(aprint))
        loop.run_forever()
