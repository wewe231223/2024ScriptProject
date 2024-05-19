from rest_apis import *

url = "https://dapi.kakao.com/v2/local/search/address.xml"
headers = {'Authorization': 'KakaoAK 4183e7656b4d6b5d12da3a0eea9e6e20'}
query_params = {'query': '사직로8길-4', 'analyze_type': 'exact'}

kakaomap_api = ApiData(
    url,
    headers,
    query_params,
    'address'
)

print(kakaomap_api.get_data())