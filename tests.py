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
        except FluidilyError as exc:
            if exc.status_code != 404:
                raise
        client.applications.create(name=test_app,
                                   organisation=test_organisation)

    @classmethod
    def tearDownClass(cls):
        client.applications.delete(test_app)

    def test_urls(self):
        self.assertTrue(client.urls())

    def test_get_token_fail(self):
        with self.assertRaises(FluidilyError) as e:
            client.get_token(username='foo', password='dvvddvd')
        self.assertEqual(e.exception.status_code, 422)

    def test_applications_get_list(self):
        apps = client.applications.get_list()
        self.assertTrue(apps)

    # TEMPLATES
    def test_template_create_fail(self):
        with self.assertRaises(FluidilyError) as e:
            client.templates.create(slug='test', body='{{ html_main }}')
        self.assertEqual(e.exception.status_code, 422)

    def test_template_create_success(self):
        result = client.templates.create(slug='test',
                                         body='{{ html_main }}',
                                         application=test_app)
        self.assertEqual(result['slug'], 'test')
        result = client.templates.get('%s/test')
        self.assertEqual(result['slug'], 'test')
