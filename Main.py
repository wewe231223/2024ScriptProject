import ApiFileIO
import os.path
import time
from tkinter import *

import tkintermapview
from tkcalendar import DateEntry
from tkinter import ttk
from lotnum_to_roadnm import *
from apartment_data import *
from region_code import *
from kakao_api import *

from tkintermapview import TkinterMapView

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from PIL import Image, ImageTk
from tkinter import ttk

from tkinter import messagebox

from e_mail import mail

from Telegram import TelegramBot, run_telegram_bot
import multiprocessing
import webbrowser


favorite_path = os.path.abspath('./Resources')+'\\'
favorite_file = 'fav.bin'


class MainGUI:
    def reset_button_colors(self):
        self.btn_search.config(bg='white', fg='black')
        self.btn_graph.config(bg='white', fg='black')
        self.btn_favorites.config(bg='white', fg='black')

    def search_apartments(self):
        self.reset_button_colors()
        self.btn_search.config(bg='red', fg='white')
        self.window.bind("<MouseWheel>", lambda event: self.result_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
        if self.data_list:
            self.display_result(self.data_list)

        self.content_frame.tkraise()

    def show_graph(self):
        self.reset_button_colors()
        self.btn_graph.config(bg='red', fg='white')

        for value in self.favorite_buffer.values():
            self.favorite_database.append(value)
        self.favorite_buffer = {}

        if self.data_list:
            self.display_bar_graph(self.graph_canvas, self.data_list)
        self.graph_frame.tkraise()

    def show_favorites(self):
        self.reset_button_colors()
        self.btn_favorites.config(bg='red', fg='white')

        for value in self.favorite_buffer.values():
            self.favorite_database.append(value)
        self.favorite_buffer = {}

        if self.favorite_database:
            self.display_result(self.favorite_database, self.favorite_canvas)
            self.window.bind("<MouseWheel>",lambda event: self.favorite_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))


        self.favorite_frame.tkraise()

    def open_telegram(self):
        webbrowser.open("https://web.telegram.org")

    def send_email_content(self):
        result = []
        for dict_item in self.favorite_database:
            item_str = "\n".join([f"{key}: {value}" for key, value in dict_item.items()])
            result.append(item_str)
        for item in self.favorite_buffer.values():
            item_str = "\n".join([f"{key}: {value}" for key, value in item.items()])
            result.append(item_str)

        content = "\n---------------\n".join(result)

        mail(self.email_entry.get(), content)
        messagebox.showinfo("이메일 전송 성공","이메일 전송에 성공했습니다.")
        self.email_window.destroy()

    def send_email(self):
        if self.email_window is None or not self.email_window.winfo_exists():
            self.email_window = Toplevel(self.window)

            Label(self.email_window, text="즐겨찾기에 등록된 거래 기록을 입력한 메일로 전송하겠습니다.").pack()
            self.email_entry = Entry(self.email_window, width=30)
            self.email_entry.pack()

            send_button = Button(self.email_window, text="전송하기 ", command=self.send_email_content)
            send_button.pack()

    def get_ym(self):
        year_str = self.year_menu.get()[:-1]
        month_str = self.month_menu.get()[:-1]

        if year_str == '' or month_str == '':
            return "202405"

        if len(month_str) == 1:
            month_str = '0'+month_str

        return year_str + month_str

    def sido_invoke(self,event):
        sido = self.option_menu_sido.get()
        self.local_option_sgg = self.local_option_sgg[:1]
        self.local_option_sgg += get_sggs(sido)
        self.option_menu_sgg['values'] = self.local_option_sgg
        self.option_menu_sgg.set(self.local_option_sgg[0])

    def sgg_invoke(self,event):
        sido = self.option_menu_sido.get()
        sgg = self.option_menu_sgg.get()
        self.region_code = sgg_codes[sido][sgg]
        sgg_full_name = sido+' '+sgg

        self.cur_ym = self.get_ym()
        self.data_list = get_apart_trade_data(self.region_code, self.cur_ym)
        valid_names = get_valid_umd_names(self.data_list)
        self.local_option_umd = self.local_option_umd[:1]
        self.local_option_umd += valid_names
        self.option_menu_umd['values'] = self.local_option_umd
        self.option_menu_umd.set(self.local_option_umd[0])

    def mark_apart_location(self, data_list):
        self.map.delete_all_marker()

        keywords = set()
        for data in data_list:
            loc = f'{data["법정동"]} {data["지번"]} {data["아파트"]}'
            keywords.add(loc)
        keywords = list(keywords)

        p = multiprocessing.Pool(4)
        xy_list = p.map(kakaomap_xy_search, keywords, 4)
        xy_list = list(filter(lambda t: not t[0] is None, xy_list))

        for x, y, apart in xy_list:
            self.map.set_marker(y, x, apart)

    def search_umd_trade_data(self, umd):
        rt_data = []
        for data in self.data_list:
            if data['법정동'].strip() == umd:
                rt_data.append(data)

        return rt_data

    def umd_invoke(self,event):
        pass

    def search_invoke(self):
        sido = self.option_menu_sido.get()
        sgg = self.option_menu_sgg.get()
        umd = self.option_menu_umd.get()

        self.result_canvas.delete('all')
        self.data_list = self.search_umd_trade_data(umd)

        self.mark_apart_location(self.data_list)

        umd_x, umd_y, _ = kakaomap_xy_search(sido + ' ' + sgg + ' ' + umd)
        self.map.set_position(umd_y, umd_x)

        for value in self.favorite_buffer.values():
            self.favorite_database.append(value)

        self.favorite_buffer = {}
        self.display_result(data=self.data_list)

    def favorite_invoke(self, index):
        if self.favorite_buttons[index].cget('text') == '즐겨찾기에 등록됨':
            self.favorite_buttons[index].config(text=f'즐겨찾기에 등록 : {self.favorite_buffer[index]["아파트"]} {self.favorite_buffer[index]["거래금액"]}',bg='white')
            del self.favorite_buffer[index]
        else:
            self.favorite_buttons[index].config(text='즐겨찾기에 등록됨',bg='yellow')
            self.favorite_buffer[index] = self.data_list[index]

    def favorite_remove(self, index):
        self.favorite_buttons[index].destroy()
        del self.favorite_database[index]
        self.display_result(self.favorite_database, self.favorite_canvas)

    def sort_invoke(self, event):
        match self.sort_option.get():
            case '거래 금액 순':
                sorted_by_price = sorted(self.data_list, key=lambda x: int(x['거래금액'].replace(" ","").replace(",","")))
                self.display_result(sorted_by_price)

            case '거래일 순':
                sorted_by_date = sorted(self.data_list, key=lambda x: int(x['일']))
                self.display_result(sorted_by_date)

            case '전용 면적 순':
                sorted_by_area = sorted(self.data_list, key=lambda x: float(x['전용면적']))
                self.display_result(sorted_by_area)
            case '건축 년도 순':
                sorted_by_year = sorted(self.data_list, key=lambda x: int(x['건축년도']))
                self.display_result(sorted_by_year)
            case _:
                raise Exception("Something went wrong")

    def display_result(self,data,canvas = None):
        if len(self.favorite_buttons) > 0:
            for button in self.favorite_buttons:
                button.destroy()

        self.favorite_buttons = []

        if canvas is None:
            self.result_canvas.delete('all')
            for data_id, data in enumerate(data):
                b = None
                if data in self.favorite_database:
                    b = Button(self.result_canvas, text='즐겨찾기에 등록됨', bg='yellow')
                else :
                    b = Button(self.result_canvas, text=f'즐겨찾기에 등록 : {data["아파트"]} {data["거래금액"]}',command=lambda index=data_id: self.favorite_invoke(index))
                self.result_canvas.create_window(400,100 + 700 * data_id, window=b)
                self.favorite_buttons.append(b)

                for line, (key, value) in enumerate(data.items()):
                    self.result_canvas.create_text(0, 100 + (30 * line) + 700 * data_id, text=f'{key}: {value}',font=('Arial', 20), anchor='w')

            self.result_canvas.configure(scrollregion=self.result_canvas.bbox('all'))
        else:
            canvas.delete('all')
            for data_id, data in enumerate(data):
                b = Button(canvas, text=f'등록 해제 : {data["아파트"]} {data["거래금액"]}', bg='yellow',
                           command=lambda index=data_id: self.favorite_remove(index))
                canvas.create_window(400, 100 + 700 * data_id, window=b)
                self.favorite_buttons.append(b)

                for line, (key, value) in enumerate(data.items()):
                    canvas.create_text(0, 100 + (30 * line) + 700 * data_id, text=f'{key}: {value}',font=('Arial', 20), anchor='w')

            canvas.configure(scrollregion= canvas.bbox('all'))

    def display_bar_graph(self,canvas,data_list):
        # 데이터 리스트에서 아파트 이름과 거래금액을 추출
        apartments = [data['아파트'] for data in data_list]
        prices = [int(data['거래금액'].replace(',', '')) for data in data_list]  # 거래금액을 정수로 변환

        if self.graph_ax:
            self.graph_ax.clear()
        else:
            self.graph_ax = self.graph_figure.add_subplot(111)
        plt.rcParams['font.family'] = 'Malgun Gothic'


        self.graph_ax.bar(apartments, prices)
        self.graph_ax.set_xlabel('아파트')
        self.graph_ax.set_ylabel('거래금액')
        self.graph_ax.set_title('아파트별 거래금액')

        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    def update(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.clock_lab.config(text=current_time)
        self.window.after(1000, self.update)

    def __init__(self):
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.after(1000, self.update)
        self.window.title("Apartment Search App")
        self.window.geometry("1200x800")


        self.telegram_process = multiprocessing.Process(target= run_telegram_bot)
        self.telegram_process.start()

        # 검색용 변수들
        self.region_code = ''
        self.cur_ym = ''
        self.sgg_codes = {}
        self.umd_codes = {}

        # 좌측 메뉴 프레임
        self.menu_frame = Frame(self.window, width=100, bg='white')
        self.menu_frame.grid(row=0, column=0, rowspan=3, sticky='nsew')

        # 로고 이미지
        self.logo_image = PhotoImage(file='Resources/Apartment.png')
        self.logo_label = Label(self.menu_frame, image=self.logo_image, bg='white',width=100,height=100)
        self.logo_label.pack()

        # 메뉴 버튼들
        self.btn_search = Button(self.menu_frame, text="검색", bg='red', fg='white', command=self.search_apartments, height=5)
        self.btn_search.pack(fill='x')

        self.btn_graph = Button(self.menu_frame, text="그래프", bg='white', fg='black', command=self.show_graph, height=5)
        self.btn_graph.pack(fill='x')

        self.btn_favorites = Button(self.menu_frame, text="즐겨찾기", bg='white', fg='black', command=self.show_favorites, height=5)
        self.btn_favorites.pack(fill='x')


        self.data_list = []

        self.favorite_buttons = []
        self.favorite_buffer = {}
        self.favorite_database = []
        if ApiFileIO.search_file(favorite_path, favorite_file):
            self.favorite_database = ApiFileIO.read_binary_dict_in_list(favorite_path+favorite_file)

        # 우측 콘텐츠 프레임
        self.content_frame = Frame(self.window)
        self.content_frame.grid(row=0, column=1, rowspan=4, sticky='nsew')

        # 상단 검색 기능 프레임
        self.search_frame = Frame(self.content_frame,padx=10,pady=10)
        self.search_frame.pack(fill='x')

        # 지역으로 검색
        self.lbl_search = Label(self.search_frame, text="지역으로 검색")
        self.lbl_search.grid(row=0, column=0)

        self.local_option_sido = ['선택'] + get_sidos()
        self.local_option_sgg = ['선택']
        self.local_option_umd = ['선택']

        self.option_menu_sido = ttk.Combobox(self.search_frame,values=self.local_option_sido)
        self.option_menu_sido.bind("<<ComboboxSelected>>", self.sido_invoke)
        self.option_menu_sido.grid(row=0, column=1)

        self.option_menu_sgg = ttk.Combobox(self.search_frame,values=self.local_option_sgg)
        self.option_menu_sgg.bind("<<ComboboxSelected>>", self.sgg_invoke)
        self.option_menu_sgg.grid(row=0, column=2)

        self.option_menu_umd = ttk.Combobox(self.search_frame, values=self.local_option_umd)
        self.option_menu_umd.bind("<<ComboboxSelected>>", self.umd_invoke)
        self.option_menu_umd.grid(row=0, column=3)

        image = Image.open("Resources/Search.png")
        image = image.resize((20,20),Image.LANCZOS)
        self.search_image = ImageTk.PhotoImage(image)
        self.search_button = Button(self.search_frame, image= self.search_image,width=20,height=20,command=self.search_invoke)
        self.search_button.grid(row=0, column=4)

        # 정렬 기준
        self.lbl_sort = Label(self.search_frame, text="정렬 기준")
        self.lbl_sort.grid(row=1, column=0)

        self.sort_option = ['거래 금액 순', '거래일 순', '전용 면적 순', '건축 년도 순']
        self.sort_option = ttk.Combobox(self.search_frame,values=self.sort_option)
        self.sort_option.bind("<<ComboboxSelected>>", self.sort_invoke)
        self.sort_option.grid(row=1, column=1)

        self.lbl_month = Label(self.search_frame, text="월별 거래일자")
        self.lbl_month.grid(row=2, column=0)


        self.year_menu = ttk.Combobox(self.search_frame, values = [f'{year}년' for year in range(2006,2024+1)])
        self.year_menu.grid(row=2, column=1)
        self.year_menu.set("년도를 선택하세요")

        self.month_menu = ttk.Combobox(self.search_frame, values=[f'{month}월' for month in range(1,13)])
        self.month_menu.grid(row=2, column=2)
        self.month_menu.set("월을 선택하세요")


        # 검색 결과 리스트박스와 스크롤바

        self.result_frame = Frame(self.content_frame)
        self.result_frame.pack(fill='both',expand=True)


        self.result_canvas = Canvas(self.result_frame,bg='white',width=100,height=100)
        self.result_canvas.pack(side=LEFT, fill='both', expand=True)

        self.result_vertical_scrollbar = Scrollbar(self.result_canvas,orient='vertical',command=self.result_canvas.yview)
        self.result_vertical_scrollbar.pack(side='right', fill='y')
        self.window.bind("<MouseWheel>", lambda event: self.result_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        self.result_canvas.configure(yscrollcommand=self.result_vertical_scrollbar.set)


        self.favorite_frame = Frame(self.window)
        self.favorite_frame.grid(row=0, column=1, rowspan=4, sticky='nsew')
        self.favorite_canvas = Canvas(self.favorite_frame, bg='white', width=100, height=100)
        self.favorite_canvas.pack(side=LEFT, fill='both', expand=True)

        self.favorite_vertical_scrollbar = Scrollbar(self.favorite_canvas, orient='vertical', command=self.favorite_canvas.yview)
        self.favorite_vertical_scrollbar.pack(side='right', fill='y')

        self.favorite_canvas.configure(yscrollcommand=self.favorite_vertical_scrollbar.set)

        self.graph_frame = Frame(self.window)
        self.graph_frame.grid(row=0, column=1, rowspan=4, sticky='nsew')

        self.graph_figure = plt.Figure(figsize=(10, 10), dpi=100)
        self.graph_canvas = FigureCanvasTkAgg(self.graph_figure, master=self.graph_frame)
        self.graph_ax = None
        plt.rcParams['font.family'] = 'Malgun Gothic'



        self.content_frame.tkraise()

        self.right_button_frame = Frame(self.window ,width=300)
        self.right_button_frame.grid(row=0,column=3,rowspan=2,sticky='nsew',padx=30,pady=30)

        self.clock_lab = Label(self.right_button_frame, font=('Malgun Gothic', 20, 'bold'), bg='white')
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.clock_lab.config(bg=self.window.cget('bg'))
        self.clock_lab.config(text=current_time)
        self.clock_lab.pack()

        self.telegram_image = PhotoImage(file='Resources/Telegram.png')
        self.telegram_button = Button(self.right_button_frame,image=self.telegram_image,command=self.open_telegram)
        self.telegram_button.pack(padx=10)

        self.email_image = PhotoImage(file='Resources/Gmail.png')
        self.email_button = Button(self.right_button_frame,image=self.email_image,command=self.send_email)
        self.email_button.pack(padx=10)

        self.email_window = None

        self.map = TkinterMapView(self.right_button_frame,width=400, height=500, corner_radius=0)
        self.map.set_position(37.3410721,126.7326877)
        self.map.pack(pady=10)

        # 위치 맞추기
        self.window.grid_rowconfigure(0,weight=1)
        self.window.grid_columnconfigure(1,weight=3)
        self.window.grid_columnconfigure(2,weight=2)

        self.window.mainloop()

    def on_close(self):
        if self.telegram_process.is_alive():
            self.telegram_process.terminate()
            self.telegram_process.join()

        ApiFileIO.write_binary_dict_in_list(favorite_path+favorite_file, self.favorite_database)

        if self.window:
            self.window.destroy()

if __name__ == "__main__":
    m = MainGUI()




