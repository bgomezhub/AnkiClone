from tkinter import *

import ConjugationQuizPage


class Home:
    def __init__(self, frame):
        # Title
        f_home_title = Frame(frame)
        f_home_title.pack(padx=200, pady=50)
        Label(f_home_title, text='Welcome', font=('Arial', 30)).pack()
        # Type of Quiz
        f_home_options = Frame(frame)
        f_home_options.pack(padx=200, pady=50)
        Button(f_home_options, text='Conjugations',
               command=lambda: self.submission([f_home_title, f_home_options, frame])).grid(column=0, row=0)

    def submission(self, frames):
        # destroy all objects of home page
        frames[0].destroy()
        frames[1].destroy()
        # initialize objects for appropriate option clicked
        ConjugationQuizPage.ConjugationQuizPage(frames[2])
