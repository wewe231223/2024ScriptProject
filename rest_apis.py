import requests
import xml.etree.ElementTree as ElemTree

#병원정보 서비스 예제
url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
# 공공데이터포털에서 발급받은 디코딩되지 않은 인증키 입력
service_key = "4PeRdvcpIuthF6GZYn7+TxeUSYDgoQEP1gaFkynbIdFTJkFRx2TFi67lwYUpDU4cC5YvATmAbjH9Z+mtPtt/BQ=="
query_params = {'serviceKey': service_key, 'pageNo': '1', 'numOfRows': '10', 'LAWD_CD': '11110', 'DEAL_YMD': '202004'}

response = requests.get(url, params=query_params)
root = ElemTree.fromstring(response.text)

api_tags = []
api_data = {}

for item in root.iter('item'):
    for texts in item:
        api_tags = texts.tag
        api_data[texts.tag] = texts.text

for key, value in api_data.items():
    print(f'{key}: {value}')