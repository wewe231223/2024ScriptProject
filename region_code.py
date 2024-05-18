from rest_apis import *

query_params = {
    'serviceKey': '4PeRdvcpIuthF6GZYn7%2BTxeUSYDgoQEP1gaFkynbIdFTJkFRx2TFi67lwYUpDU4cC5YvATmAbjH9Z%2BmtPtt%2FBQ%3D%3D',
    'pageNo': '1',
    'numOfRows': '1000',
    'type': 'xml',
    'locatadd_nm': ''
}

region_code_api = ApiData(
        'http://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList',
        query_params,
        'row'
    )

region_code_data = {}
dict_data = region_code_api.get_data(['region_cd', 'locatadd_nm'])
for values in zip(dict_data['region_cd'], dict_data['locatadd_nm']):
    sgg_list = list(values[1].split())
    if len(sgg_list) == 1:
        continue
    sgg = sgg_list[0] + sgg_list[1]
    region_code_data[sgg] = values[0][:5]
del dict_data
print(region_code_data)

# test codes
if __name__ == '__main__':
    from tkinter import *

    data = region_code_api.get_data()
    test_strings = region_code_api.dict_data_to_strings()

    class GUI:
        def __init__(self):
            window = Tk()

            window.geometry('800x600+100+100')
            window.title('아파트 실거래 상세정보 API 테스트')
            texts = '첫번째 데이터만 표시합니다.\n\n' + test_strings[0]

            self.label = Label(window, text=texts)
            self.label.pack()
            # self.entry = Entry(window)
            # self.entry.bind('<Return>', self.change_query)
            # self.entry.pack()

            window.mainloop()

        def change_query(self, n):
            global data, test_strings

            region_code_api.get_new_data('', self.entry.get())
            data = region_code_api.get_data()
            test_strings = region_code_api.dict_data_to_strings()

            texts = '첫번째 데이터만 표시합니다.\n\n' + test_strings[0]
            self.label['text'] = texts
            # with open(f'{y}년 {m}월 거래정보.txt', 'w', encoding='utf8') as f:
            #     f.write(f'tatal count : {len(test_strings)}')
            #     for string in test_strings:
            #         f.write('--------------------------------------------------------\n')
            #         f.write(string)
    GUI()

