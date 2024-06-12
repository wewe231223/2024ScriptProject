from rest_apis import *
from region_code import *
import ApiFileIO
import os

trade_file_path = os.path.abspath('./Resources/trade_cache')+'\\'

query_params = {
    'serviceKey': "4PeRdvcpIuthF6GZYn7+TxeUSYDgoQEP1gaFkynbIdFTJkFRx2TFi67lwYUpDU4cC5YvATmAbjH9Z+mtPtt/BQ==",
    'pageNo': '1',
    'numOfRows': '1000',
    'LAWD_CD': '',
    'DEAL_YMD': ''
}

apartment_ex_api = ApiData(
    'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev',
    None,
    query_params,
    'item'
)

valid_apart_tags = ['거래금액', '거래유형', '건축년도', '년', '월', '일', '법정동', '지번', '아파트', '동', '층', '전용면적']


def get_apart_trade_data(sgg_code, ym):
    param_code = apartment_ex_api.get_param_value('LAWD_CD')
    param_ymd = apartment_ex_api.get_param_value('DEAL_YMD')
    dict_data = None
    trade_file_name = f'{sgg_code}{ym}.bin'

    if ApiFileIO.search_file(trade_file_path, trade_file_name):
        print(f'read binary file {trade_file_path+trade_file_name}')
        dict_data = ApiFileIO.read_binary_dict_in_list(trade_file_path+trade_file_name)
    else:
        if param_code == sgg_code and param_ymd == ym:
            dict_data = apartment_ex_api.get_data(tags=valid_apart_tags)
        else:
            dict_data = apartment_ex_api.get_new_data({'LAWD_CD': sgg_code, 'DEAL_YMD': ym}, get_data_all=True,
                                                      item_tag='', tags=valid_apart_tags)

        if dict_data:
            print(f'write new binary file {trade_file_path+trade_file_name}')
            ApiFileIO.write_binary_dict_in_list(trade_file_path+trade_file_name, dict_data)

    return dict_data


def get_apart_trade_data_search(sido_name, sgg_name, umd_name, y, m):
    code = sgg_codes[sido_name][sgg_name]
    m = str(m) if len(str(m)) != 1 else '0'+str(m)
    ym = str(y)+str(m)

    if len(ym) != 6:
        raise ValueError('년월 데이터가 6자리가 아닙니다.')

    dict_data = get_apart_trade_data(code, ym)

    rt_data = []
    for data in dict_data:
        if data['법정동'].strip(' ') == umd_name:
            rt_data.append(data)
    return rt_data


def get_valid_umd_names(dict_data):
    rt_names = set()
    for data in dict_data:
        rt_names.add(data['법정동'].strip(' '))
    return list(rt_names)


def get_apart_info(info_data):
    strings = []
    for dict_data in info_data:
        string = ''
        for k, v in dict_data.items():
            string += f'{k}: {v},  '
        strings.append(string)

    return strings