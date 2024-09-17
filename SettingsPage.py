import customtkinter as ctk


class SettingsPage:
    def __init__(self, frame):
        # Title
        self.f_title = ctk.CTkFrame(frame)
        self.f_title.pack(padx=200, pady=50)
        ctk.CTkLabel(self.f_title, text='Settings', font=('Arial', 40)).pack()
        # Type of Quiz
        self.f_home_options = ctk.CTkFrame(frame)
        self.f_home_options.pack(padx=200, pady=100)
        ctk.CTkButton(self.f_home_options, text='Back', font=('Arial', 18),
                      command=lambda: self.submission(frame, 'quiz')).grid(column=0, row=0)
        ctk.CTkButton(self.f_home_options, text='Done', font=('Arial', 18),
                      command=lambda: self.submission(frame, 'settings')).grid(column=0, row=0)

    def submission(self, frame, option):
        # destroy all objects of home page
        self.f_home_title.destroy()
        self.f_home_options.destroy()
        # initialize objects for appropriate option clicked
        if option == 'quiz':
            word_list = QuizManager.select_questions()
            QuizManager.next_question(frame, word_list)
        elif option == 'settings':
            SettingsPage.SettingsPage(frame)
