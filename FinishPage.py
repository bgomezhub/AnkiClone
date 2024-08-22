from tkinter import *

import Home


class FinishPage:
    def __init__(self, frame):
        # Title
        self.f_finish_title = Frame(frame)
        self.f_finish_title.pack(pady=150, padx=150)
        Label(self.f_finish_title, text=f'Congratulations you finished!', font=('Arial', 30)).pack()
        # Type of Quiz
        self.f_finish_options = Frame(frame)
        self.f_finish_options.pack(padx=200, pady=50)

        Button(self.f_finish_options, text='Quiz',
               command=lambda: self.leave_page(frame)).grid(column=0, row=0)

    def leave_page(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        return Home.Home(frame)
