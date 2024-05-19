from rest_apis import *

url = "https://dapi.kakao.com/v2/local/search/address.xml"
headers = {'Authorization': 'KakaoAK 4183e7656b4d6b5d12da3a0eea9e6e20'}
query_params = {'query': '', 'analyze_type': 'exact'}

kakaomap_api = ApiData(
    url,
    headers,
    query_params,
    'address'
)


def kakaomap_search(road_name, tags=[]):
    kakaomap_api.get_new_data({'query': road_name})
    if not tags:
        return kakaomap_api.get_data()

    return kakaomap_api.get_data(tags)


def kakaomap_xy_search(road_name):
    kakaomap_api.get_new_data({'query': road_name})
    return kakaomap_api.get_data(['address_name', 'x', 'y'])


#test code
if __name__ == '__main__':
    from tkinter import *

    def address_locate_to_string(dict_data):
        string = ''
        for address, x, y in zip(*list(dict_data.values())):
            string += f'address: {address}\nx: {x}\ny: {y}\n'
        return string

    def search_road(_):
        global label, entry
        data = kakaomap_xy_search(entry.get())
        if not data:
            label['text'] = '일치하는 정보가 없습니다.'

        label['text'] = address_locate_to_string(data)


    window = Tk()
    window.title('카카오맵 테스트')
    window.geometry('800x600+100+100')

    label = Label(window, text='')
    label.pack()

    Label(window, text='도로명 주소를 입력해주세요 (도로명-지번)').place(x=300, y=600-100)
    entry = Entry(window)
    entry.bind('<Return>', search_road)
    entry.place(x=300, y=600-50)

    window.mainloop()
