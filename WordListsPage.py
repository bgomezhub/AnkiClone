from tkinter import ttk
import customtkinter as ctk
import QuizManager
import Home
import sqlite3


class WordListsPage:
    def __init__(self, frame):
        # Fonts
        font = QuizManager.get_fonts()
        self.font_title = ctk.CTkFont(family=font[0], size=font[1])
        self.font_body = ctk.CTkFont(family=font[0], size=font[2])
        # Title
        self.root_frame = frame
        self.f_wl_title = ctk.CTkFrame(self.root_frame)
        self.f_wl_title.pack(padx=200, pady=25)
        ctk.CTkLabel(self.f_wl_title, text='Word Lists', font=self.font_title).pack()
        # Tabview for Word Lists
        self.f_wl_options = ctk.CTkFrame(self.root_frame)
        self.f_wl_options.pack(padx=200, pady=5)

        self.tabview = ctk.CTkTabview(self.f_wl_options)
        self.tabview.pack()
        self.tabview.add("Nouns")
        self.tabview.add("Adjectives")
        self.tabview.add("Conjugations")
        # Default section
        self.display_nouns()
        self.display_adjs()
        self.display_conjugations()

        # Submission
        self.f_submission = ctk.CTkFrame(self.root_frame)
        self.f_submission.pack()
        ctk.CTkButton(self.f_submission, text='Done', font=self.font_body,
                      command=lambda: self.submission()).grid(column=0, row=0, padx=200, pady=25, sticky='EW')

    def get_nouns(self):
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Select nouns
        c.execute(f"Select * FROM noun")
        noun_list = c.fetchall()

        return noun_list

    def display_nouns(self):
        # Show total number of nouns
        noun_list = self.get_nouns()
        ctk.CTkLabel(self.tabview.tab("Nouns"), text=f'Nouns: {len(noun_list)}').pack(pady=10)

        # Add scrollable frame as base of section
        f_nouns = ctk.CTkScrollableFrame(self.tabview.tab("Nouns"), border_width=3, border_color='#666666')
        f_nouns.pack(ipadx=55, ipady=50)

        # Display column names
        NOUNS_PROPS = ['English', 'French', 'Gender', 'Plural']
        for i in range(0, len(NOUNS_PROPS)):
            ctk.CTkLabel(f_nouns, text=NOUNS_PROPS[i]).grid(column=i, row = 0, padx=10, pady=10)
        ctk.CTkLabel(f_nouns, text='English').grid(column=0, row=0, padx=10, pady=10)
        ctk.CTkLabel(f_nouns, text='French').grid(column=1, row=0, padx=10, pady=10)
        ctk.CTkLabel(f_nouns, text='Gender').grid(column=2, row=0, padx=10, pady=10)
        ctk.CTkLabel(f_nouns, text='Plural').grid(column=3, row=0, padx=10, pady=10)
        # Add bar below column names and data
        separator = ctk.CTkFrame(f_nouns, fg_color='#666666', height=3)
        separator.grid(column=0, columnspan=5, row=1, sticky='ew')

        # Display noun_list data
        i = 8  # widget count
        for noun_row in noun_list:
            for noun_field in noun_row:
                # Plural check
                if i % 4 != 3:
                    ctk.CTkLabel(f_nouns, text=noun_field, justify='center').grid(
                        column=i % 4, row=i // 4, padx=10, pady=10)
                else:
                    # Display in english on plural column instead of 0 or 1
                    if noun_field == 1:
                        ctk.CTkLabel(f_nouns, text="Yes", justify='right').grid(
                            column=i % 4, row=i // 4, padx=10, pady=10)
                    else:
                        ctk.CTkLabel(f_nouns, text="No", justify='right').grid(
                            column=i % 4, row=i // 4, padx=10, pady=10)
                i += 1
            separator = ctk.CTkFrame(f_nouns, fg_color='#666666', height=3)
            separator.grid(column=0, columnspan=5, row=i//4, sticky='ew')
            i += 4

    def get_adjs(self):
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Select nouns
        c.execute(f"Select * FROM adjective")
        adj_list = c.fetchall()

        return adj_list

    def display_adjs(self):
        # Show total number of adjectives
        adj_list = self.get_adjs()
        ctk.CTkLabel(self.tabview.tab("Adjectives"), text=f'Adjectives: {len(adj_list)}').pack(pady=10)

        # Add scrollable frame as base of section
        f_adjs = ctk.CTkScrollableFrame(self.tabview.tab("Adjectives"), border_width=3, border_color='#666666')
        f_adjs.pack(ipadx=90, ipady=50)

        # Display column names
        ADJ_PROPS = ['English', 'Masc. S.', 'Masc. P.', 'Fem. S.', 'Fem. P.']
        for i in range(0, len(ADJ_PROPS)):
            ctk.CTkLabel(f_adjs, text=ADJ_PROPS[i]).grid(column=i, row=0, padx=10, pady=10)
        # Add bar below column names and data
        separator = ctk.CTkFrame(f_adjs, fg_color='#666666', height=3)
        separator.grid(column=0, columnspan=6, row=1, sticky='ew')

        # Display noun_list data
        i = 10  # widget count
        for adj_row in adj_list:
            for adjs_field in adj_row:
                ctk.CTkLabel(f_adjs, text=adjs_field, justify='center').grid(column=i % 5, row=i // 5, padx=10, pady=10)
                i += 1
            separator = ctk.CTkFrame(f_adjs, fg_color='#666666', height=3)
            separator.grid(column=0, columnspan=6, row=i // 5, sticky='ew')
            i += 5


    def get_conjugations(self):
        # Connect to database
        conn = sqlite3.connect('en_fr_words.db')
        # Create cursor
        c = conn.cursor()
        # Select nouns
        c.execute(f"Select * FROM present_verb")
        con_list = c.fetchall()

        return con_list

    def display_conjugations(self):
        # Show total number of conjugations
        con_list = self.get_conjugations()
        ctk.CTkLabel(self.tabview.tab("Conjugations"), text=f'Conjugations: {len(con_list)}').pack(pady=10)

        # Add scrollable frame as base of section
        f_cons = ctk.CTkScrollableFrame(self.tabview.tab("Conjugations"), border_width=3, border_color='#666666')
        f_cons.pack(ipadx=280, ipady=50)

        # Display column names
        CON_PROPS = ['English', 'Infinitive', 'Je', 'Tu', 'Il/Elle', 'Nous', 'Vous', 'Ils/Elles']
        for i in range(0, len(CON_PROPS)):
            ctk.CTkLabel(f_cons, text=CON_PROPS[i]).grid(column=i, row = 0, padx=10, pady=10)
        # Add bar below column names and data
        separator = ctk.CTkFrame(f_cons, fg_color='#666666', height=3)
        separator.grid(column=0, columnspan=9, row=1, sticky='ew')

        # Display noun_list data
        i = 16  # widget count
        for con_row in con_list:
            for adjs_field in con_row:
                ctk.CTkLabel(f_cons, text=adjs_field, justify='center').grid(column=i % 8, row=i // 8, padx=10, pady=10)
                i += 1
            separator = ctk.CTkFrame(f_cons, fg_color='#666666', height=3)
            separator.grid(column=0, columnspan=9, row=i // 8, sticky='ew')
            i += 8

    def submission(self):
        # destroy all objects of Word Lists page
        for widget in self.root_frame.winfo_children():
            widget.destroy()

        Home.Home(self.root_frame)

        return
