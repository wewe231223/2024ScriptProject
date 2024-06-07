from rest_apis import *
from region_code import *

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
    if param_code == sgg_code and param_ymd == ym:
        dict_data = apartment_ex_api.get_data(tags=valid_apart_tags)
    else:
        dict_data = apartment_ex_api.get_new_data({'LAWD_CD': sgg_code, 'DEAL_YMD': ym}, get_data_all=True,
                                                  item_tag='', tags=valid_apart_tags)

    return dict_data

def get_apart_trade_data_search(sido_name, sgg_name, umd_name, y, m):
    new_params = { 'LAWD_CD': None, 'DEAL_YMD': None }
    code = sgg_codes[sido_name][sgg_name]
    new_params['LAWD_CD'] = code
    m = str(m) if len(str(m)) != 1 else '0'+str(m)
    ym = str(y)+str(m)

    if len(ym) != 6:
        raise ValueError('년월 데이터가 6자리가 아닙니다.')

    new_params['DEAL_YMD'] = ym
    dict_data = apartment_ex_api.get_new_data(new_params=new_params, get_data_all=True, item_tag='', tags=valid_apart_tags)

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


print(get_apart_trade_data_search('서울특별시', '종로구', '사직동', 2024, 2))
print(get_apart_trade_data_search('서울특별시', '종로구', '사직동', '2024', '05'))