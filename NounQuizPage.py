import random
import sqlite3
from tkinter import *


class NounQuizPage:
    def __init__(self, frame):
        # Table Frame
        self.f_nouns_table = Frame(frame)
        self.f_nouns_table.grid(column=0, row=0, padx=200, pady=200)

        # Select noun
        self.noun = []
        self.select_noun()

        # Properties of noun
        self.gen = StringVar()
        self.plural = IntVar()

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
        Checkbutton(self.f_nouns_table, text="Les", variable=self.plural, onvalue=1, offvalue=0).grid(column=0, row=1)

        # Define gender
        Radiobutton(self.f_nouns_table, text="Le", variable=self.gen,  value='le').grid(column=1, row=1)
        Radiobutton(self.f_nouns_table, text="La", variable=self.gen, value='la').grid(column=2, row=1)

        # Define Input box
        self.nouns_table.append(Entry(self.f_nouns_table))
        self.nouns_table[1].grid(column=3, row=1)

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
        # Check fr translation
        if self.nouns_table[1].get() == self.noun[1]:
            feedback = Label(self.f_nouns_table, text=self.nouns_table[1].get(), padx=40, pady=10, bg='#AAFFAA')
        else:
            Label(self.f_nouns_table, text=self.noun[1], padx=40, pady=10).grid(column=4, row=1)
            feedback = Label(self.f_nouns_table, text=self.nouns_table[1].get(), padx=40, pady=10, bg='#FFAAAA')
        self.nouns_table[1].destroy()  # Clear Entry from screen
        # Clear list to gather info to be displayed
        self.nouns_table.clear()
        self.nouns_table.append(feedback)

        # Check gender
        if self.gen.get() == self.noun[-2]:
            self.nouns_table.append(Label(self.f_nouns_table, text=self.noun[-2], padx=40, pady=10, bg='#AAFFAA'))
        else:
            self.nouns_table.append(Label(self.f_nouns_table, text=self.gen.get(), padx=40, pady=10, bg='#FFAAAA'))

        # Check Plurality
        if self.plural.get() == self.noun[-1] and self.noun[-1] == 0:
            self.nouns_table.append(Label(self.f_nouns_table, text="Not Plural", padx=40, pady=10, bg='#AAFFAA'))
        elif self.plural.get() == self.noun[-1] and self.noun[-1] == 1:
            self.nouns_table.append(Label(self.f_nouns_table, text="Plural", padx=40, pady=10, bg='#AAFFAA'))
        else:
            if self.noun[-1] == 0:
                self.nouns_table.append(Label(self.f_nouns_table, text="Not Plural", padx=40, pady=10, bg='#FFAAAA'))
            else:
                self.nouns_table.append(Label(self.f_nouns_table, text="Not Plural", padx=40, pady=10, bg='#FFAAAA'))
        # Display feedback
        for i in range(-1, -4, -1):
            self.nouns_table[i].grid(column=abs(i + 1), row=1)
        # Display Button
        self.submit.destroy()
        done = Button(self.f_nouns_table, text='Done', command=quit)
        done.grid(column=0, row=2, columnspan=4, pady=20)
