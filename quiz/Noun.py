import json

import customtkinter as ctk
from tkinter import ttk

import Model
from controllers import Quiz


class Noun:
    def __init__(self, f_root, word_list):
        # Fonts
        font = Model.get_fonts()
        self.font_title = ctk.CTkFont(family=font[0], size=font[1])
        self.font_body = ctk.CTkFont(family=font[0], size=font[2])
        # Table Frame
        self.f_page = ctk.CTkScrollableFrame(f_root)
        self.f_page.pack(fill='both', expand=True)
        self.f_question = ctk.CTkFrame(self.f_page)
        self.f_question.pack(padx=200, pady=75)
        self.f_noun_table = ctk.CTkFrame(self.f_page)
        self.f_noun_table.pack(padx=200, pady=50)
        self.f_submission = ctk.CTkFrame(self.f_page)
        self.f_submission.pack(padx=200, pady=75)

        # Select noun
        self.word = word_list[0][word_list[1]][0]  # noun index
        self.table = word_list[0][word_list[1]][1]
        self.is_new = Model.get_new_info(self.word, self.table)
        self.noun = Model.get_word(self.word, self.table)

        # Properties of noun
        self.gen = ctk.StringVar()
        self.plural = ctk.IntVar()

        self.noun_table = []

        # Display new word or none new word
        if self.is_new == 1:
            # Define & Display nouns table
            self.define_noun_table_new_word()
            # New word, no pts/cap/cooldown
            Quiz.submission_button(self.f_page, self.f_submission, self.font_body, self.noun_table, word_list)
        else:
            # Define & Display nouns table
            self.define_noun_table()
            # Submission
            self.submit = ctk.CTkButton(self.f_submission, text="Submit", font=self.font_body,
                                        command=lambda: self.submission(word_list))
            self.submit.grid(column=0, row=2, columnspan=4, sticky='S', pady=20)

    def define_noun_table(self):
        # Define noun table
        # Define noun
        Quiz.quiz_title(self.f_question, self.font_title, self.word, self.table)

        # Define plurality
        ctk.CTkCheckBox(self.f_noun_table, text="Les", variable=self.plural, font=self.font_body,
                        onvalue=1, offvalue=0, width=90).grid(column=0, row=1)

        # Define gender
        ctk.CTkRadioButton(self.f_noun_table, text="Le", font=self.font_body, variable=self.gen,
                           value='le', width=70).grid(column=1, row=1)
        ctk.CTkRadioButton(self.f_noun_table, text="La", font=self.font_body, variable=self.gen,
                           value='la', width=70).grid(column=2, row=1)

        # Define Input box
        self.noun_table.append(ctk.CTkEntry(self.f_noun_table, font=self.font_body, width=90))
        self.noun_table[0].grid(column=3, row=1)
        return

    def define_noun_table_new_word(self):
        # Define noun title
        Quiz.quiz_title(self.f_question, self.font_title, self.word, self.table)

        # Get plurality from word, no SQL necessary since there is no info to gather.
        if self.noun[-1] == 0:
            ctk.CTkLabel(self.f_noun_table, text='Not Plural', font=self.font_body, padx=25, pady=12).grid(column=0, row=1)
        else:
            ctk.CTkLabel(self.f_noun_table, text='Plural', font=self.font_body, padx=25, pady=12).grid(column=0, row=1)

        # Add separator
        ttk.Separator(self.f_noun_table, orient='vertical').grid(column=1, row=1, sticky='ns')

        # Get gender from word NO SQL
        if self.noun[-2] == 'le':
            ctk.CTkLabel(self.f_noun_table, text='Le', font=self.font_body, padx=25, pady=12).grid(column=2, row=1)
        else:
            ctk.CTkLabel(self.f_noun_table, text='La', font=self.font_body, padx=25, pady=12).grid(column=2, row=1)

        # Add separator
        ttk.Separator(self.f_noun_table, orient='vertical').grid(column=3, row=1, sticky='ns')

        # Get word translation
        ctk.CTkLabel(self.f_noun_table, text=self.noun[-3], font=self.font_body, padx=25, pady=12).grid(column=4, row=1)
        return

    # Submit entries and receive feedback on performance
    def submission(self, word_list):
        # Open settings for feedback colors dependent on program appearance (light/dark)
        with open("./settings.json", 'r') as file:
            settings = json.load(file)
        file.close()

        if settings["appearance"] == 'light':
            colors = settings["correct_feedback"][0], settings['incorrect_feedback'][0]
        else:
            colors = settings["correct_feedback"][1], settings['incorrect_feedback'][1]

        grade = 0
        # Check fr translation
        if self.noun_table[0].get() == self.noun[1]:
            feedback = ctk.CTkLabel(self.f_noun_table, text=self.noun_table[0].get(), font=self.font_body,
                                    padx=25, pady=12, bg_color=colors[0])
            grade += 1
        else:
            ctk.CTkLabel(self.f_noun_table, text=self.noun[1], font=self.font_body, padx=25, pady=12).grid(column=4, row=1)
            feedback = ctk.CTkLabel(self.f_noun_table, text=self.noun_table[0].get(), font=self.font_body,
                                    padx=25, pady=12, bg_color=colors[1])
        self.noun_table[0].destroy()  # Clear Entry from screen
        # Clear list to gather info to be displayed
        self.noun_table.clear()
        self.noun_table.append(feedback)

        # Check gender
        # Correct
        if self.gen.get() == self.noun[-2]:
            self.noun_table.append(ctk.CTkLabel(self.f_noun_table, text=self.noun[-2], font=self.font_body,
                                                padx=25, pady=12, bg_color=colors[0]))
            grade += 1
        # Incorrect
        else:
            self.noun_table.append(ctk.CTkLabel(self.f_noun_table, text=self.gen.get(), font=self.font_body,
                                                padx=25, pady=12, bg_color=colors[1]))

        # Check Plurality
        # Correct
        if self.plural.get() == self.noun[-1]:
            if self.noun[-1] == 0:
                self.noun_table.append(ctk.CTkLabel(self.f_noun_table, text="Not Plural", font=self.font_body,
                                                    padx=25, pady=12, bg_color=colors[0]))
            else:
                self.noun_table.append(ctk.CTkLabel(self.f_noun_table, text="Plural", font=self.font_body,
                                                    padx=25, pady=12, bg_color=colors[0]))
            grade += 1
        # Incorrect
        else:
            if self.noun[-1] == 0:
                self.noun_table.append(ctk.CTkLabel(self.f_noun_table, text="Plural", font=self.font_body,
                                                    padx=25, pady=12, bg_color=colors[1]))
            else:
                self.noun_table.append(ctk.CTkLabel(self.f_noun_table, text="Not Plural", font=self.font_body,
                                                    padx=25, pady=12, bg_color=colors[1]))

        # Display feedback
        for i in range(-1, -4, -1):
            self.noun_table[i].grid(column=abs(i + 1), row=1, sticky='WE')

        grade = grade/3  # Percentage
        # pts cap has not been hit
        if Model.get_pts_cap(self.word, self.table) == 0:
            # Add pts, set pts cap
            Model.update_pts(self.word, self.table, grade)

        # Display Button
        self.submit.destroy()
        # Also handles cooldown
        Quiz.next_button(self.f_page, self.font_body, self.f_submission, word_list, grade)
        return
