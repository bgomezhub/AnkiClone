import customtkinter as ctk
from pages import Home


class Finish:
    def __init__(self, frame):
        # Title
        self.f_finish_title = ctk.CTkFrame(frame)
        self.f_finish_title.pack(pady=150, padx=150)
        ctk.CTkLabel(self.f_finish_title, text=f'Congratulations you finished!', font=('Arial', 30)).pack()
        # Type of Quiz
        self.f_finish_options = ctk.CTkFrame(frame)
        self.f_finish_options.pack(padx=200, pady=50)

        ctk.CTkButton(self.f_finish_options, text='Quiz', command=lambda: leave_page(frame)).grid(column=0, row=0)


def leave_page(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    return Home.Home(frame)
