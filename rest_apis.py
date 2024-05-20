import requests
import xml.etree.ElementTree as ElemTree
from urllib.parse import unquote
import re


class ApiData:
    def __init__(self, url, headers, query_params, item_tag, verify=True):
        if 'serviceKey' in query_params:
            query_params['serviceKey'] = unquote(query_params['serviceKey'])
        self.url = url
        self.root = None
        self.query_params = query_params
        self.headers = headers
        self.verify = verify

        self.extract_item_tag = item_tag
        self.data_tags = set()
        self.api_data = []
        self.elem_count = 0

    def change_url(self, new_url):
        self.url = new_url

    def get_response(self):
        response = requests.get(self.url, headers=self.headers, params=self.query_params)
        self.root = ElemTree.fromstring(response.text)

    def get_root_elem(self):
        return self.root

    def extract_data_root_child(self):
        for item in self.root.iter(self.extract_item_tag):
            dict_data = {}
            for elem in item:
                self.data_tags.add(elem.text)
                dict_data[elem.tag] = elem.text
            self.api_data.append(dict_data)

    def get_new_data(self, new_params, get_data_all=False, item_tag=''):
        self.api_data.clear()
        self.query_params['pageNo'] = '1'
        self.elem_count = 0

        for k, v in new_params.items():
            self.query_params[k] = v
        self.get_response()

        if item_tag != '':
            self.extract_item_tag = item_tag

        self.extract_data_root_child()
        self.elem_count = len(self.api_data)
        if get_data_all:
            total_count = 0
            elem_total_count = self.root.iter('totalCount')
            for elem in elem_total_count:
                total_count = int(elem.text)
            page = 1

            while self.elem_count < total_count:
                page += 1
                self.append_new_data({'pageNo': str(page)})

        return self.api_data

    def append_new_data(self, new_params, item_tag=''):
        for k, v in new_params.items():
            self.query_params[k] = v

        self.get_response()
        if item_tag != '':
            self.extract_item_tag = item_tag

        self.extract_data_root_child()
        self.elem_count = len(self.api_data)

        return self.api_data

    def dict_data_to_strings(self):
        strings = []
        for dict_data in self.api_data:
            string = ''
            for key, value in dict_data.items():
                if not key or not value:
                    continue

                value = re.sub(r"\s", "", value)
                string += f'{key} : {value}\n'
            strings.append(string)
        return strings

    def get_item_tags(self):
        return self.data_tags

    def get_data(self, tags=[]):
        if not self.api_data:
            self.get_response()
            self.extract_data_root_child()

        if not tags:
            return self.api_data

        rt_data = []
        for data in self.api_data:
            dict_data = {}
            for tag in tags:
                if tag not in data:
                    print(f'not tag in api data {tag}')
                    return []

                dict_data[tag] = data[tag]
            rt_data.append(dict_data)

        return rt_data

    def clear_data(self):
        self.api_data.clear()

    def get_elem_count(self):
        return self.elem_count
