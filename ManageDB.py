from tkinter import *
import sqlite3

# Create Table
# Connect to database
#conn = sqlite3.connect('en_fr_words.db')
# Create cursor
#c = conn.cursor()
#c.execute("CREATE TABLE nouns ( en TEXT, fr TEXT, gender TEXT, plural INTEGER)")

#c.execute('DELETE FROM present_verb WHERE infinitive_en="to speak"')
#c.execute('SELECT * FROM present_verb')
#print(c.fetchall())


class ManageDB:
    def __init__(self):
        # Define frames, section->table->recent
        self.root = Tk()
        self.section_f = Frame(self.root)
        self.section_f.grid(column=0, row=0)
        self.table_f = Frame(self.root)
        self.table_f.grid(column=0, row=1)
        self.recent_f = Frame(self.root)
        self.recent_f.grid(column=0, row=2)
        # Initiate class variables
        self.section()
        self.conjugation_table = []
        self.noun_table = []
        self.con_manager()

        # Show recent inputs
        self.recent()

        self.root.mainloop()

    def con_manager(self):
        # Define db manager
        con_subjects = ["infinitive en", "infinitive fr", "I", "you", "he/she", "we", "you(formal)", "they"]
        for num in range(0, 16):
            if num % 2 == 0:
                self.conjugation_table.append(Label(self.table_f, text=con_subjects[num//2], pady=8, padx=25))
                self.conjugation_table[num].grid(column=0, row=num//2)
            else:
                self.conjugation_table.append(Entry(self.table_f))
                self.conjugation_table[num].grid(column=1, row=num//2)
        # Submission button
        Button(self.table_f, text="submit",
               command=lambda: self.sub_con()).grid(columnspan=2, column=0, row=8, pady=10)

    def noun_manager(self):
        #c.execute("CREATE TABLE nouns ( en TEXT, fr TEXT, gender TEXT, plural INTEGER)")
        noun_req = ["English", "French", "Gender", "Plural"]
        for num in range(0, 8):
            if num % 2 == 0:
                self.noun_table.append(Label(self.table_f, text=noun_req[num//2]))
                self.noun_table[num].grid(column=0, row=num//2)
            else:
                self.noun_table.append(Entry(self.table_f))
                self.noun_table[num].grid(column=1, row=num // 2)


    def section(self):
        conjugations = Button(self.section_f, text="conjugations",
              command=lambda: self.con_manager()).grid(column=0, row=0, pady=10, sticky='NW')
        nouns = Button(self.section_f, text="nouns",
              command=lambda: self.noun_manager()).grid(column=1, row=0, pady=10, sticky='NW')

    def recent(self):
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Select Table
        c.execute("SELECT * FROM present_verb ORDER BY rowid DESC")
        # Show recent inputs
        records = c.fetchmany(5)
        for record in records:
            Label(self.recent_f, text=record, pady=5, padx=5).pack()

        # Commit changes and close
        conn.commit()
        conn.close()
        return

    def sub_con(self):
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Insert values into database
        c.execute("INSERT INTO present_verb VALUES (:infinitive_en, :infinitive_fr,:i, :you, :he_she, :we, :you_formal, :they)", {
            'infinitive_en': self.conjugation_table[1].get(),
            'infinitive_fr': self.conjugation_table[3].get(),
            'i': self.conjugation_table[5].get(),
            'you': self.conjugation_table[7].get(),
            'he_she': self.conjugation_table[9].get(),
            'we': self.conjugation_table[11].get(),
            'you_formal': self.conjugation_table[13].get(),
            'they': self.conjugation_table[15].get(),
            })

        # Commit changes and close db
        conn.commit()
        conn.close()

        # Clear the table and create it again
        for item in self.conjugation_table:
            item.destroy()
        self.conjugation_table.clear()
        self.con_manager()

        # Delete & update the recent widget
        for widget in self.recent_f.winfo_children():
            widget.destroy()
        self.recent()

        return


ManageDB()
