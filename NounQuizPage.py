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

        # Font for body
        self.font_b = ('Arial', 14)

        # Select noun
        self.word = word_list[0][word_list[1]][0]  # noun index
        self.noun = QuizManager.select_word('noun', self.word)
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
        ctk.CTkCheckBox(self.f_nouns_table, text="Les", font=self.font_b,
                        variable=self.plural, onvalue=1, offvalue=0, width=90).grid(column=0, row=1)

        # Define gender
        ctk.CTkRadioButton(self.f_nouns_table, text="Le", font=self.font_b,
                           variable=self.gen,  value='le', width=70).grid(column=1, row=1)
        ctk.CTkRadioButton(self.f_nouns_table, text="La", font=self.font_b,
                           variable=self.gen, value='la', width=70).grid(column=2, row=1)

        # Define Input box
        self.nouns_table.append(ctk.CTkEntry(self.f_nouns_table, width=90))
        self.nouns_table[0].grid(column=3, row=1)
        return

    # Submit entries and receive feedback on performance
    def submission(self, word_list):
        grade = 0
        # Check fr translation
        if self.nouns_table[0].get() == self.noun[1]:
            feedback = ctk.CTkLabel(self.f_nouns_table, text=self.nouns_table[0].get(), font=self.font_b,
                                    padx=25, pady=12, bg_color='#AAFFAA')
            grade += 1
        else:
            ctk.CTkLabel(self.f_nouns_table, text=self.noun[1], font=self.font_b,
                         padx=25, pady=12).grid(column=4, row=1)
            feedback = ctk.CTkLabel(self.f_nouns_table, text=self.nouns_table[0].get(), font=self.font_b,
                                    padx=25, pady=12, bg_color='#FFAAAA')
        self.nouns_table[0].destroy()  # Clear Entry from screen
        # Clear list to gather info to be displayed
        self.nouns_table.clear()
        self.nouns_table.append(feedback)

        # Check gender
        # Correct
        if self.gen.get() == self.noun[-2]:
            self.nouns_table.append(ctk.CTkLabel(self.f_nouns_table, text=self.noun[-2], font=self.font_b,
                                                 padx=25, pady=12, bg_color='#AAFFAA'))
            grade += 1
        # Incorrect
        else:
            self.nouns_table.append(ctk.CTkLabel(self.f_nouns_table, text=self.gen.get(), font=self.font_b,
                                                 padx=25, pady=12, bg_color='#FFAAAA'))

        # Check Plurality
        # Correct
        if self.plural.get() == self.noun[-1]:
            if self.noun[-1] == 0:
                self.nouns_table.append(ctk.CTkLabel(self.f_nouns_table, text="Not Plural", font=self.font_b,
                                                     padx=25, pady=12, bg_color='#AAFFAA'))
            else:
                self.nouns_table.append(ctk.CTkLabel(self.f_nouns_table, text="Plural", font=self.font_b,
                                                     padx=25, pady=12, bg_color='#AAFFAA'))
            grade += 1
        # Incorrect
        else:
            if self.noun[-1] == 0:
                self.nouns_table.append(ctk.CTkLabel(self.f_nouns_table, text="Plural", font=self.font_b,
                                                     padx=25, pady=12, bg_color='#FFAAAA'))
            else:
                self.nouns_table.append(ctk.CTkLabel(self.f_nouns_table, text="Not Plural", font=self.font_b,
                                                     padx=25, pady=12, bg_color='#FFAAAA'))

        # Display feedback
        for i in range(-1, -4, -1):
            self.nouns_table[i].grid(column=abs(i + 1), row=1, sticky='WE')

        grade = grade/3  # Percentage
        # pts cap has not been hit
        if QuizManager.get_pts_cap(self.word) == 0:
            # Add pts, set pts cap
            QuizManager.update_pts(self.word, grade)

        # Display Button
        self.submit.destroy()
        # Also handles cooldown
        QuizManager.next_button(self.root_frame, self.f_submission, self.font_b, word_list, grade)
        return
