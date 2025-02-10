import customtkinter as ctk
import Model
from controllers import Quiz


class Conjugation:
    def __init__(self, f_root, word_list):
        # Fonts
        font = Model.get_fonts()
        self.font_title = ctk.CTkFont(family=font[0], size=font[1])
        self.font_body = ctk.CTkFont(family=font[0], size=font[2])

        # Declare Frames
        self.f_page = ctk.CTkScrollableFrame(f_root)
        self.f_page.pack(fill="both", expand=True)
        self.f_question = ctk.CTkFrame(self.f_page)
        self.f_question.pack(pady=50)
        self.f_conjugation_table = ctk.CTkFrame(self.f_page)
        self.f_conjugation_table.pack(pady=25)
        self.f_submission = ctk.CTkFrame(self.f_page)
        self.f_submission.pack(pady=75)

        # Conjugation
        self.word = word_list[0][word_list[1]][0]
        self.table = word_list[0][word_list[1]][1]

        # Define & Display conjugation table
        self.conjugation_table = self.build_conjugation_table()
        # Define & Display submission button
        Quiz.submission_button(self.f_page, self.f_submission, self.font_body, self.conjugation_table,
                                         word_list)

    def build_conjugation_table(self):
        con_subjects = ['Infinitive', 'Je', 'Tu', 'Il/Elle', 'Nous', 'Vous', 'Ils/Elles']

        Quiz.quiz_title(self.f_question, self.font_title, self.word, self.table)
        return Quiz.build_table(self.f_conjugation_table, self.font_body, self.word, self.table, con_subjects)
