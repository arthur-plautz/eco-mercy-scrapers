import yaml
import os
import pandas as pd

class Products:
    def __init__(self, model):
        self.model = model

    @property
    def config(self):
        path = f'{os.getcwd()}/config/{self.model}/product.yml'
        with open(path, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    @property
    def wait_condition(self):
        return self.config['wait']

    @property
    def wait_timeout(self):
        return self.config['timeout']

    def __build_method(self, browser, method_type):
        methods = {
            'class_name': browser.find_elements_by_class_name,
            'css_selector': browser.find_elements_by_css_selector
        }
        return methods[method_type]

    def parse_from_browser(self, browser):
        config = self.config
        elements = {}
        for field_name, field in config['fields'].items():
            get_property = self.__build_method(browser, field['type'])
            elements[field_name] = [el.text for el in get_property(field['key'])]
        
        products = []
        for i in range(len(elements['title'])):
            product = {}
            for prop in elements.keys():
                product[prop] = elements[prop][i]
            products.append(product)
        return products
    
    def format_products(self, data):
        df = pd.DataFrame(data)
        df['total_sales'] = [int(v.replace(' vendidos', '')) for v in df['total_sales']]
        df['price'] = [float(v.replace('R$', '').replace(',', '.')) for v in df['price']]
        return df
        