import sqlite3
import customtkinter as ctk

import Home
import QuizManager


class AdjectivesQuizPage:
    def __init__(self, frame, word_list):
        # Table Frame
        self.root_frame = frame
        self.f_question = ctk.CTkFrame(frame)
        self.f_question.grid(column=0, row=0, padx=200, pady=75)
        self.f_adj_table = ctk.CTkFrame(frame)
        self.f_adj_table.grid(column=0, row=1, padx=200, pady=50)
        self.f_submission = ctk.CTkFrame(frame)
        self.f_submission.grid(column=0, row=2, padx=200, pady=75)

        # Font for body
        self.font_b = ('Arial', 14)

        # Adjective
        word = word_list[0][word_list[1]][0]
        self.adj = QuizManager.select_word('adjective', word)

        # Define & Display adjective table
        self.adj_table = []
        self.define_adj_table()

        # Submission
        self.submit = ctk.CTkButton(
            self.f_submission, text="Submit", font=self.font_b, command=lambda: self.submission(word_list))
        self.submit.grid(column=0, row=8, columnspan=2, sticky='S', pady=20)

    def define_adj_table(self):
        # Define adjective
        ctk.CTkLabel(self.f_question, text=self.adj[0], font=('Arial', 40)).grid(column=0, row=0)

        # Build table
        adj_props = ['Masculine s.', 'Feminine s.', 'Masculine p.', 'Feminine p.']
        for num in range(0, 8):
            if num % 2 == 0:
                self.adj_table.append(
                    ctk.CTkLabel(self.f_adj_table, text=adj_props[num // 2], font=self.font_b,  pady=12, padx=25))
                self.adj_table[num].grid(column=0, row=num // 2)
            else:
                self.adj_table.append(ctk.CTkEntry(self.f_adj_table))
                self.adj_table[num].grid(column=1, row=num // 2)
        return

    # Submit entries and receive feedback on performance
    def submission(self, word_list):
        for entry in range(1, 8, 2):
            if self.adj_table[entry].get() == self.adj[-(-entry // 2)]:
                feedback = ctk.CTkLabel(self.f_adj_table, text=self.adj_table[entry].get(), font=self.font_b,
                                        padx=25, pady=12, bg_color='#AAFFAA')  # Correct
            else:
                feedback = ctk.CTkLabel(self.f_adj_table, text=self.adj_table[entry].get(), font=self.font_b,
                                        padx=25, pady=12, bg_color='#FFAAAA')  # Incorrect
                ctk.CTkLabel(self.f_adj_table, text=self.adj[-(-entry // 2)], font=self.font_b,
                             padx=25, pady=12).grid(column=3, row=entry // 2)
            # Delete Entry to replace with feedback label
            self.adj_table[entry].destroy()
            feedback.grid(column=1, row=(entry // 2), sticky='WE')  # 'we' fills area of feedback with color

        # Replace button
        self.submit.destroy()
        done = ctk.CTkButton(self.f_submission, text="Next", font=self.font_b,
                             command=lambda: QuizManager.reset_quiz_manager(self.root_frame, word_list))
        done.grid(column=0, row=0, sticky='S', pady=20)
        return
