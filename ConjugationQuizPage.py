import customtkinter as ctk
import QuizManager


class ConjugationQuizPage:
    def __init__(self, frame, word_list):
        # Fonts
        font = QuizManager.get_fonts()
        self.font_title = ctk.CTkFont(family=font[0], size=font[1])
        self.font_body = ctk.CTkFont(family=font[0], size=font[2])
        # Declare Frames
        self.root_frame = ctk.CTkScrollableFrame(frame)
        self.root_frame.pack(fill="both", expand=True)
        self.f_question = ctk.CTkFrame(self.root_frame)
        self.f_question.pack(pady=50)
        self.f_conjugation_table = ctk.CTkFrame(self.root_frame)
        self.f_conjugation_table.pack(pady=25)
        self.f_submission = ctk.CTkFrame(self.root_frame)
        self.f_submission.pack(pady=75)

        # composite conjugations
        self.composite_conjugations = ['passe_compose', 'futur_anterieur', 'plus_que_parfait']

        # conjugation
        self.word = word_list[0][word_list[1]][0]
        self.table = word_list[0][word_list[1]][1]
        self.is_new = QuizManager.get_new_info(self.word, self.table)
        self.conjugation = QuizManager.select_word(self.word, self.table)

        # Define & Display conjugation table
        self.conjugation_table = self.define_conjugation_table()

        # Skip submission step for new words, no pts/cap/cooldown to be changed
        if self.is_new == 1:
            QuizManager.submission_new_word(self.root_frame, self.font_body, self.f_submission, word_list)
        else:
            # Submission
            self.submit = ctk.CTkButton(self.f_submission, text="Submit", font=self.font_body,
                                        command=lambda: self.submission(word_list))
            self.submit.grid(column=0, row=0, sticky='S', pady=20)

    def define_conjugation_table(self):
        # Build table
        con_subjects = ['Infinitive', 'Je', 'Tu', 'Il/Elle', 'Nous', 'Vous', 'Ils/Elles']

        # Word is new, build table w/o entries, do not need return
        if self.is_new == 1:
            QuizManager.quiz_title(self.f_question, self.font_title, self.word, new=True)

            if self.table in self.composite_conjugations:
                QuizManager.build_table_new_word_comp(self.f_conjugation_table, self.font_body, con_subjects, 21,
                                                      self.conjugation)
            else:
                QuizManager.build_table_new_word(self.f_conjugation_table, self.font_body, con_subjects, 14,
                                                 self.conjugation)
        else:
            QuizManager.quiz_title(self.f_question, self.font_title, self.word)
            # Return table widgets
            if self.table in self.composite_conjugations:
                return QuizManager.build_table(self.f_conjugation_table, self.font_body, con_subjects, 21, columns=3)
            else:
                return QuizManager.build_table(self.f_conjugation_table, self.font_body, con_subjects, 14)

    # Submit entries and receive feedback on performance
    def submission(self, word_list):
        # Display & track feedback
        if self.is_new:
            grade = QuizManager.table_feedback(
                self.f_conjugation_table, self.font_body, self.conjugation_table, self.conjugation, 21)
        else:
            grade = QuizManager.table_feedback(
                self.f_conjugation_table, self.font_body, self.conjugation_table, self.conjugation, 14)

        # pts cap has not been hit
        if QuizManager.get_pts_cap(self.word) == 0:
            # Add pts, set pts cap
            QuizManager.set_pts(self.word, grade)

        # Replace button
        self.submit.destroy()
        # Also handles cooldown
        QuizManager.next_button(self.root_frame, self.font_body, self.f_submission, word_list, grade)

        return
