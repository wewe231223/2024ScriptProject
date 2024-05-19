from rest_apis import *

query_params = {
    'serviceKey': "4PeRdvcpIuthF6GZYn7+TxeUSYDgoQEP1gaFkynbIdFTJkFRx2TFi67lwYUpDU4cC5YvATmAbjH9Z+mtPtt/BQ==",
    'pageNo': '1',
    'numOfRows': '1000',
    'LAWD_CD': '11110',
    'DEAL_YMD': '202010'
}

apartment_api = ApiData(
    'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev',
    None,
    query_params,
    'item'
)

lst = apartment_api.get_data(['도로명', '아파트', '도로명건물본번호코드'])
for d, c, a in zip(lst['도로명'], lst['도로명건물본번호코드'], lst['아파트']):
    print(f'{d}-{int(c)} {a}')
