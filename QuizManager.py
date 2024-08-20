from tkinter import *
import sqlite3
import random
import datetime

import ConjugationQuizPage
import NounQuizPage
import AdjectivesQuizPage

class QuizManger:
    def __init__(self, frame):
        self.quiz_list = []
        self.new_words_limit = 5

        # Prepare Questions
        self.select_questions()

        # Send to page corresponding to word
        word = self.quiz_list[random.randint(0, len(self.quiz_list) - 1)]
        if word[1] == 'present_verb':
            ConjugationQuizPage.ConjugationQuizPage(frame, word)
        elif word[1] == 'noun':
            NounQuizPage.NounQuizPage(frame, word)
        elif word[1] == 'adjective':
            AdjectivesQuizPage.AdjectivesQuizPage(frame, word)

    def select_questions(self):
        # Select all in a list
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()

        # Select new words
        c.execute("SELECT * FROM word_info WHERE new = 1")
        # Add new words to quiz list
        self.quiz_list = c.fetchmany(self.new_words_limit)

        # Select due words
        c.execute(f"Select * FROM word_info WHERE cooldown <= {datetime.datetime.now().strftime('%Y%m%d')}")
        self.quiz_list += c.fetchall()

