# Import python files
import json
import sqlite3
import random
import datetime

# Import quiz Pages
import Conjugation
import Noun
import Adjective
import Finish


def get_fonts():
    """Return a tuple of font family, title size, body size."""
    settings = get_settings()

    # Get font family
    with open(f"themes/{settings['color']}.json", 'r') as file:
        theme = json.load(file)
    file.close()
    font_family = theme['CTkFont']['Windows']['family']

    # Select body & title size
    font_size_body = theme['CTkFont']['Windows']['size']
    font_size_title = theme['CTkFont']['Windows']['title_size']

    return tuple((font_family, font_size_title, font_size_body))


def get_settings():
    """Return the settings json file."""
    with open("settings.json", 'r') as file:
        settings = json.load(file)
    file.close()

    return settings


def set_settings(settings_file):
    """Write into settings file."""
    with open("settings.json", 'w') as file:
        json.dump(settings_file, file, indent=2)
    file.close()

    return


def get_pts_cap(word, table):
    """Returns bool if pts_cap has been triggered."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"SELECT pts_cap FROM word_info WHERE word = '{word}' AND type = '{table}'")
    pts_cap_value = c.fetchone()[0]
    conn.close()  # Close db connection

    if pts_cap_value == 1:
        return True
    else:
        return False


def set_pts_cap(word, table):
    """Sets pts_cap to True."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"UPDATE word_info SET pts_cap = 1 WHERE word = '{word}' AND type = '{table}'")

    conn.commit()  # Commit changes
    conn.close()  # Close db connection
    return


def remove_pts_cap(word, table):
    """Sets pts_cap to False."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"UPDATE word_info SET pts_cap = 0 WHERE word = '{word}' AND type = '{table}'")

    conn.commit()  # Commit changes
    conn.close()  # Close db connection
    return


def get_new_info(word, table):
    """Returns bool if word is new."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"SELECT new FROM word_info WHERE word = '{word}' and type = '{table}'")
    new_value = c.fetchone()[0]
    conn.close()  # Close db connection

    if new_value == 1:
        return True
    else:
        return False


def remove_new_from_word(word, table):
    """Sets new to false on word_info."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"UPDATE word_info SET new = 0 WHERE word = '{word}' and type = '{table}'")

    conn.commit()  # Commit changes
    conn.close()  # Close db connection
    return


def get_pts(word, table):
    """Returns pts of selected word"""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"SELECT pts FROM word_info WHERE word = '{word}' and type = '{table}'")
    pts = c.fetchone()[0]
    conn.close()  # Close db connection

    return pts


def set_pts(word, table, word_pts, gained_pts):
    """Adds pts to word_info."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor

    # pts will not be lost further if at or below zero
    if not (word_pts <= 0 and gained_pts < 0):
        c.execute(f"UPDATE word_info SET pts = (pts + {gained_pts}) WHERE word = '{word}' AND type = '{table}'")

    conn.commit()  # Commit changes
    conn.close()  # Close db connection
    return


def calculate_pts(grade):
    """Returns pts based of grade of submission."""
    return grade * 20 - 10  # +- 10 pts, 50% results in 0


def update_pts(word, table, grade):
    """Updates pts & sets pts_cap."""
    pts_gained = calculate_pts(grade)
    word_pts = get_pts(word, table)
    set_pts(word, table, word_pts, pts_gained)
    set_pts_cap(word, table)

    return


def set_cooldown(word, table, date):
    """Sets next review date for word."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"UPDATE word_info SET cooldown = '{date}' WHERE word = '{word}' AND type = '{table}'")

    conn.commit()  # Commit changes
    conn.close()  # Close db connection
    return


def calculate_cooldown_days(pts):
    """Returns # of days until next review date."""
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


def calculate_cooldown_date(days):
    """Returns the date until next review."""
    cd = datetime.datetime.now() + datetime.timedelta(days=days)  # Add cooldown to today's date
    date = cd.strftime("%Y%m%d")  # format YYYYMMDD

    return date


def update_cooldown(word, table):
    """Updates cooldown date & removes pts_cap of word."""
    pts = get_pts(word, table)
    days = calculate_cooldown_days(pts)
    date = calculate_cooldown_date(days)
    set_cooldown(word, table, date)
    remove_pts_cap(word, table)


def get_composite(table):
    """Returns bool if word is a composite verb."""
    if table in ['passe_compose', 'futur_anterieur', 'plus_que_parfait']:
        return True
    else:
        return False


def get_composite_verbs(word):
    """Returns alternating list of aux and verb."""
    infinitive_verb = get_word(word[0], word[2])[1]
    aux = get_word(word[1], word[2])
    past_participle = word[3]

    # Add infinitives
    composite = [aux[1], infinitive_verb]
    # Add conjugations
    for i in range(2, len(aux)):
        composite.append(aux[i])
        composite.append(past_participle)

    return composite


def get_word(word, table):
    """Returns word properties of word."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"SELECT * FROM {table} WHERE en = '{word}'")
    word_properties = c.fetchone()
    conn.close()  # Close db connection

    return word_properties


def get_questions():
    """Returns word list of due & new words."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor

    # Select new words
    '''c.execute("SELECT word, type FROM word_info WHERE new = 1 "
              "AND (type = 'present' OR type='adjective' OR type = 'noun')")'''
    #word_list = c.fetchmany(2)  # Add new words to quiz list

    # Select due words
    '''c.execute(f"Select word, type FROM word_info "
              f"WHERE cooldown <= {datetime.datetime.now().strftime('%Y%m%d')} AND new = 0")'''
    '''c.execute("SELECT word, type FROM word_info "
              "WHERE word = 'to eat' and type = 'passe_compose'")'''
    '''c.execute("SELECT word, type FROM word_info "
              "WHERE word = 'to speak'")'''
    c.execute("SELECT word, type FROM word_info "
                  "WHERE word = 'big, tall'")

    word_list = c.fetchmany(1)
    print(word_list)
    #word_list += c.fetchall()

    conn.close()  # Close db connection
    return word_list


def next_question(f_root, word_list):
    """Randomizes next question and sends program to page depending on the type of the word."""
    # Base condition
    if len(word_list) == 0:
        return Finish.Finish(f_root)

    selected_index = random.randint(0, len(word_list) - 1)  # Randomize next word
    word_table = word_list[selected_index][1]

    # Send to corresponding page
    if word_table == 'noun':
        Noun.Noun(f_root, [word_list, selected_index])
    elif word_table == 'adjective':
        Adjective.Adjective(f_root, [word_list, selected_index])
    else:
        Conjugation.Conjugation(f_root, [word_list, selected_index])

    return


def remove_question(word_list, remove_from_word_list=True):
    """Returns word_list with current question unselected or removed."""
    if remove_from_word_list:
        selected_index = word_list[1]
        word_list = word_list[0]
        word_list.remove(word_list[selected_index])
    else:
        word_list = word_list[0]

    return word_list
