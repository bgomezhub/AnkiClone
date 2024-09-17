import customtkinter as ctk
from tkinter import ttk
import QuizManager


class NounQuizPage:
    def __init__(self, frame, word_list):
        # Table Frame
        self.root_frame = frame
        self.f_question = ctk.CTkFrame(frame)
        self.f_question.grid(column=0, row=0, padx=200, pady=75)
        self.f_noun_table = ctk.CTkFrame(frame)
        self.f_noun_table.grid(column=0, row=1, padx=200, pady=50)
        self.f_submission = ctk.CTkFrame(frame)
        self.f_submission.grid(column=0, row=2, padx=200, pady=75)

        # Select noun
        self.word = word_list[0][word_list[1]][0]  # noun index
        self.is_new = QuizManager.get_new_info(self.word)
        self.noun = QuizManager.select_word('noun', self.word)

        # Properties of noun
        self.gen = ctk.StringVar()
        self.plural = ctk.IntVar()

        # Display new word or none new word
        if self.is_new == 1:
            # Define & Display nouns table
            self.define_noun_table_new_word()
            # New word, no pts/cap/cooldown
            QuizManager.submission_new_word(self.root_frame, self.f_submission, word_list)
        else:
            # Define & Display nouns table
            self.noun_table = []
            self.define_noun_table()
            # Submission
            self.submit = ctk.CTkButton(self.f_submission, text="Submit",
                                        command=lambda: self.submission(word_list))
            self.submit.grid(column=0, row=2, columnspan=4, sticky='S', pady=20)

    def define_noun_table(self):
        # Define noun table
        # Define noun
        QuizManager.quiz_title(self.f_question, self.word)

        # Define plurality
        ctk.CTkCheckBox(self.f_noun_table, text="Les", variable=self.plural,
                        onvalue=1, offvalue=0, width=90).grid(column=0, row=1)

        # Define gender
        ctk.CTkRadioButton(self.f_noun_table, text="Le", variable=self.gen,  value='le', width=70).grid(column=1, row=1)
        ctk.CTkRadioButton(self.f_noun_table, text="La", variable=self.gen, value='la', width=70).grid(column=2, row=1)

        # Define Input box
        self.noun_table.append(ctk.CTkEntry(self.f_noun_table, width=90))
        self.noun_table[0].grid(column=3, row=1)
        return

    def define_noun_table_new_word(self):
        # Define noun title
        QuizManager.quiz_title(self.f_question, self.word, new=True)

        # Get plurality from word, no SQL necessary since there is no info to gather.
        if self.noun[-1] == 0:
            ctk.CTkLabel(self.f_noun_table, text='Not Plural', padx=25, pady=12).grid(column=0, row=1)
        else:
            ctk.CTkLabel(self.f_noun_table, text='Plural', padx=25, pady=12).grid(column=0, row=1)

        # Add separator
        ttk.Separator(self.f_noun_table, orient='vertical').grid(column=1, row=1, sticky='ns')

        # Get gender from word NO SQL
        if self.noun[-2] == 'le':
            ctk.CTkLabel(self.f_noun_table, text='Le', padx=25, pady=12).grid(column=2, row=1)
        else:
            ctk.CTkLabel(self.f_noun_table, text='La', padx=25, pady=12).grid(column=2, row=1)

        # Add separator
        ttk.Separator(self.f_noun_table, orient='vertical').grid(column=3, row=1, sticky='ns')

        # Get word translation
        ctk.CTkLabel(self.f_noun_table, text=self.noun[-3], padx=25, pady=12).grid(column=4, row=1)
        return

    # Submit entries and receive feedback on performance
    def submission(self, word_list):
        grade = 0
        # Check fr translation
        if self.noun_table[0].get() == self.noun[1]:
            feedback = ctk.CTkLabel(self.f_noun_table, text=self.noun_table[0].get(), padx=25, pady=12, bg_color='#AAFFAA')
            grade += 1
        else:
            ctk.CTkLabel(self.f_noun_table, text=self.noun[1], padx=25, pady=12).grid(column=4, row=1)
            feedback = ctk.CTkLabel(self.f_noun_table, text=self.noun_table[0].get(),
                                    padx=25, pady=12, bg_color='#FFAAAA')
        self.noun_table[0].destroy()  # Clear Entry from screen
        # Clear list to gather info to be displayed
        self.noun_table.clear()
        self.noun_table.append(feedback)

        # Check gender
        # Correct
        if self.gen.get() == self.noun[-2]:
            self.noun_table.append(ctk.CTkLabel(self.f_noun_table, text=self.noun[-2],
                                                padx=25, pady=12, bg_color='#AAFFAA'))
            grade += 1
        # Incorrect
        else:
            self.noun_table.append(ctk.CTkLabel(self.f_noun_table, text=self.gen.get(),
                                                padx=25, pady=12, bg_color='#FFAAAA'))

        # Check Plurality
        # Correct
        if self.plural.get() == self.noun[-1]:
            if self.noun[-1] == 0:
                self.noun_table.append(ctk.CTkLabel(self.f_noun_table, text="Not Plural",
                                                    padx=25, pady=12, bg_color='#AAFFAA'))
            else:
                self.noun_table.append(ctk.CTkLabel(self.f_noun_table, text="Plural",
                                                    padx=25, pady=12, bg_color='#AAFFAA'))
            grade += 1
        # Incorrect
        else:
            if self.noun[-1] == 0:
                self.noun_table.append(ctk.CTkLabel(self.f_noun_table, text="Plural",
                                                    padx=25, pady=12, bg_color='#FFAAAA'))
            else:
                self.noun_table.append(ctk.CTkLabel(self.f_noun_table, text="Not Plural",
                                                    padx=25, pady=12, bg_color='#FFAAAA'))

        # Display feedback
        for i in range(-1, -4, -1):
            self.noun_table[i].grid(column=abs(i + 1), row=1, sticky='WE')

        grade = grade/3  # Percentage
        # pts cap has not been hit
        if QuizManager.get_pts_cap(self.word) == 0:
            # Add pts, set pts cap
            QuizManager.set_pts(self.word, grade)

        # Display Button
        self.submit.destroy()
        # Also handles cooldown
        QuizManager.next_button(self.root_frame, self.f_submission, word_list, grade)
        return
