from tkinter import Tk, Canvas, Scrollbar

# Tkinter 윈도우를 생성합니다.
window = Tk()

# Canvas와 Scrollbar를 생성하고 배치합니다.
canvas = Canvas(window, bg='white', width=400, height=400)
canvas.pack(side='left', fill='both', expand=True)

scrollbar = Scrollbar(window, command=canvas.yview)
scrollbar.pack(side='left', fill='y')

# Canvas의 스크롤 명령을 Scrollbar에 연결합니다.
canvas.configure(yscrollcommand=scrollbar.set)

# Canvas에 몇 가지 아이템을 추가합니다.
for i in range(20):
    canvas.create_text(200, 50 + i*100, text=f"Item {i+1}", font=("Arial", 20))

# Canvas의 스크롤 영역을 업데이트합니다.
canvas.configure(scrollregion=canvas.bbox('all'))

# Tkinter 이벤트 루프를 시작합니다.
window.mainloop()