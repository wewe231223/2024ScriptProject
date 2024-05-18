from rest_apis import *

query_params = {
    'serviceKey': '4PeRdvcpIuthF6GZYn7%2BTxeUSYDgoQEP1gaFkynbIdFTJkFRx2TFi67lwYUpDU4cC5YvATmAbjH9Z%2BmtPtt%2FBQ%3D%3D',
    'pageNo': '1',
    'numOfRows': '',
    'type': 'xml',
    'locatadd_nm': ''
}

region_code_api = ApiData(
        'http://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList',
        query_params,
        'row'
    )

sido = {
    '서울특별시': '11',
    '부산광역시': '21',
    '대구광역시': '22',
    '인천광역시': '23',
    '광주광역시': '24',
    '대전광역시': '25',
    '울산광역시': '26',
    '세종특별자치시': '29',
    '경기도': '31',
    '강원특별자치도': '32',
    '충청북도': '33',
    '충청남도': '34',
    '전라북도': '35',
    '전라남도': '36',
    '경상북도': '37',
    '경상남도': '38',
    '제주특별자치도': '39'
}


def get_sgg_codes(sido_str):
    if sido_str not in sido:
        print('not exist sido_cd')
        return {}

    region_code_api.get_new_data({'numOfRows': '1000', 'locatadd_nm': sido_str}, True)
    region_data = region_code_api.get_data(['locatadd_nm', 'sgg_cd'])
    sgg_codes = {}
    for locate_name, sgg_cd in zip(region_data['locatadd_nm'], region_data['sgg_cd']):
        split_names = list(locate_name.split())
        if len(split_names) < 2:
            continue

        locate_name = split_names[1]
        sgg_codes[locate_name] = sgg_cd

    region_code_api.clear_data()
    return sgg_codes


def get_umd_codes(sido_str, sgg_str):
    if sido_str not in sido:
        return {}

    region_code_api.get_new_data({'numOfRows': '1000', 'locatadd_nm': sido_str+' '+sgg_str}, True)
    region_data = region_code_api.get_data(['locatadd_nm', 'umd_cd'])

    umd_codes = {}
    for locate_name, sgg_cd in zip(region_data['locatadd_nm'], region_data['umd_cd']):
        split_names = list(locate_name.split())
        if len(split_names) < 3:
            continue

        locate_name = split_names[2]
        umd_codes[locate_name] = sgg_cd

    region_code_api.clear_data()
    return umd_codes


def get_ri_codes(sido_str, sgg_str, umd_str):
    if sido_str not in sido:
        return {}

    region_code_api.get_new_data({'numOfRows': '1000',
                                  'locatadd_nm': sido_str + ' ' + sgg_str+' '+umd_str},
                                 True)
    region_data = region_code_api.get_data(['locatadd_nm', 'ri_cd'])
    ri_codes = {}
    for locate_name, sgg_cd in zip(region_data['locatadd_nm'], region_data['ri_cd']):
        split_names = list(locate_name.split())
        if len(split_names) < 4:
            continue

        locate_name = split_names[3]
        ri_codes[locate_name] = sgg_cd

    region_code_api.clear_data()
    return ri_codes

# print(get_sgg_codes('강원특별자치도'))
# print(get_umd_codes('강원특별자치도', '동해시'))


# test_code
if __name__ == '__main__':
    from tkinter import *

    def dict_code_to_string(dic):
        new_line_cnt = 2
        if len(dic) >= 100:
            new_line_cnt = 3

        string = ''
        cnt = 0
        for k, v in dic.items():
            if cnt % new_line_cnt == 0:
                string += '\n'
            string += f'{k} : 코드 [{v}]  '
            cnt += 1
        return string

    def entry_sido(_):
        global e1, sido_str, label
        sido_str = e1.get()
        dict_data = get_sgg_codes(sido_str)
        if not dict_data:
            sido_str = ''
            label['text'] = '그런 시/도는 없습니다.'
            return

        label['text'] = '시/도 데이터 목록\n' + dict_code_to_string(dict_data)


    def entry_sgg(_):
        global e2, sido_str, sgg_str, label
        if sido_str == '':
            label['text'] = '시/도를 먼저 입력해주세요'
            return

        sgg_str = e2.get()
        dict_data = get_umd_codes(sido_str, sgg_str)
        if not dict_data:
            sgg_str = ''
            label['text'] = '그런 시군구는 없습니다.'
            return

        label['text'] = '시군구 데이터 목록\n' + dict_code_to_string(dict_data)

    def entry_umd(_):
        global e3, sido_str, sgg_str, label
        if sido_str == '' or sgg_str == '':
            label['text'] = '시/도 와 시군구를 먼저 입력해주세요'
            return

        umd_str = e3.get()
        dict_data = get_ri_codes(sido_str, sgg_str, umd_str)
        if not dict_data:
            label['text'] = '그런 읍면동은 없습니다.'
            return

        label['text'] = 'XX리 데이터 목록\n' + dict_code_to_string(dict_data)

    window = Tk()
    window.geometry(f'800x600+100+100')
    window.title('시군구, 읍면동 데이터 테스트')

    label = Label(window, text='')
    label.pack()

    Label(window, text='시(특별시/광역시)/도 입력').place(x=50, y=600-100)
    e1 = Entry(window)
    e1.bind('<Return>', entry_sido)
    e1.place(x=50, y=600-50)

    sido_str = ''
    Label(window, text='시군구 입력').place(x=250, y=600-100)
    e2 = Entry(window)
    e2.bind('<Return>', entry_sgg)
    e2.place(x=250, y=600-50)

    sgg_str = ''
    Label(window, text='읍면동 입력').place(x=450, y=600-100)
    e3 = Entry(window)
    e3.bind('<Return>', entry_umd)
    e3.place(x=450, y=600 - 50)

    window.mainloop()
