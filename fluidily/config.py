import os
import configparser


def from_config(filename, entry=None, token=None, url=None):
    config = configparser.ConfigParser()
    path = os.path.join(os.path.expanduser("~"), filename)
    if os.path.isfile(path):
        config.read(path)
        entry = entry or 'default'
        token = config.get(entry, 'token', fallback=token)
        if not url:
            url = config.get(entry, 'url', fallback=None)
    return token, url
