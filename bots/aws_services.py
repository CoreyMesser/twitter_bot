import boto3
import pandas as pd
import uuid
import logging
import os

from io import StringIO
from bots.constants import AWSConstants as awsc


class AWSConnection(object):

    def __init__(self):
        self.client = boto3.client('s3')
        self.bucket = awsc.BUCKET


    def s3_list_objects(self):
        obj_list = list(self.client.list_objects(Bucket=self.bucket))
        return obj_list

    def s3_get_latest(self, obj_list):
        return obj_list[len(obj_list)-1]


    def s3_get_csv_object(self, latest):
        csv_obj = self.client.get_object(Bucket=self.bucket, Key=latest)
        body = csv_obj['Body']
        csv_string = body.read().decode('uf-8')
        df = pd.read_csv(StringIO(csv_string))
        return df
