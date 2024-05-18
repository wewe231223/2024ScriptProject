import requests
import xml.etree.ElementTree as ElemTree
from urllib.parse import unquote
import re

class ApiData:
    def __init__(self, url, query_params, item_tag, verify=True):
        query_params['serviceKey'] = unquote(query_params['serviceKey'])
        response = requests.get(url, params=query_params, verify=verify)
        self.url = url
        self.root = ElemTree.fromstring(response.text)
        self.query_params = query_params

        self.extract_item_tag = item_tag
        self.data_tags = set()
        self.api_data = []
        self.extract_data_root_child()

    def extract_data_root_child(self):
        for item in self.root.iter(self.extract_item_tag):
            dict_data = {}
            for elem in item:
                self.data_tags.add(elem.text)
                dict_data[elem.tag] = elem.text
            self.api_data.append(dict_data)

    def get_new_data(self, param_tag, new_param_data, item_tag=''):
        self.query_params[param_tag] = new_param_data
        response = requests.get(self.url, params=self.query_params)
        self.root = ElemTree.fromstring(response.text)
        if item_tag != '':
            self.extract_item_tag = item_tag

        self.api_data.clear()
        self.extract_data_root_child()

    def append_new_data(self, param_tag, new_param_data, item_tag=''):
        self.query_params[param_tag] = new_param_data
        response = requests.get(self.url, params=self.query_params)
        self.root = ElemTree.fromstring(response.text)
        if item_tag != '':
            self.extract_item_tag = item_tag

        self.extract_data_root_child()

    def dict_data_to_strings(self):
        strings = []
        for dict_data in self.api_data:
            string = ''
            for key, value in dict_data.items():
                if not key or not value:
                    continue

                value_remove_all = re.sub(r"\s", "", value)
                if value_remove_all != '':
                    string += f'{key} : {value}\n'
            strings.append(string)
        return strings

    def get_item_tags(self):
        return self.data_tags

    def get_data(self, tags=[], type_func=None):
        if not tags:
            return self.api_data

        rt_data = {}
        for tag in tags:
            rt_data[tag] = []
            for data in self.api_data:
                if type_func:
                    rt_data[tag].append(type_func(data[tag]))
                else:
                    rt_data[tag].append(data[tag])
        print(rt_data)
        return rt_data
