import os
import unittest

from fluidily import Fluidily, FluidilyError


try:
    import fluidily_config  # noqa
except ImportError:
    pass

test_app = 'fluid-test'
test_organisation = os.environ.get('FLUIDILY_ORGANISATION')
client = Fluidily(os.environ.get('FLUIDILY_URL'),
                  token=os.environ.get('FLUIDILY_TOKEN'))


class TestFluidily(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            client.applications.delete(test_app)
        except FluidilyError:
            pass
        client.applications.create(name=test_app,
                                   organisation=test_organisation)

    @classmethod
    def tearDownClass(cls):
        client.applications.delete(test_app)

    def test_urls(self):
        self.assertTrue(client.urls())

    def test_applications_get_list(self):
        apps = client.applications.get_list()
        self.assertTrue(apps)

    # TEMPLATES
    def test_create_fail(self):
        with self.assertRaises(FluidilyError) as e:
            client.templates.create(name='test', body='{{ html_main }}')
        self.assertEqual(e.exception.status_code, 422)
