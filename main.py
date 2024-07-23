from tkinter import *

root = Tk()

# Defining conjugation table
en_infinitive = Entry(root)
fr_infinitive = Entry(root)
en_i = Entry(root)
fr_i = Entry(root)
en_you = Entry(root)
fr_you = Entry(root)
en_he_she = Entry(root)
fr_he_she = Entry(root)
en_we = Entry(root)
fr_we = Entry(root)
en_you_formal = Entry(root)
fr_you_formal = Entry(root)
en_they = Entry(root)
fr_they = Entry(root)

# Display conjugation table
en_infinitive.grid(column=0, row=0)
fr_infinitive.grid(column=1, row=0)
en_i.grid(column=0, row=1)
fr_i.grid(column=1, row=1)
en_you.grid(column=0, row=2)
fr_you.grid(column=1, row=2)
en_he_she.grid(column=0, row=3)
fr_he_she.grid(column=1, row=3)
en_we.grid(column=0, row=4)
fr_we.grid(column=1, row=4)
en_you_formal.grid(column=0, row=5)
fr_you_formal.grid(column=1, row=5)
en_they.grid(column=0, row=6)
fr_they.grid(column=1, row=6)


root.mainloop()
