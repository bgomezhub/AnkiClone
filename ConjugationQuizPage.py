import random
import sqlite3
import customtkinter as ctk

import QuizManager


class ConjugationQuizPage:
    def __init__(self, frame, word_list):
        # Table Frame
        self.root_frame = frame
        self.f_question = ctk.CTkFrame(frame)
        self.f_question.grid(column=0, row=0, padx=200, pady=50)
        self.f_conjugation_table = ctk.CTkFrame(frame)
        self.f_conjugation_table.grid(column=0, row=1, padx=200, pady=25)
        self.f_submission = ctk.CTkFrame(frame)
        self.f_submission.grid(column=0, row=2, padx=200, pady=50)

        # Font for body
        self.font_b = ('Arial', 14)

        # conjugation
        word = word_list[0][word_list[1]][0]
        self.conjugation = QuizManager.select_word('present_verb', word)

        # Define & Display conjugation table
        self.conjugation_table = self.define_conjugation_table()

        # Submission
        self.submit = ctk.CTkButton(
            self.f_submission, text="Submit", font=self.font_b, command=lambda: self.submission(word_list))
        self.submit.grid(column=0, row=0, sticky='S', pady=20)

    def define_conjugation_table(self):
        # Define conjugation question (top)
        ctk.CTkLabel(self.f_question, text=self.conjugation[0], font=("Arial", 40)).grid(column=0, row=0)

        # Build table
        con_subjects = ['infinitive', 'Je', 'Tu', 'Il/Elle', 'Nous', 'Vous', 'Ils/Elles']
        return QuizManager.build_table(self.f_conjugation_table, self.font_b, con_subjects, 14)

    # Submit entries and receive feedback on performance
    def submission(self, word_list):
        # Provide feedback
        QuizManager.table_feedback(self.f_conjugation_table, self.conjugation_table, self.font_b, self.conjugation, 14)

        # Replace button
        self.submit.destroy()
        done = ctk.CTkButton(self.f_submission, text="Next", font=self.font_b,
                             command=lambda: QuizManager.reset_quiz_manager(self.root_frame, word_list))
        done.grid(column=0, row=0, sticky='S', pady=20)
        return
