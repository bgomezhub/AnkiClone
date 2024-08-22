import sqlite3
from tkinter import *

import Home
import QuizManager


class AdjectivesQuizPage:
    def __init__(self, frame, word_list):
        # Table Frame
        self.root_frame = frame
        self.f_adj_table = Frame(frame)
        self.f_adj_table.grid(column=0, row=0, padx=200, pady=200)

        # Adjective
        word = word_list[0][word_list[1]][0]
        self.adj = ''
        self.select_adj(word)

        # Define & Display adjective table
        self.adj_table = []
        self.define_adj_table()

        # Submission
        self.submit = Button(
            self.f_adj_table, text="Submit", command=lambda: self.submission(word_list))
        self.submit.grid(column=0, row=8, columnspan=2, sticky='S', pady=20)  # Padding between table & button

    def define_adj_table(self):
        # Define adjective
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
        return

    def select_adj(self, word):
        # Select all in a list
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Select Table
        c.execute(f"SELECT * FROM adjective WHERE en = '{word}'")
        # Choose random number & assign to conjugation
        self.adj = c.fetchone()
        return

    # Submit entries and receive feedback on performance
    def submission(self, word_list):
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
        done = Button(self.f_adj_table, text="Next", command=lambda: self.return_quiz_manager(word_list))
        done.grid(column=0, row=8, columnspan=3, sticky='S', pady=20)
        return

    # Destroy page and return to QuizManager.py
    def return_quiz_manager(self, word_list):
        for widget in self.root_frame.winfo_children():
            widget.destroy()

        word_list = QuizManager.remove_question(word_list)
        return QuizManager.next_question(self.root_frame, word_list[0], self.adj)

