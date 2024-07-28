from tkinter import *
from math import floor


def define_conjugation_table():
    con_list = [Label(f_conjugation_table, text="To be")]  # Placeholder
    con_subjects = ['Je', 'Tu', 'Il/Elle', 'Nous', 'Vous', 'Ils/Elles']
    i = 0
    for num in range(1, 14):
        if num % 2 == 0:
            con_list.append(Label(f_conjugation_table, text=con_subjects[i], pady=8, padx=25))
            i += 1
        else:
            con_list.append(Entry(f_conjugation_table))
    return con_list


def display_conjugation_table(conjugation_table):
    i = 0
    while i < len(conjugation_table) - 1:
        for row in range(7):
            for column in range(2):
                conjugation_table[i].grid(column=column, row=row)
                i += 1


# Submit entries and receive feedback on performance
def submission(infinitive, conjugation_table):
    i = 0
    for entry in range(1,14,2):
        if conjugation_table[entry].get() == infinitive[i]:
            feedback = Label(f_conjugation_table, text=conjugation_table[entry].get(),
                             padx=40, pady=10, bg='#AAFFAA')  # Correct
        else:
            feedback = Label(f_conjugation_table, text=conjugation_table[entry].get(),
                             padx=20, pady=10, bg='#FFAAAA')  # Incorrect
        conjugation_table[entry].destroy()
        feedback.grid(column=1, row=floor(entry / 2), sticky='WE')
        i += 1


# Define root widget
root = Tk()
f_conjugation_table = Frame(root)
f_conjugation_table.grid(column=0, row=0, padx=200, pady=150)

# conjugation to be
conjugations = {'To be': ['Etre', 'suis', 'es', 'est', 'sommes', 'etes', 'sont']}  # Placeholder

# Define & Display conjugation table
conjugation_table = define_conjugation_table()
display_conjugation_table(conjugation_table)

# Submission
submit = Button(
    f_conjugation_table, text="Submit", command=lambda: submission(conjugations['To be'], conjugation_table))
submit.grid(column=0, row=8, columnspan=2,sticky='S', pady=20)  # Padding between table & button

root.mainloop()
