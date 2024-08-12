import random
import sqlite3
from tkinter import *
from math import floor


class ConjugationQuizPage:
    def __init__(self, frame):
        # Table Frame
        self.f_conjugation_table = Frame(frame)
        self.f_conjugation_table.grid(column=0, row=0, padx=200, pady=150)

        # conjugation
        self.conjugation = []
        self.select_conjugation()

        # Define & Display conjugation table
        self.conjugation_table = []
        self.define_conjugation_table(self.f_conjugation_table)

        # Submission
        self.submit = Button(
            self.f_conjugation_table, text="Submit", command=lambda: self.submission())
        self.submit.grid(column=0, row=8, columnspan=2, sticky='S', pady=20)  # Padding between table & button

    def define_conjugation_table(self, frame):
        # Define conjugation
        self.conjugation_table.append(Label(frame, text=self.conjugation[0]))
        self.conjugation_table[0].grid(column=0, row=0)
        # Build table
        con_subjects = ['Je', 'Tu', 'Il/Elle', 'Nous', 'Vous', 'Ils/Elles']
        for num in range(1, 14):
            if num % 2 == 0:
                self.conjugation_table.append(Label(frame, text=con_subjects[num//2 - 1], pady=8, padx=25))
                self.conjugation_table[num].grid(column=0, row=num//2)
            else:
                self.conjugation_table.append(Entry(frame))
                self.conjugation_table[num].grid(column=1, row=num//2)

    def select_conjugation(self):
        # Select all in a list
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Select Table
        c.execute("SELECT * FROM present_verb")
        db_table = c.fetchall()
        # Choose random number & assign to conjugation
        self.conjugation = db_table[random.randint(0, len(db_table) - 1)]

    # Submit entries and receive feedback on performance
    def submission(self):
        i = 1
        for entry in range(1,14,2):
            if self.conjugation_table[entry].get() == self.conjugation[i]:
                feedback = Label(self.f_conjugation_table, text=self.conjugation_table[entry].get(),
                                 padx=40, pady=10, bg='#AAFFAA')  # Correct
            else:
                feedback = Label(self.f_conjugation_table, text=self.conjugation_table[entry].get(),
                                 padx=20, pady=10, bg='#FFAAAA')  # Incorrect
            # Delete Entry to replace with feedback label
            self.conjugation_table[entry].destroy()
            feedback.grid(column=1, row=floor(entry / 2), sticky='WE')  # 'we' fills area of feedback with color
            i += 1

        # Replace button
        self.submit.destroy()
        done = Button(self.f_conjugation_table, text="Done", command=quit)
        done.grid(column=0, row=8, columnspan=2, sticky='S', pady=20)
