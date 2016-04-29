import os
import json
import unittest
from unittest import skipUnless

import fluidily

try:
    import fluidily_config  # noqa
except ImportError:
    pass


cfg = json.loads(os.environ.get('FLUIDILY_CONFIG', '{}'))

client = fluidily.Fluidily(cfg.pop('url', 'https://api.quantmind.com'),
                           token=cfg.pop('token', None))


class TestFluidily(unittest.TestCase):

    def test_urls(self):
        self.assertTrue(client.urls())

    @skipUnless(cfg.get('username'), 'requires username')
    def test_token(self):
        token = client.get_token(**cfg)
        self.assertEqual(client.token, token)

    def test_applications_get_list(self):
        apps = client.applications.get_list()
        self.assertTrue(apps)
