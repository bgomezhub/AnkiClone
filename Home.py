from tkinter import *

import ConjugationQuizPage
import NounQuizPage
import AdjectivesQuizPage


class Home:
    def __init__(self, frame):
        # Title
        self.f_home_title = Frame(frame)
        self.f_home_title.pack(padx=200, pady=50)
        Label(self.f_home_title, text='Welcome', font=('Arial', 30)).pack()
        # Type of Quiz
        self.f_home_options = Frame(frame)
        self.f_home_options.pack(padx=200, pady=50)
        Button(self.f_home_options, text='Conjugations',
               command=lambda: self.submission(frame, 'con')).grid(column=0, row=0)
        Button(self.f_home_options, text='Nouns',
               command=lambda: self.submission(frame, 'nouns')).grid(column=1, row=0)
        Button(self.f_home_options, text='Adjectives',
               command=lambda: self.submission(frame, 'adjs')).grid(column=2, row=0)

    def submission(self, frame, option):
        # destroy all objects of home page
        self.f_home_title.destroy()
        self.f_home_options.destroy()
        # initialize objects for appropriate option clicked
        if option == 'con':
            ConjugationQuizPage.ConjugationQuizPage(frame)
        elif option == 'nouns':
            NounQuizPage.NounQuizPage(frame)
        elif option == 'adjs':
            AdjectivesQuizPage.AdjectivesQuizPage(frame)
