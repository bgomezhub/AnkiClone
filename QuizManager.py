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
    #word_list = c.fetchmany(1)#  # Temporary

    # Select due words
    c.execute(f"Select * FROM word_info "
              f"WHERE cooldown <= {datetime.datetime.now().strftime('%Y%m%d')} AND new = 0")
    #word_list += c.fetchall()#
    word_list = c.fetchall()
    print(word_list)
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


def next_question(frame, word_list):
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


def remove_question(word_list, remove=True):
    if remove:
        rand_index = word_list[1]
        word_list = word_list[0]
        word_list.remove(word_list[rand_index])
    else:
        word_list = word_list[0]

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
    grade = 0
    for entry in range(1, widgets_num, 2):
        if table[entry].get() == word[-(-entry // 2)]:
            feedback = ctk.CTkLabel(table_frame, text=table[entry].get(), font=font,
                                    padx=25, pady=12, bg_color='#AAFFAA')  # Correct
            grade += 1
        else:
            feedback = ctk.CTkLabel(table_frame, text=table[entry].get(), font=font,
                                    padx=25, pady=12, bg_color='#FFAAAA')  # Incorrect
            # Correct Label
            ctk.CTkLabel(table_frame, text=word[-(-entry // 2)], font=font,
                         padx=25, pady=12).grid(column=3, row=entry // 2)
        # Delete Entry to replace with feedback label
        table[entry].destroy()
        feedback.grid(column=1, row=(entry // 2), sticky='WE')  # 'we' fills area of feedback with color

    return grade/(widgets_num/2)


def get_pts_cap(word):
    # Connect to database
    conn = sqlite3.connect('en_fr_words.db')
    # Create cursor
    c = conn.cursor()
    c.execute(f"SELECT pts_cap FROM word_info WHERE word = '{word}'")

    return c.fetchone()[0]  # Fetchone returns tuple with a null at end


def update_pts(word, pts):
    # Select all in a list
    # Connect to database
    conn = sqlite3.connect('en_fr_words.db')
    # Create cursor
    c = conn.cursor()
    # calculate pts
    pts = pts * 20 - 10  # +- 10 pts, 50% results in 0

    # pts will not be lost further if below zero
    c.execute(f"SELECT pts from word_info WHERE word = '{word}'")
    if not (c.fetchone()[0] < 0 and pts < 0):
        c.execute(f"UPDATE word_info SET pts = (pts + {pts}) WHERE word = '{word}'")

    #
    c.execute(f"UPDATE word_info SET pts_cap = 1 WHERE word = '{word}'")
    # Commit changes and close db
    conn.commit()
    conn.close()
    return


def calculate_cooldown(pts):
    if pts < 15:
        return 1
    elif pts < 30:
        return 2
    elif pts < 50:
        return 5
    elif pts < 70:
        return 7
    elif pts < 90:
        return 9
    elif pts < 100:
        return 11
    else:
        return 13


def update_cooldown(word):
    # Connect to database
    conn = sqlite3.connect('en_fr_words.db')
    # Create cursor
    c = conn.cursor()

    # Calculate cooldown based off pts
    c.execute(f"SELECT pts FROM word_info WHERE word = '{word}'")
    cd = calculate_cooldown(c.fetchone()[0])  # fetchone returns tuple here
    # Add cooldown to today's date
    cd = datetime.datetime.now() + datetime.timedelta(days=cd)
    # format YYYYMMDD
    cd = cd.strftime("%Y%m%d")
    # Update Table
    c.execute(f"UPDATE word_info SET cooldown = '{cd}' WHERE word = '{word}'")
    c.execute(f"UPDATE word_info set pts_cap = 0 WHERE word = '{word}'")

    # Commit changes and close db
    conn.commit()
    conn.close()
    return


def reset_quiz_manager(root_frame, word_list, remove=True):
    # Destroy all widgets on screen
    for widget in root_frame.winfo_children():
        widget.destroy()

    # Remove from list
    if remove:
        word_list = remove_question(word_list)
    else:
        word_list = remove_question(word_list, remove=False)

    return next_question(root_frame, word_list)
