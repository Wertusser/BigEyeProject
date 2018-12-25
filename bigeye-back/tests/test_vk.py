import unittest
from domain.ws.vkontakte import VkListener
import asyncio


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.listener = VkListener(token='5ac516e15ac516e15ac516e1015aa3d1e455ac55ac516e1011237fda012082912d0f0c5')

    def test_auth(self):
        self.assertIn("key", self.listener._vk_auth())

    def test_get_rules(self):
        print(self.listener.get_rules())

    def test_set_rules(self):
        data = [{"rule": {"value": "я", "tag": 'tag_1312312312'}}]
        print(self.listener.add_rules(rules=data))

    def test_del_rules(self):
        data = [{"tag": 'tag_1312312312'}]
        print(self.listener.delete_rules(rules=data))

    def test_listen(self):
        loop = asyncio.get_event_loop()
        c = self.listener.create_listener()
        loop.run_until_complete(c)
