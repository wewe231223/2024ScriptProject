from rest_apis import *

query_params = {
    'serviceKey': "4PeRdvcpIuthF6GZYn7+TxeUSYDgoQEP1gaFkynbIdFTJkFRx2TFi67lwYUpDU4cC5YvATmAbjH9Z+mtPtt/BQ==",
    'pageNo': '1',
    'numOfRows': '1000',
    'LAWD_CD': '',
    'DEAL_YMD': ''
}

apartment_api = ApiData(
    'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev',
    query_params,
    'item'
    )

# test codes
if __name__ == '__main__':
    from tkinter import *

    data = apartment_api.get_data()
    test_strings = apartment_api.dict_data_to_strings()

    class GUI:
        def __init__(self):
            window = Tk()

            window.geometry('800x600+100+100')
            window.title('아파트 실거래 상세정보 API 테스트')
            texts = '첫번째 데이터만 표시합니다.\n\n' + test_strings[0]

            self.label = Label(window, text=texts)
            self.label.pack()
            self.entry = Entry(window)
            self.entry.bind('<Return>', self.change_query)
            self.entry.pack()

            window.mainloop()

        def change_query(self, n):
            global data, test_strings

            apartment_api.get_new_data('DEAL_YMD', self.entry.get())
            data = apartment_api.get_data()
            test_strings = apartment_api.dict_data_to_strings()

            texts = '첫번째 데이터만 표시합니다.\n\n' + test_strings[0]
            self.label['text'] = texts

            y = self.entry.get()[:4]
            m = self.entry.get()[4:6]
            # with open(f'{y}년 {m}월 거래정보.txt', 'w', encoding='utf8') as f:
            #     f.write(f'tatal count : {len(test_strings)}')
            #     for string in test_strings:
            #         f.write('--------------------------------------------------------\n')
            #         f.write(string)
    GUI()



