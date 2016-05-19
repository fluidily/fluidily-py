import os
import unittest

from fluidily import Fluidily, FluidilyError


try:
    import fluidev  # noqa
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

    # INFO
    def test_urls(self):
        self.assertTrue(client.urls())

    def test_version(self):
        self.assertTrue(client.version()['version'])

    def test_packages(self):
        packages = client.python()
        self.assertTrue(packages['python'])
        self.assertTrue(packages['pulsar'])
        self.assertTrue(packages['lux'])

    def test_get_token_fail(self):
        with self.assertRaises(FluidilyError) as e:
            client.get_token(username='foo', password='dvvddvd')
        self.assertEqual(e.exception.status_code, 422)

    # APPLICATIONS
    def test_applications_get_list(self):
        apps = client.applications.get_list()
        self.assertTrue(apps['result'])

    def test_applications_set_config(self):
        app = client.applications.get(test_app)
        self.assertEqual(app.name, test_app)

    # TEMPLATES
    def test_template_create_fail(self):
        with self.assertRaises(FluidilyError) as e:
            client.templates.create(slug='test', body='{{ html_main }}')
        self.assertEqual(e.exception.status_code, 422)
        with self.assertRaises(FluidilyError) as e:
            client.templates.get('%s/test' % test_app)
        self.assertEqual(e.exception.status_code, 404)

    def test_template_create_success(self):
        result = client.templates.create(slug='test1',
                                         body='{{ html_main }}',
                                         application=test_app)
        self.assertEqual(result['slug'], 'test1')
        result = client.templates.get('%s/test1' % test_app)
        self.assertEqual(result['slug'], 'test1')

    def test_template_update_success(self):
        result = client.templates.create(slug='test2',
                                         body='{{ html_main }}',
                                         application=test_app)
        self.assertEqual(result['slug'], 'test2')
        result = client.templates.get('%s/test2' % test_app)
        self.assertEqual(result['slug'], 'test2')
        result = client.templates.update('%s/test2' % test_app,
                                         body='<navbar></navbar>'
                                              '{{ html_main }}')
        self.assertEqual(result['body'], '<navbar></navbar>{{ html_main }}')
