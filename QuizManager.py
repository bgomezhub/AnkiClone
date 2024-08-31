# Import python files
import sqlite3
import random
import datetime
import customtkinter as ctk
# Import quiz Pages
import ConjugationQuizPage
import NounQuizPage
import AdjectivesQuizPage
import FinishPage


def select_questions():
    # Select all in a list
    # Connect to database
    conn = sqlite3.connect('en_fr_words.db')
    # Create cursor
    c = conn.cursor()

    # Select new words
    c.execute("SELECT * FROM word_info WHERE new = 1")
    # Add new words to quiz list
    word_list = c.fetchmany(1)  # Temporary

    # Select due words
    c.execute(f"Select * FROM word_info "
              f"WHERE cooldown <= {datetime.datetime.now().strftime('%Y%m%d')} AND new = 0")
    word_list += c.fetchall()
    return word_list


def select_word(table, word):
    # Select all in a list
    # Connect to database
    conn = sqlite3.connect('en_fr_words.db')
    # Create cursor
    c = conn.cursor()
    # Select Table
    c.execute(f"SELECT * FROM {table} WHERE en = '{word}'")
    # return selected word
    return c.fetchone()


def next_question(frame, word_list, remove_word=None):
    # Base condition
    if len(word_list) == 0:
        return FinishPage.FinishPage(frame)

    # Randomize next word
    rand_index = random.randint(0, len(word_list) - 1)
    # Send to corresponding page
    if word_list[rand_index][1] == 'present_verb':
        ConjugationQuizPage.ConjugationQuizPage(frame, [word_list, rand_index])
    elif word_list[rand_index][1] == 'noun':
        NounQuizPage.NounQuizPage(frame, [word_list, rand_index])
    elif word_list[rand_index][1] == 'adjective':
        AdjectivesQuizPage.AdjectivesQuizPage(frame, [word_list, rand_index])


def remove_question(word_list):
    rand_index = word_list[1]
    word_list = word_list[0]
    word_list.remove(word_list[rand_index])

    return word_list


def build_table(table_frame, font, props, widgets_num):
    table = []
    for num in range(0, widgets_num):
        if num % 2 == 0:
            table.append(ctk.CTkLabel(table_frame, text=props[num // 2], font=font,  pady=12, padx=25))
            table[num].grid(column=0, row=num // 2)
        else:
            table.append(ctk.CTkEntry(table_frame))
            table[num].grid(column=1, row=num // 2)

    return table


def table_feedback(table_frame, table, font, word, widgets_num):
    for entry in range(1, widgets_num, 2):
        if table[entry].get() == word[-(-entry // 2)]:
            feedback = ctk.CTkLabel(table_frame, text=table[entry].get(), font=font,
                                    padx=25, pady=12, bg_color='#AAFFAA')  # Correct
        else:
            feedback = ctk.CTkLabel(table_frame, text=table[entry].get(), font=font,
                                    padx=25, pady=12, bg_color='#FFAAAA')  # Incorrect
            # Correct Label
            ctk.CTkLabel(table_frame, text=word[-(-entry // 2)], font=font,
                         padx=25, pady=12).grid(column=3, row=entry // 2)
        # Delete Entry to replace with feedback label
        table[entry].destroy()
        feedback.grid(column=1, row=(entry // 2), sticky='WE')  # 'we' fills area of feedback with color


def reset_quiz_manager(root_frame, word_list):
    for widget in root_frame.winfo_children():
        widget.destroy()

    word_list = remove_question(word_list)
    return next_question(root_frame, word_list)
