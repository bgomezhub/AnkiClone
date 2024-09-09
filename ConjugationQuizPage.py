import customtkinter as ctk
import QuizManager


class ConjugationQuizPage:
    def __init__(self, frame, word_list):
        # Declare Frames
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
        self.word = word_list[0][word_list[1]][0]
        self.is_new = QuizManager.get_new_info(self.word)
        self.conjugation = QuizManager.select_word('present_verb', self.word)

        # Define & Display conjugation table
        self.conjugation_table = self.define_conjugation_table()

        # Skip submission step for new words
        if self.is_new == 1:
            # New word, no pts/cap/cooldown
            QuizManager.submission_new_word(self.root_frame, self.f_submission, self.font_b, word_list)
        else:
            # Submission
            self.submit = ctk.CTkButton(self.f_submission, text="Submit", font=self.font_b,
                                        command=lambda: self.submission(word_list))
            self.submit.grid(column=0, row=0, sticky='S', pady=20)

    def define_conjugation_table(self):
        # Build table
        con_subjects = ['infinitive', 'Je', 'Tu', 'Il/Elle', 'Nous', 'Vous', 'Ils/Elles']

        if self.is_new == 1:
            # Define conjugation question (top)
            QuizManager.quiz_title(self.f_question, self.word, new=True)

            # Word is new, build table w/o entries, do not need return
            QuizManager.build_table_new_word(self.f_conjugation_table, self.font_b, con_subjects, 14,
                                             word=self.conjugation)
        else:
            # Define conjugation question (top)
            QuizManager.quiz_title(self.f_question, self.word)
            # Return table widgets
            return QuizManager.build_table(self.f_conjugation_table, self.font_b, con_subjects, 14)

    # Submit entries and receive feedback on performance
    def submission(self, word_list):
        # Display & track feedback
        grade = QuizManager.table_feedback(
            self.f_conjugation_table, self.conjugation_table, self.font_b, self.conjugation, 14)

        # pts cap has not been hit
        if QuizManager.get_pts_cap(self.word) == 0:
            # Add pts, set pts cap
            QuizManager.set_pts(self.word, grade)

        # Replace button
        self.submit.destroy()
        # Also handles cooldown
        QuizManager.next_button(self.root_frame, self.f_submission, self.font_b, word_list, grade)

        return
