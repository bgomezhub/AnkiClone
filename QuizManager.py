# Import python files
import json
import sqlite3
import random
import datetime
import tkinter
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


def next_question(f_root, word_list):
    # Base condition
    if len(word_list) == 0:
        return FinishPage.FinishPage(f_root)

    # Randomize next word
    rand_index = random.randint(0, len(word_list) - 1)
    # Send to corresponding page
    if word_list[rand_index][1] == 'noun':
        NounQuizPage.NounQuizPage(f_root, [word_list, rand_index])
    elif word_list[rand_index][1] == 'adjective':
        AdjectivesQuizPage.AdjectivesQuizPage(f_root, [word_list, rand_index])
    else:
        ConjugationQuizPage.ConjugationQuizPage(f_root, [word_list, rand_index])


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
    settings = get_settings()

    # Get font family
    with open(f"themes/{settings['color']}.json", 'r') as file:
        theme = json.load(file)
    file.close()

    font_family = theme['CTkFont']['Windows']['family']

    # Return body or title size
    font_size_body = theme['CTkFont']['Windows']['size']
    font_size_title = theme['CTkFont']['Windows']['title_size']

    return tuple((font_family, font_size_title, font_size_body))


def get_settings():
    with open("settings.json", 'r') as file:
        settings = json.load(file)
    file.close()

    return settings


def quiz_title(f_question, font_title, word, table):
    is_new = get_new_info(word, table)

    if is_new:
        ctk.CTkLabel(f_question, text="NEW", font=(font_title["family"], font_title["size"] - 10),
                     text_color='red').grid(column=0, row=0, pady=10)
        ctk.CTkLabel(f_question, text=word, font=font_title).grid(column=0, row=1)
    else:
        ctk.CTkLabel(f_question, text=word, font=font_title).grid(column=0, row=0)

    return


def build_table(f_table, font_body, word, table, props):
    is_new = get_new_info(word, table)
    is_composite = get_composite(table)
    word_props = select_word(word, table)
    widget_num = get_widget_num(table)

    if is_new == 1:
        if is_composite == 1:
            build_table_new_word_comp(f_table, font_body, props, widget_num, word_props)
        else:
            build_table_new_word(f_table, font_body, props, widget_num, word_props)
    else:
        if is_composite == 1:
            return build_table_old_word_comp(f_table, font_body)
        else:
            return build_table_old_word(f_table, font_body, props, widget_num)

    return


def build_table_old_word(f_table, font_body, subjects, widgets_num):
    table = []
    for num in range(0, widgets_num):
        if num % 2 == 0:
            table.append(ctk.CTkLabel(f_table, text=subjects[num // 2], font=font_body, pady=12, padx=25))
            table[num].grid(column=0, row=num // 2)
        else:
            table.append(ctk.CTkEntry(f_table, font=font_body))
            table[num].grid(column=1, row=num // 2)

    return table


def build_table_old_word_comp(f_table, font_body):
    table = []
    tenses = ['Present', 'Imparfait', 'Futur']

    tense_var = tkinter.StringVar(value="Present")
    tense_menu = ctk.CTkOptionMenu(f_table, values=tenses, variable=tense_var)
    tense_menu.grid(column=0, row=2, padx=25)
    table.append(tense_var)

    aux_str = tkinter.StringVar(value="avoir")
    ctk.CTkRadioButton(f_table, text="avoir", value="to have", variable=aux_str).grid(column=1, row=2)
    ctk.CTkRadioButton(f_table, text="être", value="to be", variable=aux_str).grid(column=2, row=2)
    table.append(aux_str)

    entry = ctk.CTkEntry(f_table, font=font_body)
    entry.grid(column=3, row=2)
    table.append(entry)

    return table


def build_table_new_word(f_table, font_body, props, widgets_num, word_props):
    for num in range(0, widgets_num):
        if num % 2 == 0:
            ctk.CTkLabel(f_table, text=props[num // 2], font=font_body, pady=12, padx=25).grid(column=0, row=num)
        else:
            ctk.CTkLabel(f_table, text=word_props[num // 2 + 1], font=font_body, pady=12, padx=25).grid(column=1, row=num - 1)
            ttk.Separator(f_table, orient='horizontal').grid(columnspan=2, row=num, sticky='ew')

    return


def build_table_new_word_comp(f_table, font_body, props, widgets_num, word_props):
    composite_verbs = get_composite_verbs(word_props)
    composite_question_short_table_title(f_table, font_body)
    composite_question_short_table_props(f_table, font_body, word_props, composite_verbs[0])
    ctk.CTkLabel(f_table, text='').grid(columnspan=3, row=3)
    composite_tense_table(f_table, font_body, props, widgets_num, composite_verbs).grid(columnspan=3, row=4)

    return


def composite_question_short_table_title(f_table, font_body):
    ctk.CTkLabel(f_table, text='Tense', font=font_body, pady=12, padx=25).grid(column=0, row=0)
    ctk.CTkLabel(f_table, text='Auxiliaire', font=font_body, pady=12, padx=25).grid(column=1, row=0)
    ctk.CTkLabel(f_table, text='Participe Passé', font=font_body, pady=12, padx=25).grid(column=2, row=0)

    ttk.Separator(f_table, orient='horizontal').grid(columnspan=3, row=1, sticky='ew')

    return


def composite_question_short_table_props(f_table, font_body, word, inf_aux):
    ctk.CTkLabel(f_table, text=word[2].capitalize(), font=font_body, pady=12, padx=25).grid(column=0, row=2)
    ctk.CTkLabel(f_table, text=inf_aux, font=font_body, pady=12, padx=25).grid(column=1, row=2)
    ctk.CTkLabel(f_table, text=word[3], font=font_body, pady=12, padx=25).grid(column=2, row=2)

    return


def composite_tense_table(f_table, font_body, props, widgets_num, composite_verbs):
    f_return = ctk.CTkFrame(f_table)
    column = 0
    i = 0
    for num in range(0, widgets_num):
        if num % 3 == 0:
            ctk.CTkLabel(f_return, text=props[num // 3], font=font_body, pady=12, padx=25).grid(column=0, row=num)
        else:
            ctk.CTkLabel(f_return, text=composite_verbs[i], font=font_body, pady=12, padx=25).grid(column=column,
                                                                                                    row=num - column)
            i += 1

        column += 1
        if column % 3 == 0:
            column = 0
            ttk.Separator(f_return, orient='horizontal').grid(columnspan=3, row=num, sticky='ew')

    return f_return


def provide_feedback(f_table, font_body, table, responses, word_props, widgets_num):
    settings = get_settings()
    if settings["appearance"] == 'light':
        colors = settings["correct_feedback"][0], settings['incorrect_feedback'][0]
    else:
        colors = settings["correct_feedback"][1], settings['incorrect_feedback'][1]

    is_composite = get_composite(table)
    if is_composite == 1:
        grade = composite_question_short_table_feedback(f_table, font_body, responses, word_props, colors)
        composite_tense_table_feedback(f_table, font_body, responses, word_props, colors).grid(columnspan=4, row=4)
        return grade
    else:
        return table_feedback(f_table, font_body, responses, word_props, widgets_num, colors)


def table_feedback(f_table, font_body, table, word, widgets_num, colors):
    grade = 0
    for entry in range(1, widgets_num, 2):
        if table[entry].get() == word[-(-entry // 2)]:
            # Correct
            feedback = ctk.CTkLabel(f_table, text=table[entry].get(), font=font_body, padx=25, pady=12, bg_color=colors[0])
            grade += 1
        else:
            # Incorrect
            feedback = ctk.CTkLabel(f_table, text=table[entry].get(), font=font_body, padx=25, pady=12, bg_color=colors[1])
            # Correct Label
            ctk.CTkLabel(f_table, text=word[-(-entry // 2)], font=font_body, padx=25, pady=12).grid(column=3, row=entry // 2)
        # Delete Entry to replace with feedback label
        table[entry].destroy()
        feedback.grid(column=1, row=(entry // 2), sticky='WE')  # 'we' fills area of feedback with color

    return grade/(widgets_num/2)  # percentage


def composite_question_short_table_feedback(f_table, font_body, responses, word_props, colors):
    grade = 0

    if responses[0].get().lower() == word_props[2]:
        ctk.CTkLabel(f_table, text=word_props[2].capitalize(), font=font_body, bg_color=colors[0], pady=12,
                     padx=25).grid(column=0, row=2, sticky='WE')
        grade += 1
    else:
        ctk.CTkLabel(f_table, text=responses[0].get(), font=font_body, bg_color=colors[1], pady=12,
                     padx=25).grid(column=0, row=2, sticky='WE')
        ctk.CTkLabel(f_table, text=word_props[2].capitalize(), font=font_body, pady=12,
                     padx=25).grid(column=0, row=3, sticky='WE')
    if responses[1].get() == word_props[1]:
        ctk.CTkLabel(f_table, text=select_word(word_props[1], word_props[2])[1], font=font_body,
                     bg_color=colors[0], pady=12, padx=25).grid(column=1, row=2, sticky='WE')
        grade += 1
    else:
        ctk.CTkLabel(f_table, text=select_word(responses[1].get(), responses[0].get())[1], font=font_body,
                     bg_color=colors[1], pady=12, padx=25).grid(column=1, row=2, sticky='WE')
        ctk.CTkLabel(f_table, text=select_word(word_props[1], word_props[2])[1], font=font_body, pady=12,
                     padx=25).grid(column=1, row=3, sticky='WE')
    if responses[2].get() == word_props[3]:
        ctk.CTkLabel(f_table, text=word_props[3], font=font_body, bg_color=colors[0], pady=12,
                     padx=25).grid(column=2, row=2, sticky='WE')
        grade += 1
    else:
        ctk.CTkLabel(f_table, text=responses[2].get(), font=font_body,
                     bg_color=colors[1], pady=12, padx=25).grid(column=2, row=2, sticky='WE')
        ctk.CTkLabel(f_table, text=word_props[3], font=font_body, pady=12, padx=25).grid(column=2, row=3)

    return grade/3


def composite_tense_table_feedback(f_table, font_body, responses, word_props, colors):
    f_temp = ctk.CTkFrame(f_table)
    con_subjects = ['Infinitive', 'Je', 'Tu', 'Il/Elle', 'Nous', 'Vous', 'Ils/Elles']
    column = 1
    aux = select_word(responses[1].get(), responses[0].get())
    table_height = len(aux)
    for index in range(0, len(con_subjects)):
        ctk.CTkLabel(f_temp, text=con_subjects[index], font=font_body, pady=12, padx=25).grid(column=0, row=index)

    # Check aux correct and tense
    if not (responses[1].get() == word_props[1] and responses[0].get().lower() == word_props[2]):
        for index in range(0, table_height):
            ctk.CTkLabel(f_temp, text=aux[index], font=font_body, bg_color=colors[1], pady=12, padx=25).grid(column=column,
                                                                                                             row=index, sticky='WE')
        column += 1
        correct_aux = select_word(word_props[1], word_props[2])
        for index in range(0, table_height):
            ctk.CTkLabel(f_temp, text=correct_aux[index], font=font_body, pady=12, padx=25).grid(column=column, row=index)
    else:
        for index in range(0, table_height):
            ctk.CTkLabel(f_temp, text=aux[index], font=font_body, bg_color=colors[0], pady=12, padx=25).grid(column=column,
                                                                                                             row=index, sticky='WE')
    column += 1

    # Check verb
    if responses[2].get() == word_props[3]:
        for index in range(0, table_height):
            ctk.CTkLabel(f_temp, text=word_props[3], font=font_body, bg_color=colors[0], pady=12, padx=25).grid(column=column,
                                                                                                             row=index, sticky='WE')
    else:
        for index in range(0, table_height):
            ctk.CTkLabel(f_temp, text=responses[2].get(), font=font_body, bg_color=colors[1], pady=12, padx=25).grid(column=column,
                                                                                                             row=index, sticky='WE')
        column += 1
        for index in range(0, table_height):
            ctk.CTkLabel(f_temp, text=word_props[3], font=font_body, pady=12, padx=25).grid(column=column, row=index)
    responses[2].destroy()

    return f_temp


def next_button(f_root, font_body, f_submission, word_list, grade):
    # Replace button
    done = ctk.CTkButton(f_submission, text="Next", font=font_body)

    # 100% remove from list & set next due date
    if grade == 1:
        update_cooldown(word_list[0][word_list[1]][0])
        done.configure(command=lambda: reset_quiz_manager(f_root, word_list))
    else:
        # Does not remove from word list
        done.configure(command=lambda: reset_quiz_manager(f_root, word_list, remove=False))

    done.grid(column=0, row=0, sticky='S', pady=20)

    return


def submission_button(f_root, f_submission, font_body, responses, word_list):
    word = word_list[0][word_list[1]][0]
    table = word_list[0][word_list[1]][1]

    is_new = get_new_info(word, table)

    if is_new == 1:
        remove_new_from_word(word, table)
        done = ctk.CTkButton(f_submission, text="Next", font=font_body)
        # Does not remove from word list
        done.configure(command=lambda: reset_quiz_manager(f_root, word_list, remove=False))
        done.grid(column=0, row=0, sticky='N')
    else:
        submit = ctk.CTkButton(f_submission, text="Submit", font=font_body)
        submit.configure(command=lambda: grade_question(f_root, font_body, responses, word_list, submit))
        submit.grid(column=0, row=0, sticky='N')

    return


def grade_question(f_root, font_body, responses, word_list, submit_button):
    f_table = f_root.winfo_children()[1]
    submission_f = f_root.winfo_children()[2]

    word = word_list[0][word_list[1]][0]
    table = word_list[0][word_list[1]][1]

    word_props = select_word(word, table)
    widget_num = get_widget_num(table)

    grade = provide_feedback(f_table, font_body, table, responses, word_props, widget_num)

    if get_pts_cap(word) == 0:
        # Add pts, set pts cap
        set_pts(word, grade)

    submit_button.destroy()

    next_button(f_root, font_body, submission_f, word_list, grade)

    return


def get_composite(table):
    if table in ['passe_compose', 'futur_anterieur', 'plus_que_parfait']:
        return 1
    else:
        return 0


def get_composite_verbs(word):
    inf_participle = select_word(word[0], word[2])[1]
    aux = select_word(word[1], word[2])
    past_participle = word[3]

    composite = [aux[1], inf_participle]

    for i in range(2, len(aux)):
        composite.append(aux[i])
        composite.append(past_participle)

    return composite


def get_widget_num(table):
    widget_index = {'adjective': 8, 'passe_compose': 21, 'futur_anterieur': 21, 'plus_que_parfait': 21}

    if table in widget_index:
        return widget_index[table]
    else:
        return 14


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


def reset_quiz_manager(f_root, word_list, remove=True):
    # This only works if there is a scrollable frame
    f_root = f_root.master.master
    # Destroy all widgets on screen
    for widget in f_root.winfo_children():
        widget.destroy()

    # Remove from list
    if remove:
        word_list = remove_question(word_list)
    else:
        word_list = remove_question(word_list, remove=False)

    return next_question(f_root, word_list)
