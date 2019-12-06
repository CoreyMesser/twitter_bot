import boto3
from botocore.exceptions import ClientError

import pandas as pd

from io import StringIO
from bots.constants import AWSConstants, TwitterConstants

import logging


class AWSConnection(object):

    def __init__(self):
        self.client = boto3.client('s3')
        awsc = AWSConstants()
        self.bucket = awsc.BUCKET
        self.tw_bucket = awsc.TWITTER_BUCKET
        self.tc = TwitterConstants()


    def s3_list_objects(self):
        obj = self.client.get_object(Bucket=self.bucket, Key=self.tc.TWITTER)
        return obj

    def s3_get_latest(self):
        get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
        objs = self.client.list_objects(Bucket='artistlist')['Contents']
        last_added = objs[-1]['Key']
        return last_added


    def s3_get_csv_object(self, latest):
        try:
            csv_obj = self.client.get_object(Bucket=self.bucket, Key=latest)
            body = csv_obj['Body']
            csv_string = body.read().decode('utf-8')
        except ClientError as e:
            logging.error(e)
            return None
        return csv_string.split('\n')
