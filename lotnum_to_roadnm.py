from rest_apis import *

query_params = {
    'confmKey': 'devU01TX0FVVEgyMDI0MDUxOTE0NDIxNjExNDc3NjE=',
    'currentPage': 1,
    'countPerPage': 10,
    'keyword': '',
    'resultType': 'xml',
    'hstryYn': 'Y',
    'firstSort': 'none',
    'addInfoYn': 'Y'
}

juso_api = ApiData(
    'https://business.juso.go.kr/addrlink/addrLinkApi.do',
    None,
    query_params,
    'juso'
)


def lotaddr_to_roadname(lot_addr):
    juso_api.get_new_data({'keyword': lot_addr})
    dict_data = juso_api.get_data(['roadAddr'])
    if not dict_data:
        return {}

    return dict_data[0]


def lotnum_to_roadname(umd, lot_num, building_nm):
    juso_api.get_new_data({'keyword': f'{umd} {lot_num} {building_nm}'})
    dict_data = juso_api.get_data(['roadAddr'])
    if not dict_data:
        return {}

    return dict_data[0]


#test code
if __name__ == '__main__':
    from tkinter import *

    def get_roadnm(_):
        global entry, label

        data = lotaddr_to_roadname(entry.get())

        if not data:
            return

        label['text'] = data['roadAddr']

    window = Tk()
    window.title('지번 주소 도로명 주소로 변환 테스트')
    window.geometry('350x300+100+100')

    label = Label(window, text='')
    label.pack()

    Label(window, text='지번과 건물명을 입력(ex: 72 경희궁의아침3단지\n'+
          'or: ').place(x=50, y=300-100)
    entry = Entry(window)
    entry.bind('<Return>', get_roadnm)
    entry.place(x=100, y=300-50)

    window.mainloop()

