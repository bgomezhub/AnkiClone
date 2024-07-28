from tkinter import *
import ConjugationQuizPage as cqp
from math import floor

# Define root widget
root = Tk()
f_conjugation_table = Frame(root)
f_conjugation_table.grid(column=0, row=0, padx=200, pady=150)

# conjugation to be
conjugations = {'To be': ['Etre', 'suis', 'es', 'est', 'sommes', 'etes', 'sont']}  # Placeholder

# Define & Display conjugation table
conjugation_table = cqp.define_conjugation_table(f_conjugation_table)  # Create list of table labels/entries
cqp.display_conjugation_table(conjugation_table)

# Submission
submit = Button(
    f_conjugation_table, text="Submit",
    command=lambda: cqp.submission(conjugations['To be'], conjugation_table, f_conjugation_table))
submit.grid(column=0, row=8, columnspan=2,sticky='S', pady=20)  # Padding between table & button

root.mainloop()
