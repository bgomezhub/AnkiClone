import random
import sqlite3
from tkinter import *


class NounQuizPage:
    def __init__(self, frame):
        # Table Frame
        self.f_nouns_table = Frame(frame)
        self.f_nouns_table.grid(column=0, row=0, padx=200, pady=200)

        # select noun
        self.noun = []
        self.select_noun()

        # Define & Display nouns table
        self.nouns_table = []
        self.define_nouns_table()

        # Submission
        self.submit = Button(
            self.f_nouns_table, text="Submit", command=lambda: self.submission())
        self.submit.grid(column=0, row=2, columnspan=4, sticky='S', pady=20)  # Padding between table & button

    def define_nouns_table(self):
        # Define noun table
        # Define noun
        self.nouns_table.append(Label(self.f_nouns_table, text=self.noun[0], font=('Arial', 30), padx=20, pady=10))
        self.nouns_table[0].grid(column=0, row=0, columnspan=4)
        # Define plurality
        check = IntVar()
        Checkbutton(self.f_nouns_table, text="Les", variable=check, onvalue=1, offvalue=0).grid(column=0, row=1)
        # Define gender
        gen = StringVar()
        self.nouns_table.append(Radiobutton(self.f_nouns_table, text="Le", variable=gen, value='Le'))
        self.nouns_table[1].grid(column=1, row=1)
        self.nouns_table.append(Radiobutton(self.f_nouns_table, text="La", variable=gen, value='La'))
        self.nouns_table[2].grid(column=2, row=1)
        # Define Input box
        self.nouns_table.append(Entry(self.f_nouns_table))
        self.nouns_table[3].grid(column=3, row=1)

    def select_noun(self):
        # Select all in a list
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Select Table
        c.execute("SELECT * FROM nouns")
        db_table = c.fetchall()
        # Choose random number & assign to conjugation
        self.noun = db_table[random.randint(0, len(db_table) - 1)]
        return

    # Submit entries and receive feedback on performance
    def submission(self):
        i = 1
        for entry in range(1, 14, 2):
            if self.nouns_table[entry].get() == self.noun[i]:
                feedback = Label(self.f_nouns_table, text=self.nouns_table[entry].get(),
                                 padx=40, pady=10, bg='#AAFFAA')  # Correct
            else:
                feedback = Label(self.f_nouns_table, text=self.nouns_table[entry].get(),
                                 padx=20, pady=10, bg='#FFAAAA')  # Incorrect
                Label(self.f_nouns_table, text=self.noun[i], padx=40, pady=10).grid(column=3, row=i - 1)
            # Delete Entry to replace with feedback label
            self.nouns_table[entry].destroy()
            feedback.grid(column=1, row=(entry // 2), sticky='WE')  # 'we' fills area of feedback with color
            # Show correct answer
            i += 1

        # Replace button
        self.submit.destroy()
        done = Button(self.f_nouns_table, text="Done", command=quit)
        done.grid(column=0, row=2, columnspan=4, sticky='S', pady=20)
