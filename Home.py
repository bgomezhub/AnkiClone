import json

import customtkinter as ctk
import QuizManager
import SettingsPage


class Home:
    def __init__(self, frame):
        # Fonts
        font = QuizManager.get_fonts()
        self.font_title = ctk.CTkFont(family=font[0], size=font[1])
        self.font_body = ctk.CTkFont(family=font[0], size=font[2])
        # Title
        self.f_home_title = ctk.CTkFrame(frame)
        self.f_home_title.pack(padx=200, pady=90)
        ctk.CTkLabel(self.f_home_title, text='Welcome', font=self.font_title).pack()
        # Type of Quiz
        self.f_home_options = ctk.CTkFrame(frame)
        self.f_home_options.pack(padx=200, pady=90)
        button_size = self.font_body["family"], self.font_body["size"] + 10
        ctk.CTkButton(self.f_home_options, text='Quiz', font=button_size,
                      command=lambda: self.submission(frame, 'quiz')).grid(column=0, row=0, pady=12, sticky='EW')
        ctk.CTkButton(self.f_home_options, text='Word Lists', font=button_size,
                      command=lambda: self.submission(frame, 'quiz')).grid(column=0, row=1, pady=12, sticky='EW')
        ctk.CTkButton(self.f_home_options, text='Settings', font=button_size,
                      command=lambda: self.submission(frame, 'settings')).grid(column=0, row=2, pady=12, sticky='EW')

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
