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

    def urls(self):
        return self.execute('')

    def get_token(self, **params):
        """"""
        data = self.execute('/authorizations', 'post', data=params)
        self.token = data['token']
        return self.token

    def execute(self, command, method=None, **params):
        url = '%s%s' % (self.url, command)
        method = method or 'GET'
        response = self.sessions.request(method, url, **params)
        response.raise_for_status()
        return response.json()
