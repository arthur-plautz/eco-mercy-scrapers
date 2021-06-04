from models.shopee import Shopee
import os
import yaml
import json

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
        log_file = self.config.get('log', 'general.log')
        self.log = f'{os.getcwd()}/logs/{log_file}'

    def __build_config(self):
        if os.getenv('CONFIG'):
            try:
                self.config = json.loads(os.getenv('CONFIG'))
            except Exception as exc:
                print(exc)
        else:
            path = f'{os.getcwd()}/config/run.yml'
            with open(path, 'r') as stream:
                try:
                    self.config = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)

    def execute(self):
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
        df.to_csv(f'{os.getcwd()}/data/{operation}.csv')
