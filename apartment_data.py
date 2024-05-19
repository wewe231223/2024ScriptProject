from rest_apis import *

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


def get_apart_trade_simple_data(sgg_code, ym):
    apartment_ex_api.get_new_data({'LAWD_CD': sgg_code, 'DEAL_YMD': ym})
    return apartment_ex_api.get_data(['거래금액', '건축년도', '년', '월', '일', '아파트', '지번'])


def get_apart_info(info_data):
    key_lst = list(info_data.keys())
    value_lst = list(info_data.values())

    strings = []
    for i in range(len(value_lst[0])):
        string = ''
        for j in range(len(key_lst)):
            string += f'{key_lst[j]}: {value_lst[j][i]}\n'
        strings.append(string)

    return strings


#test code
if __name__ == '__main__':
    strings = get_apart_info(get_apart_trade_simple_data(11110, 202010))
    for string in strings:
        print('-------------------------------------------')
        print(string)
