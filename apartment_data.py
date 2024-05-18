from rest_apis import *

query_params = {
    'serviceKey': "4PeRdvcpIuthF6GZYn7+TxeUSYDgoQEP1gaFkynbIdFTJkFRx2TFi67lwYUpDU4cC5YvATmAbjH9Z+mtPtt/BQ==",
    'pageNo': '1',
    'numOfRows': '1000',
    'LAWD_CD': '11110',
    'DEAL_YMD': ''
}

apartment_api = ApiData(
    'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev',
    query_params,
    'item'
    )
