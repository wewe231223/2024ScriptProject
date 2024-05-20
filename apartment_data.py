from rest_apis import *

query_params = {
    'serviceKey': "mCs5VgBMDTzgbM3a9ErIkLcJ/6Fg0gdBectxinG0WAlEH4LmwjKhuYZHTl0VpZ1AebN7P0D+96ltQ8zCXXoB+A==",
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
    return apartment_ex_api.get_data(['거래금액', '건축년도', '년', '월', '일', '아파트', '법정동', '지번', '층', '전용면적'])


def get_apart_info(info_data):
    strings = []
    for dict_data in info_data:
        string = ''
        for k, v in dict_data.items():
            string += f'{k}: {v},  '
        strings.append(string)

    return strings

#test code
if __name__ == '__main__':
    import csv
    from region_code import *

    def get_code_list(sido):
        high_region_code = sido_codes[sido]
        low_region_codes = get_sgg_codes(sido)
        names, codes = [], []
        for low_name, low_code in low_region_codes.items():
            names.append(sido+low_name)
            codes.append(high_region_code+low_code)

        return names, codes

    def write_apart_data_in_file(file, region_code, ym):
        dict_data = get_apart_trade_simple_data(region_code, ym)
        if not dict_data:
            return

        writer = csv.DictWriter(file, fieldnames=list(dict_data[0].keys()))
        writer.writeheader()
        writer.writerows(dict_data)

    def apartment_data_write(region_nm, region_code, filepath, start_y, start_m, end_y, end_m):
        file_name = filepath+region_nm+' 부동산실거래자료.csv'
        with open(file_name, 'w', encoding='utf-8-sig', newline='') as f:
            for y in range(start_y, end_y + 1):
                if y == start_y:
                    for m in range(start_m, 12 + 1):
                        write_apart_data_in_file(f, region_code, str(y)+str(m))
                elif y == end_y:
                    for m in range(1, end_m + 1):
                        write_apart_data_in_file(f, region_code, str(y)+str(m))
                else:
                    for m in range(1, 12 + 1):
                        write_apart_data_in_file(f, region_code, str(y)+str(m))

    def get_all_data(start_ym, end_ym, sido, row_code=None):
        dir_path = './부동산자료/'
        names, codes = get_code_list(sido)

        start_y, start_m = int(start_ym[:4]), int(start_ym[4:6])
        end_y, end_m = int(end_ym[:4]), int(end_ym[4:6])
        for name, code in zip(names, codes):
            apartment_data_write(name, code, dir_path, start_y, start_m, end_y, end_m)

    get_all_data('202010', '202404', '서울특별시')
