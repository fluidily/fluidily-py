import os
import configparser


def token_from_config(filename):
    config = configparser.ConfigParser()
    path = os.path.join(os.path.expanduser("~"), filename)
    if os.path.isfile(path):
        config.read(path)
        return config.get('credentials', 'token')
