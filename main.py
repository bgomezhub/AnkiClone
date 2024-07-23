from tkinter import *

root = Tk()

# Defining conjugation table
def define_conjugation_table():
    con_list = [Label(root, text="to_speak")]  # Placeholder
    con_subjects = ['Je', 'Tu', 'Il/Elle', 'Nous', 'Vous', 'Ils/Elles']
    i = 0
    for num in range(1, 14):
        if num % 2 == 0:
            con_list.append(Label(root, text=con_subjects[i]))
            i += 1
        else:
            con_list.append(Entry(root))
    return con_list


conjugation_table = define_conjugation_table()
# Display conjugation table
i = 0
while i < len(conjugation_table) - 1:
    for row in range(7):
        for column in range(2):
            conjugation_table[i].grid(column=column, row=row)
            i += 1

root.mainloop()
