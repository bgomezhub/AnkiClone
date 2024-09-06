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
        self.word = word_list[0][word_list[1]][0]
        self.adj = QuizManager.select_word('adjective', self.word)

        # Define & Display adjective table
        self.adj_table = self.define_adj_table()

        # Submission
        self.submit = ctk.CTkButton(
            self.f_submission, text="Submit", font=self.font_b, command=lambda: self.submission(word_list))
        self.submit.grid(column=0, row=8, columnspan=2, sticky='S', pady=20)

    def define_adj_table(self):
        # Define adjective title
        ctk.CTkLabel(self.f_question, text=self.adj[0], font=('Arial', 40)).grid(column=0, row=0)

        # Build table
        adj_props = ['Masculine s.', 'Feminine s.', 'Masculine p.', 'Feminine p.']
        # Return list of table widgets
        return QuizManager.build_table(self.f_adj_table, self.font_b, adj_props, 8)

    # Submit entries and receive feedback on performance
    def submission(self, word_list):
        # Provide feedback
        grade = QuizManager.table_feedback(self.f_adj_table, self.adj_table, self.font_b, self.adj, 8)

        # pts cap has not been hit
        if QuizManager.get_pts_cap(self.word) == 0:
            # Add pts, set pts_cap
            QuizManager.update_pts(self.word, grade)

        # Replace button
        self.submit.destroy()
        # Also handles cooldown
        QuizManager.next_button(self.root_frame, self.f_submission, self.font_b, word_list, grade)

        return
