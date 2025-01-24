# Import python files
import json
import sqlite3
import random
import datetime

# Import quiz Pages
import ConjugationQuizPage
import NounQuizPage
import AdjectivesQuizPage
import FinishPage


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


def select_questions():
    # Select all in a list
    # Connect to database
    conn = sqlite3.connect('en_fr_words.db')
    # Create cursor
    c = conn.cursor()

    # Select new words
    '''c.execute("SELECT word, type FROM word_info WHERE new = 1 "
              "AND (type = 'present' OR type='adjective' OR type = 'noun')")'''
    # Add new words to quiz list
    #word_list = c.fetchmany(2)  # Temporary

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

    return


def remove_question(word_list, remove=True):
    if remove:
        rand_index = word_list[1]
        word_list = word_list[0]
        word_list.remove(word_list[rand_index])
    else:
        word_list = word_list[0]

    return word_list




