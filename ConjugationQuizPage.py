from tkinter import *
from math import floor


class ConjugationQuizPage:
    def __init__(self, frame):
        # Table Frame
        f_conjugation_table = Frame(frame)
        f_conjugation_table.grid(column=0, row=0, padx=200, pady=150)

        # conjugation to be
        conjugations = {'To be': ['Etre', 'suis', 'es', 'est', 'sommes', 'etes', 'sont']}  # Placeholder

        # Define & Display conjugation table
        conjugation_table = self.define_conjugation_table(f_conjugation_table)
        self.display_conjugation_table(conjugation_table)

        # Submission
        submit = Button(f_conjugation_table, text="Submit")
        submit['command']=lambda b=submit: self.submission(
            conjugations['To be'], conjugation_table, f_conjugation_table, b)  # Self reference to delete itself
        submit.grid(column=0, row=8, columnspan=2, sticky='S', pady=20)  # Padding between table & button


    def define_conjugation_table(self, frame):
        con_list = [Label(frame, text="To be")]  # Placeholder
        con_subjects = ['Je', 'Tu', 'Il/Elle', 'Nous', 'Vous', 'Ils/Elles']  # Placeholder
        i = 0
        for num in range(1, 14):
            if num % 2 == 0:
                con_list.append(Label(frame, text=con_subjects[i], pady=8, padx=25))
                i += 1
            else:
                con_list.append(Entry(frame))
        return con_list

    def display_conjugation_table(self, conjugation_table):
        i = 0
        while i < len(conjugation_table) - 1:
            for row in range(7):
                for column in range(2):
                    conjugation_table[i].grid(column=column, row=row)
                    i += 1

    # Submit entries and receive feedback on performance
    def submission(self, infinitive, conjugation_table, frame, b):
        i = 0
        for entry in range(1,14,2):
            if conjugation_table[entry].get() == infinitive[i]:
                feedback = Label(frame, text=conjugation_table[entry].get(),
                                 padx=40, pady=10, bg='#AAFFAA')  # Correct
            else:
                feedback = Label(frame, text=conjugation_table[entry].get(),
                                 padx=20, pady=10, bg='#FFAAAA')  # Incorrect
            # Delete Entry to replace with feedback label
            conjugation_table[entry].destroy()
            feedback.grid(column=1, row=floor(entry / 2), sticky='WE')  # 'we' fills area of feedback with color
            i += 1

        b.destroy()
        Button(frame, text="Done", command=quit).grid(column=0, row=8, columnspan=2, sticky='S', pady=20)
