from tkinter import *
from math import floor


def define_conjugation_table(frame):
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


def display_conjugation_table(conjugation_table):
    i = 0
    while i < len(conjugation_table) - 1:
        for row in range(7):
            for column in range(2):
                conjugation_table[i].grid(column=column, row=row)
                i += 1


# Submit entries and receive feedback on performance
def submission(infinitive, conjugation_table, frame):
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
