# Import python files
import json
import sqlite3
import random
import datetime
import customtkinter as ctk
from tkinter import ttk
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
    # c.execute("SELECT word, type FROM word_info WHERE new = 1")
    # Add new words to quiz list
    #word_list = c.fetchmany(2)  # Temporary

    # Select due words
    '''c.execute(f"Select word, type FROM word_info "
              f"WHERE cooldown <= {datetime.datetime.now().strftime('%Y%m%d')} AND new = 0")'''
    c.execute("SELECT word, type FROM word_info "
              "WHERE word = 'to eat' and type = 'passe_compose'")
    '''c.execute("SELECT word, type FROM word_info "
              "WHERE word = 'to speak'")'''

    word_list = c.fetchmany(1)
    print(word_list)
    #word_list += c.fetchall()#
    #word_list = c.fetchall()
    return word_list


def select_word(word, table):
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
    if word_list[rand_index][1] == 'noun':
        NounQuizPage.NounQuizPage(frame, [word_list, rand_index])
    elif word_list[rand_index][1] == 'adjective':
        AdjectivesQuizPage.AdjectivesQuizPage(frame, [word_list, rand_index])
    else:
        ConjugationQuizPage.ConjugationQuizPage(frame, [word_list, rand_index])


def remove_question(word_list, remove=True):
    if remove:
        rand_index = word_list[1]
        word_list = word_list[0]
        word_list.remove(word_list[rand_index])
    else:
        word_list = word_list[0]

    return word_list


def get_fonts():
    # Get theme & size info
    with open("settings.json", 'r') as file:
        settings = json.load(file)
    file.close()

    # Get font family
    with open(f"themes/{settings['color']}.json", 'r') as file:
        theme = json.load(file)
    file.close()

    font_family = theme['CTkFont']['Windows']['family']

    # Return body or title size
    font_size_body = theme['CTkFont']['Windows']['size']
    font_size_title = theme['CTkFont']['Windows']['title_size']

    return tuple((font_family, font_size_title, font_size_body))


def quiz_title(question_frame, font_title, word, new=False):
    if new:
        ctk.CTkLabel(question_frame, text="NEW", font=(font_title["family"], font_title["size"] - 10),
                     text_color='red').grid(column=0, row=0, pady=10)
        ctk.CTkLabel(question_frame, text=word, font=font_title).grid(column=0, row=1)
    else:
        ctk.CTkLabel(question_frame, text=word, font=font_title).grid(column=0, row=0)


def build_table(table_frame, font_body, props, widgets_num):
    table = []
    for num in range(0, widgets_num):
        if num % 2 == 0:
            table.append(ctk.CTkLabel(table_frame, text=props[num // 2], font=font_body, pady=12, padx=25))
            table[num].grid(column=0, row=num // 2)
        else:
            table.append(ctk.CTkEntry(table_frame, font=font_body))
            table[num].grid(column=1, row=num // 2)

    return table


def build_table_new_word(table_frame, font_body, props, widgets_num, word):
    for num in range(0, widgets_num):
        if num % 2 == 0:
            ctk.CTkLabel(table_frame, text=props[num // 2], font=font_body, pady=12, padx=25).grid(column=0, row=num)
        else:
            ctk.CTkLabel(table_frame, text=word[num // 2 + 1], font=font_body, pady=12, padx=25).grid(column=1, row=num - 1)
            ttk.Separator(table_frame, orient='horizontal').grid(column=0, row=num, sticky='ew')
            ttk.Separator(table_frame, orient='horizontal').grid(column=1, row=num, sticky='ew')

    return


def build_table_new_word_comp(table_frame, font_body, props, widgets_num, word):
    print(word)
    composite_verbs = get_composite_verbs(word)
    composite_question_table(table_frame, font_body, word, composite_verbs[0]).pack()
    ctk.CTkLabel(table_frame, text='').pack()
    ctk.CTkLabel(table_frame, text='').pack()
    composite_tense_table(table_frame, font_body, props, widgets_num, composite_verbs).pack()

    return


def composite_question_table(table_frame, font_body, word, inf_aux):
    ret_frame = ctk.CTkFrame(table_frame)
    ctk.CTkLabel(ret_frame, text='Tense', font=font_body, pady=12, padx=25).grid(column=0, row=0)
    ctk.CTkLabel(ret_frame, text='Auxiliaire', font=font_body, pady=12, padx=25).grid(column=1, row=0)
    ctk.CTkLabel(ret_frame, text='Participe Passé', font=font_body, pady=12, padx=25).grid(column=2, row=0)

    ttk.Separator(ret_frame, orient='horizontal').grid(columnspan=3, row=1, sticky='ew')

    ctk.CTkLabel(ret_frame, text=word[2].capitalize(), font=font_body, pady=12, padx=25).grid(column=0, row=2)
    ctk.CTkLabel(ret_frame, text=inf_aux, font=font_body, pady=12, padx=25).grid(column=1, row=2)
    ctk.CTkLabel(ret_frame, text=word[3], font=font_body, pady=12, padx=25).grid(column=2, row=2)

    return ret_frame


def composite_tense_table(table_frame, font_body, props, widgets_num, composite_verbs):
    ret_frame = ctk.CTkFrame(table_frame)
    column = 0
    i = 0
    for num in range(0, widgets_num):
        if num % 3 == 0:
            ctk.CTkLabel(ret_frame, text=props[num // 3], font=font_body, pady=12, padx=25).grid(column=0, row=num)
        else:
            ctk.CTkLabel(ret_frame, text=composite_verbs[i], font=font_body, pady=12, padx=25).grid(column=column,
                                                                                                    row=num - column)
            i += 1

        column += 1
        if column % 3 == 0:
            column = 0
            ttk.Separator(ret_frame, orient='horizontal').grid(columnspan=3, row=num, sticky='ew')

    return ret_frame


def get_composite_verbs(word):
    inf_participle = select_word(word[0], word[2])[1]
    aux = select_word(word[1], word[2])
    past_participle = word[3]

    composite = [aux[1], inf_participle]

    for i in range(2, len(aux)):
        composite.append(aux[i])
        composite.append(past_participle)

    return composite


def table_feedback(table_frame, font_body, table, word, widgets_num):
    # Open settings for feedback colors dependent on program appearance (light/dark)
    with open("settings.json", 'r') as file:
        settings = json.load(file)
    file.close()

    if settings["appearance"] == 'light':
        colors = settings["correct_feedback"][0], settings['incorrect_feedback'][0]
    else:
        colors = settings["correct_feedback"][1], settings['incorrect_feedback'][1]

    grade = 0
    for entry in range(1, widgets_num, 2):
        if table[entry].get() == word[-(-entry // 2)]:
            # Correct
            feedback = ctk.CTkLabel(table_frame, text=table[entry].get(), font=font_body, padx=25, pady=12, bg_color=colors[0])
            grade += 1
        else:
            # Incorrect
            feedback = ctk.CTkLabel(table_frame, text=table[entry].get(), font=font_body, padx=25, pady=12, bg_color=colors[1])
            # Correct Label
            ctk.CTkLabel(table_frame, text=word[-(-entry // 2)], font=font_body, padx=25, pady=12).grid(column=3, row=entry // 2)
        # Delete Entry to replace with feedback label
        table[entry].destroy()
        feedback.grid(column=1, row=(entry // 2), sticky='WE')  # 'we' fills area of feedback with color

    return grade/(widgets_num/2)  # percentage


def next_button(root_frame, font_body, sub_frame, word_list, grade):
    # Replace button
    done = ctk.CTkButton(sub_frame, text="Next", font=font_body)

    # 100% remove from list & set next due date
    if grade == 1:
        update_cooldown(word_list[0][word_list[1]][0])
        done.configure(command=lambda: reset_quiz_manager(root_frame, word_list))
    else:
        # Does not remove from word list
        done.configure(command=lambda: reset_quiz_manager(root_frame, word_list, remove=False))

    done.grid(column=0, row=0, sticky='S', pady=20)

    return


def submission_new_word(root_frame, font_body, sub_frame, word_list):
    word = word_list[0][word_list[1]][0]
    table = word_list[0][word_list[1]][1]
    remove_new_from_word(word, table)

    # Create button to leave page
    done = ctk.CTkButton(sub_frame, text="Next", font=font_body)
    # Does not remove from word list
    done.configure(command=lambda: reset_quiz_manager(root_frame, word_list, remove=False))
    done.grid(column=0, row=0, sticky='S', pady=20)
    return


def get_pts_cap(word):
    # Connect to database
    conn = sqlite3.connect('en_fr_words.db')
    # Create cursor
    c = conn.cursor()
    c.execute(f"SELECT pts_cap FROM word_info WHERE word = '{word}'")

    return c.fetchone()[0]  # Fetchone returns tuple with a null at end


def get_new_info(word, table):
    # Connect to database
    conn = sqlite3.connect('en_fr_words.db')
    # Create cursor
    c = conn.cursor()
    c.execute(f"SELECT new FROM word_info WHERE word = '{word}' and type = '{table}'")

    return c.fetchone()[0]  # Fetchone returns tuple with a null at end


def remove_new_from_word(word, table):
    # Connect to database
    conn = sqlite3.connect('en_fr_words.db')
    # Create cursor
    c = conn.cursor()
    c.execute(f"UPDATE word_info SET new = 0 WHERE word = '{word}' and type = '{table}'")
    # Commit changes and close db
    conn.commit()
    conn.close()
    return


def set_pts(word, pts):
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

    # Set pts_cap
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
