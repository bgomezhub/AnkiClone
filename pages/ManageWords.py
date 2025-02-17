import tkinter
import customtkinter as ctk
import sqlite3
import Model
import controllers.Quiz


class ManageWords:
    def __init__(self, frame):
        self.font_body = Model.get_fonts()[0:3:2]
        # Define frames, section->table->recent
        self.root = frame
        self.f_section = ctk.CTkFrame(self.root)
        self.f_section.pack(pady=5)
        self.f_table = ctk.CTkFrame(self.root)
        self.f_table.pack(pady=20)
        self.f_recent = ctk.CTkFrame(self.root)
        self.f_recent.pack()
        # Initiate class variables
        self.section()
        self.conjugation_table = []
        self.nouns_table = []
        self.adjs_table = []

        # Start with conjugation table input
        self.current_section = 'con'
        self.con_manager(self.current_section)

    # Display input table for specific section
    def section(self):
        ctk.CTkButton(self.f_section, text="Conjugations",
                      command=lambda: self.con_manager(self.current_section)).grid(column=0, row=0, padx=1, pady=10)
        ctk.CTkButton(self.f_section, text="Nouns",
                      command=lambda: self.nouns_manager(self.current_section)).grid(column=1, row=0, padx=1, pady=10)
        ctk.CTkButton(self.f_section, text="Adjectives",
                      command=lambda: self.adjs_manager(self.current_section)).grid(column=2, row=0, padx=1, pady=10)

    def con_manager(self, current_section):
        # Reset page
        self.reset_manager(current_section, remove=True)
        self.reset_recent(current_section, remove=True)

        # Update current_section
        self.current_section = 'con'

        # Define db manager for conjugations
        con_subjects = ["infinitive en", "infinitive fr", "I", "you", "he/she", "we", "you(formal)", "they"]
        self.conjugation_table = controllers.Quiz.build_table_old_word(self.f_table, self.font_body, con_subjects, 16)

        # Submission button
        ctk.CTkButton(self.f_table, text="submit",
                      command=lambda: self.sub_con()).grid(columnspan=2, column=0, row=8, pady=20)

        # Show recent inputs
        self.recent('con')
        return

    def nouns_manager(self, current_section):
        # Reset page
        self.reset_manager(current_section, remove=True)
        self.reset_recent(current_section, remove=True)

        # Update current_section
        self.current_section = 'nouns'

        # Define db manager for nouns
        nouns_req = ["English", "French"]
        self.nouns_table = controllers.Quiz.build_table_old_word(self.f_table, self.font_body, nouns_req, 4)[1::2]
        gender = tkinter.StringVar(value='le')
        plural = tkinter.IntVar(value=0)

        self.nouns_table.append(gender)
        self.nouns_table.append(plural)

        ctk.CTkLabel(self.f_table, text="Gender").grid(column=0, row=3, padx=1, pady=10)
        ctk.CTkRadioButton(self.f_table, font=self.font_body, text="Le", variable=gender, value='le').grid(column=1, row=3, padx=1, pady=10)
        ctk.CTkRadioButton(self.f_table, font=self.font_body, text="La", variable=gender, value='la').grid(column=2, row=3, padx=1, pady=10)

        ctk.CTkLabel(self.f_table, text="Plural").grid(column=0, row=4, padx=1, pady=10)
        ctk.CTkRadioButton(self.f_table, font=self.font_body, text="No", variable=plural, value=0).grid(column=1, row=4, padx=1, pady=10)
        ctk.CTkRadioButton(self.f_table, font=self.font_body, text="Yes", variable=plural, value=1).grid(column=2, row=4, padx=1, pady=10)

        # Submission button
        ctk.CTkButton(self.f_table, text="submit",
                      command=lambda: self.sub_nouns()).grid(columnspan=2, column=0, row=8, pady=20)

        # Show recent inputs
        self.recent('nouns')
        return

    def adjs_manager(self, current_section):
        # Reset page
        self.reset_manager(current_section, remove=True)
        self.reset_recent(current_section, remove=True)

        # Update current_section
        self.current_section = 'adjs'

        # Define db manager for nouns
        adjs_req = ["English", "Masc. S.", "Fem. S.", "Masc. P.", "Fem. P."]
        self.adjs_table = controllers.Quiz.build_table_old_word(self.f_table, self.font_body, adjs_req, 10)

        # Submission button
        ctk.CTkButton(self.f_table, text="submit",
                      command=lambda: self.sub_adjs()).grid(columnspan=2, column=0, row=8, pady=20)

        # Show recent inputs
        self.recent('adjs')

        return

    # Clear all values for new input
    def reset_manager(self, current_section, remove=False):
        for widget in self.f_table.winfo_children():
            widget.destroy()

        # Clear table (list) depending on current section
        # Load page for section
        if current_section == 'con':
            self.conjugation_table.clear()
            # If same section replace with itself
            if not remove:
                self.con_manager(self.current_section)
        elif current_section == 'nouns':
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
        conn = sqlite3.connect('./en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Select Table
        if frame == 'con':
            c.execute("SELECT * FROM present ORDER BY rowid DESC")
        elif frame == 'nouns':
            c.execute("Select * from noun ORDER BY rowid DESC")
        else:
            c.execute("SELECT * FROM adjective ORDER BY rowid DESC")
        # Show recent inputs
        records = c.fetchmany(5)
        ctk.CTkButton(self.f_recent, text=records[0],
                      command=lambda: self.delete_recent_entry(records[0])).pack(pady=5, padx=5, fill='x')
        ctk.CTkButton(self.f_recent, text=records[1],
                      command=lambda: self.delete_recent_entry(records[1])).pack(pady=5, padx=5, fill='x')
        ctk.CTkButton(self.f_recent, text=records[2],
                      command=lambda: self.delete_recent_entry(records[2])).pack(pady=5, padx=5, fill='x')
        ctk.CTkButton(self.f_recent, text=records[3],
                      command=lambda: self.delete_recent_entry(records[3])).pack(pady=5, padx=5, fill='x')
        ctk.CTkButton(self.f_recent, text=records[4],
                      command=lambda: self.delete_recent_entry(records[4])).pack(pady=5, padx=5, fill='x')

        conn.close()

        return

    def delete_recent_entry(self, del_entry):
        # Connect to database
        conn = sqlite3.connect('./en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Get table name
        table_name = {"adjs": "adjective", "con": "present", "nouns": "noun"}
        table_name = table_name[self.current_section]

        # Insert values into database
        # en is the first column of every table that is not word_info
        c.execute(f"DELETE FROM {table_name} WHERE en = '{del_entry[0]}'")
        c.execute(f"DELETE FROM word_info WHERE word = '{del_entry[0]}'")

        # Commit changes and close db
        conn.commit()
        conn.close()

        self.reset_recent(self.current_section)

        return


    def reset_recent(self, current_section, remove=False):
        # Delete & update the recent widget
        for widget in self.f_recent.winfo_children():
            widget.destroy()

        # Display appropriate recent depending on section
        if current_section == 'con' and not remove:
            self.recent('con')
        elif current_section == 'nouns' and not remove:
            self.recent('nouns')
        elif current_section == 'adjs' and not remove:
            self.recent('adjs')

        return

    def sub_con(self):
        # Connect to database
        conn = sqlite3.connect('./en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Insert values into database
        c.execute("INSERT INTO present VALUES (:en, :fr,:i, :you, :he_she, :we, :you_formal, :they)", {
            'en': self.conjugation_table[1].get(),
            'fr': self.conjugation_table[3].get(),
            'i': self.conjugation_table[5].get(),
            'you': self.conjugation_table[7].get(),
            'he_she': self.conjugation_table[9].get(),
            'we': self.conjugation_table[11].get(),
            'you_formal': self.conjugation_table[13].get(),
            'they': self.conjugation_table[15].get(),
            })
        c.execute("INSERT INTO word_info VALUES (:word, :type, :new, :pts, :cooldown, :pts_cap)", {
            'word': self.conjugation_table[1].get(),
            'type': 'indicatif_present',
            'new': 1,
            'pts': 0,
            'cooldown': '20240101',
            'pts_cap': 0,
        })

        # Commit changes and close db
        conn.commit()
        conn.close()

        # Clear the table and create it again
        self.reset_manager('con')

        return

    def sub_nouns(self):
        # Connect to database
        conn = sqlite3.connect('./en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Insert values into database
        c.execute("INSERT INTO noun VALUES (:en, :fr,:gender, :plural)", {
            'en': self.nouns_table[0].get(),
            'fr': self.nouns_table[1].get(),
            'gender': self.nouns_table[2].get(),
            'plural': self.nouns_table[3].get(),
            })
        c.execute("INSERT INTO word_info VALUES (:word, :type, :new, :pts, :cooldown, :pts_cap)", {
            'word': self.nouns_table[1].get(),
            'type': 'noun',
            'new': 1,
            'pts': 0,
            'cooldown': '20240101',
            'pts_cap': 0,
        })
        # Commit changes and close db
        conn.commit()
        conn.close()

        # Clear the table and create it again
        self.reset_manager('nouns')

        return

    def sub_adjs(self):
        # Connect to database
        conn = sqlite3.connect('./en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Insert values into database
        c.execute("INSERT INTO adjective VALUES (:en, :masc,:fem, :mascp, :femp)", {
            'en': self.adjs_table[1].get(),
            'masc': self.adjs_table[3].get(),
            'fem': self.adjs_table[5].get(),
            'mascp': self.adjs_table[7].get(),
            'femp': self.adjs_table[9].get(),
        })
        c.execute("INSERT INTO word_info VALUES (:word, :type, :new, :pts, :cooldown, :pts_cap)", {
            'word': self.adjs_table[1].get(),
            'type': 'adjective',
            'new': 1,
            'pts': 0,
            'cooldown': '20240101',
            'pts_cap': 0,
        })
        # Commit changes and close db
        conn.commit()
        conn.close()

        # Clear the table and create it again
        self.reset_manager('adjs')

        return
