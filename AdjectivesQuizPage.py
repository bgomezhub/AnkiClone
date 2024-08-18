import random
import sqlite3
from tkinter import *


class AdjectivesQuizPage:
    def __init__(self, frame):
        # Table Frame
        self.f_adj_table = Frame(frame)
        self.f_adj_table.grid(column=0, row=0, padx=200, pady=200)

        # conjugation
        self.adj = []
        self.select_adj()

        # Define & Display conjugation table
        self.adj_table = []
        self.define_adj_table()

        # Submission
        self.submit = Button(
            self.f_adj_table, text="Submit", command=lambda: self.submission())
        self.submit.grid(column=0, row=8, columnspan=2, sticky='S', pady=20)  # Padding between table & button

    def define_adj_table(self):
        # Define conjugation
        self.adj_table.append(Label(self.f_adj_table, text=self.adj[0], font=('Arial', 30)))
        self.adj_table[0].grid(column=0, row=0, columnspan=2, pady=10)
        # Build table
        adj_props = ['Masculine s.', 'Feminine s.', 'Masculine p.', 'Feminine p.']
        for num in range(2, 10):
            if num % 2 == 0:
                self.adj_table.append(
                    Label(self.f_adj_table, text=adj_props[num // 2 - 1], pady=8, padx=25))
                self.adj_table[num - 1].grid(column=0, row=num // 2)
            else:
                self.adj_table.append(Entry(self.f_adj_table))
                self.adj_table[num - 1].grid(column=1, row=num // 2)

    def select_adj(self):
        # Select all in a list
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Select Table
        c.execute("SELECT * FROM adjectives")
        db_table = c.fetchall()
        # Choose random number & assign to conjugation
        self.adj = db_table[random.randint(0, len(db_table) - 1)]

    # Submit entries and receive feedback on performance
    def submission(self):
        i = 1
        for entry in range(2, 9, 2):
            if self.adj_table[entry].get() == self.adj[i]:
                feedback = Label(self.f_adj_table, text=self.adj_table[entry].get(),
                                 padx=40, pady=10, bg='#AAFFAA')  # Correct
            else:
                feedback = Label(self.f_adj_table, text=self.adj_table[entry].get(),
                                 padx=20, pady=10, bg='#FFAAAA')  # Incorrect
                Label(self.f_adj_table, text=self.adj[i], padx=40, pady=10).grid(column=3, row=i)
            # Delete Entry to replace with feedback label
            self.adj_table[entry].destroy()
            feedback.grid(column=1, row=(entry // 2), sticky='WE')  # 'we' fills area of feedback with color
            # Show correct answer
            i += 1

        # Replace button
        self.submit.destroy()
        done = Button(self.f_adj_table, text="Done", command=quit)
        done.grid(column=0, row=8, columnspan=3, sticky='S', pady=20)