from tkinter import *
import sqlite3

# Create Table
#c.execute(
# "CREATE TABLE present_verb (
#   infinitive_en TEXT, infinitive_fr TEXT, i TEXT, you TEXT, he_she TEXT, we TEXT, you_formal TEXT, they TEXT)")

#c.execute('DELETE FROM present_verb WHERE infinitive_en="to speak"')
#c.execute('SELECT * FROM present_verb')
#print(c.fetchall())


class ManageDB:
    def __init__(self):
        # Define the page
        self.root = Tk()
        self.conjugation_table = []
        self.db_manager()

        # Submission button
        Button(self.root, text="submit",
              command=lambda: self.submission()).grid(columnspan=2, column=0, row=8, pady=10)

        # Show recent inputs
        self.recent()

        self.root.mainloop()

    def db_manager(self):
        # Define db manager
        con_subjects = ["infinitive en", "infinitive fr", "I", "you", "he/she", "we", "you(formal)", "they"]
        for num in range(0, 16):
            if num % 2 == 0:
                self.conjugation_table.append(Label(self.root, text=con_subjects[num//2], pady=8, padx=25))
                self.conjugation_table[num].grid(column=0, row=num//2)
            else:
                self.conjugation_table.append(Entry(self.root))
                self.conjugation_table[num].grid(column=1, row=num//2)

    def recent(self):
        r_frame = Frame(self.root)
        r_frame.grid(column=0, columnspan=2, row=9)
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Select Table
        c.execute("SELECT * FROM present_verb ORDER BY rowid DESC")
        # Show recent inputs
        records = c.fetchmany(5)
        for record in records:
            Label(r_frame, text=record, pady=5, padx=5).grid(column=0, row=0)
            print(record)

        # Commit changes and close
        conn.commit()
        conn.close()
        return

    def submission(self):
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

        # Commit changes and close
        conn.commit()
        conn.close()
        return



ManageDB()
