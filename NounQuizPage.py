import sqlite3
import customtkinter as ctk

import QuizManager


class NounQuizPage:
    def __init__(self, frame, word_list):
        # Table Frame
        self.root_frame = frame
        self.f_question = ctk.CTkFrame(frame)
        self.f_question.grid(column=0, row=0, padx=200, pady=75)
        self.f_nouns_table = ctk.CTkFrame(frame)
        self.f_nouns_table.grid(column=0, row=1, padx=200, pady=50)
        self.f_submission = ctk.CTkFrame(frame)
        self.f_submission.grid(column=0, row=2, padx=200, pady=75)

        # Select noun
        word = word_list[0][word_list[1]][0]
        self.noun = ''
        self.select_noun(word)
        # Properties of noun
        self.gen = ctk.StringVar()
        self.plural = ctk.IntVar()

        # Define & Display nouns table
        self.nouns_table = []
        self.define_nouns_table()

        # Submission
        self.submit = ctk.CTkButton(
            self.f_submission, text="Submit", command=lambda: self.submission(word_list))
        self.submit.grid(column=0, row=2, columnspan=4, sticky='S', pady=20)  # Padding between table & button

    def define_nouns_table(self):
        # Define noun table
        # Define noun
        ctk.CTkLabel(self.f_question, text=self.noun[0], font=('Arial', 40)).grid(column=0, row=0)

        # Define plurality
        ctk.CTkCheckBox(self.f_nouns_table, text="Les",
                        variable=self.plural, onvalue=1, offvalue=0, width=90).grid(column=0, row=1)

        # Define gender
        ctk.CTkRadioButton(self.f_nouns_table, text="Le",
                           variable=self.gen,  value='le', width=70).grid(column=1, row=1)
        ctk.CTkRadioButton(self.f_nouns_table, text="La",
                           variable=self.gen, value='la', width=70).grid(column=2, row=1)

        # Define Input box
        self.nouns_table.append(ctk.CTkEntry(self.f_nouns_table, width=90))
        self.nouns_table[0].grid(column=3, row=1)
        return

    def select_noun(self, word):
        # Select all in a list
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Select Table
        c.execute(f"SELECT * FROM noun WHERE en = '{word}'")
        # Retrieve word
        self.noun = c.fetchone()
        return

    # Submit entries and receive feedback on performance
    def submission(self, word_list):
        # Check fr translation
        if self.nouns_table[0].get() == self.noun[1]:
            feedback = ctk.CTkLabel(
                self.f_nouns_table, text=self.nouns_table[0].get(), padx=25, pady=12, bg_color='#AAFFAA')
        else:
            ctk.CTkLabel(self.f_nouns_table, text=self.noun[1], padx=25, pady=12).grid(column=4, row=1)
            feedback = ctk.CTkLabel(
                self.f_nouns_table, text=self.nouns_table[0].get(), padx=25, pady=12, bg_color='#FFAAAA')
        self.nouns_table[0].destroy()  # Clear Entry from screen
        # Clear list to gather info to be displayed
        self.nouns_table.clear()
        self.nouns_table.append(feedback)

        # Check gender
        if self.gen.get() == self.noun[-2]:
            self.nouns_table.append(ctk.CTkLabel(
                self.f_nouns_table, text=self.noun[-2], padx=25, pady=12, bg_color='#AAFFAA'))
        else:
            self.nouns_table.append(ctk.CTkLabel(
                self.f_nouns_table, text=self.gen.get(), padx=25, pady=12, bg_color='#FFAAAA'))

        # Check Plurality
        if self.plural.get() == self.noun[-1] and self.noun[-1] == 0:
            self.nouns_table.append(ctk.CTkLabel(
                self.f_nouns_table, text="Not Plural", padx=25, pady=12, bg_color='#AAFFAA'))

        elif self.plural.get() == self.noun[-1] and self.noun[-1] == 1:
            self.nouns_table.append(ctk.CTkLabel(
                self.f_nouns_table, text="Plural", padx=25, pady=12, bg_color='#AAFFAA'))
        else:
            if self.noun[-1] == 0:
                self.nouns_table.append(ctk.CTkLabel(
                    self.f_nouns_table, text="Plural", padx=25, pady=12, bg_color='#FFAAAA'))
            else:
                self.nouns_table.append(ctk.CTkLabel(
                    self.f_nouns_table, text="Not Plural", padx=25, pady=12, bg_color='#FFAAAA'))

        # Display feedback
        for i in range(-1, -4, -1):
            self.nouns_table[i].grid(column=abs(i + 1), row=1, sticky='WE')

        # Display Button
        self.submit.destroy()
        done = ctk.CTkButton(self.f_submission, text='Next', command=lambda: self.return_quiz_manager(word_list))
        done.grid(column=0, row=0, pady=20)
        return

    # Destroy page and return to QuizManager.py
    def return_quiz_manager(self, word_list):
        for widget in self.root_frame.winfo_children():
            widget.destroy()

        word_list = QuizManager.remove_question(word_list)
        return QuizManager.next_question(self.root_frame, word_list, self.noun)
