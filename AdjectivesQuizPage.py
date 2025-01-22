import customtkinter as ctk
import QuizManager


class AdjectivesQuizPage:
    def __init__(self, f_root, word_list):
        # Fonts
        font = QuizManager.get_fonts()
        self.font_title = ctk.CTkFont(family=font[0], size=font[1])
        self.font_body = ctk.CTkFont(family=font[0], size=font[2])

        # Declare Frames
        self.f_page = ctk.CTkScrollableFrame(f_root)
        self.f_page.pack(fill='both', expand=True)
        self.f_question = ctk.CTkFrame(self.f_page)
        self.f_question.pack(pady=50)
        self.f_adj_table = ctk.CTkFrame(self.f_page)
        self.f_adj_table.pack(pady=25)
        self.f_submission = ctk.CTkFrame(self.f_page)
        self.f_submission.pack(pady=75)

        # Adjective
        self.word = word_list[0][word_list[1]][0]
        self.table = word_list[0][word_list[1]][1]

        # Define & Display adjective table
        self.adj_table = self.build_adj_table()
        # Define & Display submission button
        QuizManager.submission_button(self.f_page, self.f_submission, self.font_body, self.adj_table, word_list)

    def build_adj_table(self):
        # Build table
        adj_props = ['Masculine s.', 'Feminine s.', 'Masculine p.', 'Feminine p.']

        QuizManager.quiz_title(self.f_question, self.font_title, self.word, self.table)
        return QuizManager.build_table(self.f_adj_table, self.font_body, self.word, self.table, adj_props)
