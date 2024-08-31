# Import python files
import sqlite3
import random
import datetime
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


def reset_quiz_manager(root_frame, word_list):
    for widget in root_frame.winfo_children():
        widget.destroy()

    word_list = remove_question(word_list)
    return next_question(root_frame, word_list)
