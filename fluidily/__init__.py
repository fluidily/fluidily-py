__version__ = '0.0.1'


class Fluidily:
    """Python client to fluidily.com
    """
    url = 'http://fluidily.com'

    def __init__(self, url=None, sessions=None, token=None):
        if sessions is None:
            from pulsar.apps.http import HttpClient
            sessions = HttpClient()
        self.url = url or self.url
        self.token = token
        self.sessions = sessions
        self.sessions.headers['content-type'] = 'application/json'
        self.sessions.headers['accept'] = 'application/json, text/*; q=0.5'
        self.url = url
        self.applications = Applications(self, '/applications')
        self.organisations = Organisations(self, '/organisations')

    def urls(self):
        return self.execute('')

    def get_token(self, **params):
        """"""
        token = self.token
        self.token = None
        try:
            data = self.execute('/authorizations', 'post', data=params)
        except Exception:
            self.token = token
            raise
        self.token = data['token']
        return self.token

    def execute(self, command, method=None, headers=None, **params):
        url = '%s%s' % (self.url, command)
        method = method or 'GET'
        if self.token:
            headers = headers or []
            headers.append(('Authorization', 'Bearer %s' % self.token))
        response = self.sessions.request(method, url, headers=headers,
                                         **params)
        if not response.status_code:
            response.raise_for_status()
        elif response.status_code >= 400:
            error = response.decode_content()
            if isinstance(error, dict):
                error = error.get('message', error)
            error = '%d: %s' % (response.status_code, error)
            raise FluidilyError(status=response.status_code, msg=error)
        if response.raise_for_status == 204:
            return True
        return response.decode_content()


class FluidilyError(Exception):

    def __init__(self, status, msg):
        super().__init__(msg)
        self.status_code = status


class Fluid:

    def __init__(self, root, url):
        self.root = root
        self.url = url

    def get_list(self, **params):
        return self.root.execute(self.url, **params)

    def get(self, id):
        return self.root.execute('%s/%s' % (self.url, id))

    def create(self, **params):
        return self.root.execute(self.url, 'post', data=params)

    def delete(self, id):
        return self.root.execute('%s/%s' % (self.url, id), 'delete')


class Applications(Fluid):
    pass


class Organisations(Fluid):
    pass
