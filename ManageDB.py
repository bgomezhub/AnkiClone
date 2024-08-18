from tkinter import *
import sqlite3

# Create Table
# Connect to database
#conn = sqlite3.connect('en_fr_words.db')
# Create cursor
#c = conn.cursor()
#c.execute("CREATE TABLE nouns ( en TEXT, fr TEXT, gender TEXT, plural INTEGER)")
#c.execute("CREATE TABLE adjectives ( en TEXT, masc TEXT, fem TEXT, mascp TEXT, femp TEXT)")
#c.execute("Select * from present_verb")
#c.execute('DELETE FROM present_verb WHERE infinitive_en=""')
#conn.commit()
#conn.close()
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
        self.nouns_table = []
        self.adjs_table = []

        # Start with conjugation table input
        self.current_section = 'con'
        self.con_manager(self.current_section)

        self.root.mainloop()

    # Display input table for specific section
    def section(self):
        Button(self.section_f, text="conjugations",
               command=lambda: self.con_manager(self.current_section)).grid(column=0, row=0, pady=10, sticky='NW')
        Button(self.section_f, text="nouns",
               command=lambda: self.nouns_manager(self.current_section)).grid(column=1, row=0, pady=10, sticky='NW')
        Button(self.section_f, text="adjectives",
               command=lambda: self.adjs_manager(self.current_section)).grid(column=2, row=0, pady=10, sticky='NW')

    def con_manager(self, current_section):
        # Remove current table if not conjugations
        if current_section == 'nouns':
            self.reset_manager('nouns', remove=True)
            self.reset_recent('nouns', remove=True)
        elif current_section == 'adjs':
            self.reset_manager('adjs', remove=True)
            self.reset_recent('adjs', remove=True)
        else:
            self.reset_recent('con', remove=True)

        # Update current_section
        self.current_section = 'con'

        # Define db manager for conjugations
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

        # Show recent inputs
        self.recent('con')
        return

    def nouns_manager(self, current_section):
        # Remove current table if not nouns
        if current_section == 'con':
            self.reset_manager('con', remove=True)
            self.reset_recent('con', remove=True)
        elif current_section == 'adjs':
            self.reset_manager('adjs', remove=True)
            self.reset_recent('adjs', remove=True)
        else:
            self.reset_recent('nouns', remove=True)

        # Update current_section
        self.current_section = 'nouns'

        # Define db manager for nouns
        nouns_req = ["English", "French", "Gender", "Plural"]
        for num in range(0, 8):
            if num % 2 == 0:
                self.nouns_table.append(Label(self.table_f, text=nouns_req[num//2], pady=8, padx=25))
                self.nouns_table[num].grid(column=0, row=num//2)
            else:
                self.nouns_table.append(Entry(self.table_f))
                self.nouns_table[num].grid(column=1, row=num // 2)

        # Submission button
        Button(self.table_f, text="submit",
               command=lambda: self.sub_nouns()).grid(columnspan=2, column=0, row=8, pady=10)

        # Show recent inputs
        self.recent('nouns')
        return

    def adjs_manager(self, current_section):
        # Remove current table if not adjectives
        if current_section == 'con':
            self.reset_manager('con', remove=True)
            self.reset_recent('con', remove=True)
        elif current_section == 'nouns':
            self.reset_manager('nouns', remove=True)
            self.reset_recent('nouns', remove=True)
        else:
            self.reset_recent('adjs', remove=True)

        # Update current_section
        self.current_section = 'adjs'

        # Define db manager for nouns
        adjs_req = ["English", "Masc. S.", "Fem. S.", "Masc. P.", "Fem. P."]
        for num in range(0, 10):
            if num % 2 == 0:
                self.adjs_table.append(Label(self.table_f, text=adjs_req[num // 2], pady=8, padx=25))
                self.adjs_table[num].grid(column=0, row=num // 2)
            else:
                self.adjs_table.append(Entry(self.table_f))
                self.adjs_table[num].grid(column=1, row=num // 2)

        # Submission button
        Button(self.table_f, text="submit",
               command=lambda: self.sub_adjs()).grid(columnspan=2, column=0, row=8, pady=10)

        # Show recent inputs
        self.recent('adjs')
        return

    # Clear all values for new input
    def reset_manager(self, frame, remove=False):
        for widget in self.table_f.winfo_children():
            widget.destroy()

        if frame == 'con':
            self.conjugation_table.clear()
            # If same section replace with itself
            if not remove:
                self.con_manager(self.current_section)
        elif frame == 'nouns':
            self.nouns_table.clear()
            # If same section replace with itself
            if not remove:
                self.nouns_manager(self.current_section)
        else:
            self.adjs_table.clear()
            # If same section replace with itself
            if not remove:
                self.adjs_manager(self.current_section)

        return

    def recent(self, frame):
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Select Table
        if frame == 'con':
            c.execute("SELECT * FROM present_verb ORDER BY rowid DESC")
        elif frame == 'nouns':
            c.execute("Select * from nouns ORDER BY rowid DESC")
        else:
            c.execute("SELECT * FROM adjectives ORDER BY rowid DESC")
        # Show recent inputs
        records = c.fetchmany(5)
        for record in records:
            Label(self.recent_f, text=record, pady=5, padx=5).pack()

        # Commit changes and close
        conn.commit()
        conn.close()
        return

    def reset_recent(self, frame, remove=False):
        # Delete & update the recent widget
        for widget in self.recent_f.winfo_children():
            widget.destroy()
        # Display appropriate recent depending on section
        if frame == 'con' and not remove:
            self.recent('con')
        elif frame == 'nouns' and not remove:
            self.recent('nouns')
        elif frame == 'adjs' and not remove:
            self.recent('adjs')

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
        self.reset_manager('con')

        return

    def sub_nouns(self):
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Insert values into database
        c.execute("INSERT INTO nouns VALUES (:en, :fr,:gender, :plural)", {
            'en': self.nouns_table[1].get(),
            'fr': self.nouns_table[3].get(),
            'gender': self.nouns_table[5].get(),
            'plural': self.nouns_table[7].get(),
            })
        # Commit changes and close db
        conn.commit()
        conn.close()

        # Clear the table and create it again
        self.reset_manager('nouns')

        return

    def sub_adjs(self):
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Insert values into database
        c.execute("INSERT INTO adjectives VALUES (:en, :masc,:fem, :mascp, :femp)", {
            'en': self.adjs_table[1].get(),
            'masc': self.adjs_table[3].get(),
            'fem': self.adjs_table[5].get(),
            'mascp': self.adjs_table[7].get(),
            'femp': self.adjs_table[9].get(),
        })
        # Commit changes and close db
        conn.commit()
        conn.close()

        # Clear the table and create it again
        self.reset_manager('adjs')

        return


ManageDB()
