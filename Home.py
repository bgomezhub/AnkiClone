from tkinter import *

import ConjugationQuizPage
import NounQuizPage
import AdjectivesQuizPage
import QuizManager


class Home:
    def __init__(self, frame):
        # Title
        self.f_home_title = Frame(frame)
        self.f_home_title.pack(padx=200, pady=100)
        Label(self.f_home_title, text='Welcome', font=('Arial', 30)).pack()
        # Type of Quiz
        self.f_home_options = Frame(frame)
        self.f_home_options.pack(padx=200, pady=100)
        Button(self.f_home_options, text='Quiz',
               command=lambda: self.submission(frame, 'quiz')).grid(column=0, row=0)

    def submission(self, frame, option):
        # destroy all objects of home page
        self.f_home_title.destroy()
        self.f_home_options.destroy()
        # initialize objects for appropriate option clicked
        if option == 'quiz':
            word_list = QuizManager.select_questions()
            QuizManager.next_question(frame, word_list)
