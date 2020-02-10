import os

class Constants(object):
    LIST_ID = os.environ.get('LIST_ID')


class TwitterConstants(object):
    CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
    CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")


class AWSConstants(object):
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    BUCKET = os.environ.get('BUCKET')
    TWITTER_BUCKET = os.environ.get('TWITTER_BUCKET')