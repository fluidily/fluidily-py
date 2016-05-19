import os

from fluidily import Fluidily

DEV_URL = 'http://api.dynquant.com:9022'
DEV_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl9pZCI6IjFjMDgxMjI3ZmRhNjRiZDE4YzUzMzE3M2FkMWYwNGE4IiwibmFtZSI6ImxzYmFyZGVsIiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJsc2JhcmRlbCJ9.cfABJIWZbRfVrZC5XGpoMtZve93x8riWMUpHN7P8wdo'

os.environ['FLUIDILY_ORGANISATION'] = 'quantmind'
os.environ['FLUIDILY_URL'] = DEV_URL
os.environ['FLUIDILY_TOKEN'] = DEV_TOKEN


def fluidily():
    return Fluidily(DEV_URL, token=DEV_TOKEN)
