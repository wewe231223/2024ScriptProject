import os.path
import time
from tkinter import *

import tkintermapview
from tkcalendar import DateEntry
from tkinter import ttk
from lotnum_to_roadnm import *
from apartment_data import *
from region_code import *

from tkintermapview import TkinterMapView


class MainGUI:
    def reset_button_colors(self):
        self.btn_search.config(bg='white', fg='black')
        self.btn_graph.config(bg='white', fg='black')
        self.btn_favorites.config(bg='white', fg='black')

    def search_apartments(self):
        self.reset_button_colors()
        self.btn_search.config(bg='red', fg='white')
        self.content_frame.tkraise()

    def show_graph(self):
        self.reset_button_colors()
        self.btn_graph.config(bg='red', fg='white')
        self.graph_frame.tkraise()

    def show_favorites(self):
        self.reset_button_colors()
        self.btn_favorites.config(bg='red', fg='white')

    def open_telegram(self):
        pass

    def send_email(self):
        pass

    def sido_invoke(self,event):
        sido = self.option_menu_sido.get()
        dict_data = get_sgg_codes(sido)
        if dict_data:
            self.region_code = sido_codes[sido]
            self.sgg_codes = dict_data
            self.local_option_sgg = self.local_option_sgg[:1]
            self.local_option_sgg += list(dict_data.keys())
            self.option_menu_sgg['values'] = self.local_option_sgg
            self.option_menu_sgg.set(self.local_option_sgg[0])

    def sgg_invoke(self,event):
        sido = self.option_menu_sido.get()
        sgg = self.option_menu_sgg.get()
        self.region_code += self.sgg_codes[sgg]
        dict_data = get_umd_codes(sido, sgg)

        # 읍면동 정보 불러오기 (없으면 dict_data == {})
        if dict_data:
            self.local_option_umd = self.local_option_umd[:1]
            self.local_option_umd += list(dict_data.keys())
            self.option_menu_umd['values'] = self.local_option_umd
            self.option_menu_umd.set(self.local_option_umd[0])

        self.listbox.delete(0,END)
        text = get_apart_info(get_apart_trade_simple_data(self.region_code, 202010))
        for t in text:
            self.listbox.insert(END,t)

    def umd_invoke(self,event):
        umd = self.option_menu_umd.get()

    def __init__(self):
        self.window = Tk()
        self.window.title("Apartment Search App")
        self.window.geometry("1920x1080")

        # 검색용 변수들
        self.region_code = ''
        self.sgg_codes = {}
        self.umd_codes = {}

        # 좌측 메뉴 프레임
        self.menu_frame = Frame(self.window, width=300, bg='white')
        self.menu_frame.grid(row=0, column=0, rowspan=3, sticky='nsew')

        # 로고 이미지
        self.logo_image = PhotoImage(file='Resources/Apartment.png')
        self.logo_label = Label(self.menu_frame, image=self.logo_image, bg='white')
        self.logo_label.pack(pady=10)

        # 메뉴 버튼들
        self.btn_search = Button(self.menu_frame, text="검색", bg='red', fg='white', command=self.search_apartments, height=5)
        self.btn_search.pack(fill='x')

        self.btn_graph = Button(self.menu_frame, text="그래프", bg='white', fg='black', command=self.show_graph, height=5)
        self.btn_graph.pack(fill='x')

        self.btn_favorites = Button(self.menu_frame, text="즐겨찾기", bg='white', fg='black', command=self.show_favorites, height=5)
        self.btn_favorites.pack(fill='x')

        # 우측 콘텐츠 프레임
        self.content_frame = Frame(self.window)
        self.content_frame.grid(row=0, column=1, rowspan=4, sticky='nsew')

        # 상단 검색 기능 프레임
        self.search_frame = Frame(self.content_frame,padx=10,pady=10)
        self.search_frame.pack(fill='x')

        # 지역으로 검색
        self.lbl_search = Label(self.search_frame, text="지역으로 검색")
        self.lbl_search.grid(row=0, column=0)

        self.local_option_sido = ['선택'] + list(sido_codes.keys())
        self.local_option_sgg = ['선택']
        self.local_option_umd = ['선택']

        self.option_menu_sido = ttk.Combobox(self.search_frame,values=self.local_option_sido,height=10, width=30)
        self.option_menu_sido.bind("<<ComboboxSelected>>", self.sido_invoke)
        self.option_menu_sido.grid(row=0, column=2)

        self.option_menu_sgg = ttk.Combobox(self.search_frame,values=self.local_option_sgg,height=10, width=30)
        self.option_menu_sgg.bind("<<ComboboxSelected>>", self.sgg_invoke)
        self.option_menu_sgg.grid(row=0, column=3)

        self.option_menu_umd = ttk.Combobox(self.search_frame, values=self.local_option_umd, height=10, width=30)
        self.option_menu_umd.bind("<<ComboboxSelected>>", self.umd_invoke)
        self.option_menu_umd.grid(row=0, column=4)


        # 정렬 기준
        self.lbl_sort = Label(self.search_frame, text="정렬 기준")
        self.lbl_sort.grid(row=1, column=0)

        self.sort_option = ['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option 5', 'Option 6']
        self.sort_option = ttk.Combobox(self.search_frame,values=self.sort_option,height=10, width=30)
        self.sort_option.grid(row=1, column=2)

        self.lbl_month = Label(self.search_frame, text="월별 거래일자")
        self.lbl_month.grid(row=2, column=0)

        self.date_entry = DateEntry(self.search_frame,date_pattern = 'y-mm-dd')
        self.date_entry.config(width=30)
        self.date_entry.grid(row=2, column=2)


        # 검색 결과 리스트박스와 스크롤바

        self.result_frame = Frame(self.content_frame)
        self.result_frame.pack(fill='both', expand=True)

        self.listbox = Listbox(self.result_frame)
        self.listbox.pack(side='left',fill='both', expand=True)

        self.scrollbar = Scrollbar(self.result_frame, orient='vertical',command=self.listbox.yview)
        self.scrollbar.pack(side='right',fill='y')
        self.listbox.config(yscrollcommand=self.scrollbar.set)



        self.graph_frame = Frame(self.window)
        self.graph_frame.grid(row=0,column=1,rowspan=3,sticky='nsew')






        self.content_frame.tkraise()

        self.right_button_frame = Frame(self.window ,width=300)
        self.right_button_frame.grid(row=0,column=2,rowspan=2,sticky='nsew',padx=30,pady=30)

        self.telegram_image = PhotoImage(file='Resources/Telegram.png')
        self.telegram_button = Button(self.right_button_frame,image=self.telegram_image,command=self.open_telegram)
        self.telegram_button.pack(padx=10)

        self.email_image = PhotoImage(file='Resources/Gmail.png')
        self.email_button = Button(self.right_button_frame,image=self.email_image,command=self.send_email)
        self.email_button.pack(padx=10)


        self.map = TkinterMapView(self.right_button_frame,width=800, height=600, corner_radius=0)

        self.map.set_position(37.3410721,126.7326877)
        self.map.pack(pady=10)


        # 위치 맞추기
        self.window.grid_rowconfigure(0,weight=1)
        self.window.grid_columnconfigure(1,weight=3)
        self.window.grid_columnconfigure(2,weight=2)



        self.window.mainloop()


if __name__ == "__main__":
    m = MainGUI()




