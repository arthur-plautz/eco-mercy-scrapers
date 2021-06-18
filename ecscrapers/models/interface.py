from ecscrapers.models.shopee import Shopee
from io import StringIO
from datetime import date
import os
import unidecode
import yaml
import json
import logging
import boto3
import pandas as pd

class Interface:
    def __init__(self):
        self.__build_config()
        self.__build_log()
        self.__build_model()

    def __build_model(self):
        model_type = self.config.get('model')

        if model_type == 'shopee':
            self.model = Shopee(log_file=self.log)
        else:
            raise Exception('Model Not Found!')

    def __build_log(self):
        enable_file_log = os.getenv('FILE_LOG')
        if enable_file_log or self.config.get('log'):
            log_file = self.config.get('log', 'general.log')
            dir_path = f'{os.getcwd()}/logs/'
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            self.log = dir_path + log_file
        else:
            self.log = None

    def __build_credentials(self):
        aws_public = os.getenv('AWS_PUBLIC')
        aws_secret = os.getenv('AWS_SECRET')
        if aws_public and aws_secret:
            self.credentials = {
                'secret': aws_secret,
                'public': aws_public
            }
        else:
            raise Exception('AWS Credentials not found!')

    def __build_config(self):
        if os.getenv('CONFIG'):
            try:
                self.config = json.loads(os.getenv('CONFIG'))
            except Exception as exc:
                print(exc)
        else:
            path = f'{os.getcwd()}/ecscrapers/config/run.yml'
            with open(path, 'r') as stream:
                try:
                    self.config = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)

    def __send_to_s3(self, data, operation, search):
        df = pd.DataFrame(data)
        df['id'] = df.index

        today = date.today()
        file_name = self.config.get('output', today.strftime("%d_%m_%Y"))

        bucket = self.config.get('s3_bucket')
        if bucket:
            search_salt = unidecode.unidecode(search).replace(" ", "_")
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)

            session = boto3.Session(
                aws_access_key_id=self.credentials.get('public'),
                aws_secret_access_key=self.credentials.get('secret')
            )

            s3_resource = session.resource('s3')
            s3_resource.Object(bucket, f'data/{operation}/{search_salt}/e{file_name}.csv').put(Body=csv_buffer.getvalue())
            logging.info('Successfull Upload to S3!')
        else:
            raise Exception('No bucket name provided!')

    def execute(self, local=False):
        if not local:
            self.__build_credentials()

        operation = self.config.get('run')

        if operation:
            function = getattr(self.model, operation)
        else:
            raise Exception('Invalid Operation!')

        search = self.config.get('search')

        if not search:
            raise Exception('No Search has been found!')

        filters = dict(self.config.get('filters', {}))

        df = function(search, filters)
        if local:
            dir_path = f'{os.getcwd()}/data'
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            df.to_csv(f'{dir_path}/{operation}.csv')
        else:
            self.__send_to_s3(df, operation, search)
