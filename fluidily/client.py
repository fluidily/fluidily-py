from .config import token_from_config


class Fluidily:
    """Python client to fluidily.com API
    """
    url = 'https://api.fluidily.com'

    def __init__(self, url=None, sessions=None, token=None):
        if sessions is None:
            import requests
            sessions = requests.Session()
        self.url = url or self.url
        self.token = token
        self.sessions = sessions
        self.applications = Applications(self)
        self.organisations = Organisations(self)
        self.contents = Contents(self)
        self.templates = Templates(self)
        if token is None:
            self.token = token_from_config('.fluidily')

    def urls(self):
        return self.execute(self.url)

    def version(self):
        return self.execute('%s/info/version' % self.url)

    def python(self):
        return self.execute('%s/info/python' % self.url)

    def get_token(self, **params):
        """"""
        token = self.token
        self.token = None
        try:
            data = self.execute(self.url + '/authorizations',
                                'post', json=params)
        except Exception:
            self.token = token
            raise
        self.token = data['token']
        return self.token

    def execute(self, url, method=None, headers=None, **params):
        method = method or 'GET'
        headers = headers or {}
        if self.token:
            headers['Authorization'] = 'Bearer %s' % self.token
        headers['Accept'] = 'application/json, text/*; q=0.5'
        response = self.sessions.request(method, url, headers=headers,
                                         **params)
        if not response.status_code:
            response.raise_for_status()
        elif response.status_code >= 400:
            try:
                error = response.json()
            except Exception:
                error = response.text
            raise FluidilyError(response.status_code, error)
        if response.status_code == 204:
            return True
        return response.json()


class FluidilyError(Exception):

    def __init__(self, status, error):
        self.status_code = status
        self.error = error


class Fluid:

    def __init__(self, root, url=None):
        self.root = root
        self.url = '%s/%s' % (root.url, url or self.__class__.__name__.lower())

    def __repr__(self):
        return self.url
    __str__ = __repr__

    def get_list(self, **params):
        return self.execute(self.url, params=params)

    def get(self, id):
        return self.execute('%s/%s' % (self.url, id))

    def create(self, **params):
        return self.execute(self.url, 'post', json=params)

    def update(self, id, **params):
        url = '%s/%s' % (self.url, id)
        return self.execute(url, 'post', json=params)

    def delete(self, id):
        return self.execute('%s/%s' % (self.url, id), 'delete')

    def execute(self, url, method=None, **params):
        return self.root.execute(url, method, **params)


class Applications(Fluid):

    def get(self, id):
        return Application(self, super().get(id))


class Organisations(Fluid):
    pass


class Contents(Fluid):

    def get_list(self, application=None, **params):
        url = self.url
        if application:
            url = '%s/%s' % (url, application)
        return self.root.execute(url, params=params)


class Templates(Contents):
    pass


class Application:

    def __init__(self, root, app):
        self.__dict__.update(app)
        self.root = root

    def __repr__(self):
        return self.url
    __str__ = __repr__

    def set_config(self, key, value):
        url = '%s/config' % self.url
        return self.root.execute(url, 'post', json={key: value})
