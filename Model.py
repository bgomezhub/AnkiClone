# Import python files
import json
import sqlite3
import random
import datetime
from customtkinter import CTkFrame

# Import quiz Pages
from pages import Finish
from quiz import Noun, Adjective, Conjugation


def get_fonts() -> tuple[str, int, int]:
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


def get_settings() -> dict:
    """Return the settings json file."""
    with open("settings.json", 'r') as file:
        settings: dict = json.load(file)
    file.close()

    return settings


def set_settings(settings: dict) -> None:
    """Write into settings.json file."""
    with open("settings.json", 'w') as file:
        json.dump(settings, file, indent=2)
    file.close()

    return


def get_theme() -> dict:
    """Return the current theme.json file."""
    color = get_settings()['color']
    with open(f"themes/{color}.json", 'r') as file:
        theme: dict = json.load(file)
    file.close()

    return theme


def get_theme_not_current(theme_color: str) -> dict:
    """Return specified theme.json file."""
    with open(f"themes/{theme_color}.json", 'r') as file:
        theme: dict = json.load(file)
    file.close()

    return theme


def set_theme(theme: dict) -> None:
    """Write into theme.json file."""
    color = get_settings()['color']
    with open(f"themes/{color}.json", 'w') as file:
        json.dump(theme, file, indent=2)
    file.close()

    return


def get_pts_cap(word: str, table: str) -> bool:
    """Returns bool if pts_cap has been triggered."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"SELECT pts_cap FROM word_info WHERE word = '{word}' AND type = '{table}'")
    pts_cap_value = c.fetchone()[0]
    conn.close()  # Close db connection

    return pts_cap_value == 1


def set_pts_cap(word: str, table: str) -> None:
    """Sets pts_cap to True."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"UPDATE word_info SET pts_cap = 1 WHERE word = '{word}' AND type = '{table}'")

    conn.commit()  # Commit changes
    conn.close()  # Close db connection
    return


def remove_pts_cap(word: str, table: str) -> None:
    """Sets pts_cap to False."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"UPDATE word_info SET pts_cap = 0 WHERE word = '{word}' AND type = '{table}'")

    conn.commit()  # Commit changes
    conn.close()  # Close db connection
    return


def get_new_info(word: str, table: str) -> bool:
    """Returns bool if word is new."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"SELECT new FROM word_info WHERE word = '{word}' and type = '{table}'")
    new_value = c.fetchone()[0]
    conn.close()  # Close db connection

    return new_value == 1


def remove_new_from_word(word: str, table: str) -> None:
    """Sets new to false on word_info."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"UPDATE word_info SET new = 0 WHERE word = '{word}' and type = '{table}'")

    conn.commit()  # Commit changes
    conn.close()  # Close db connection
    return


def get_pts(word: str, table: str) -> int:
    """Returns pts of selected word"""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"SELECT pts FROM word_info WHERE word = '{word}' and type = '{table}'")
    pts: int = c.fetchone()[0]
    conn.close()  # Close db connection

    return pts


def set_pts(word: str, table: str, word_pts: int, gained_pts: int) -> None:
    """Adds pts to word_info."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor

    # pts will not be lost further if at or below zero
    if not (word_pts <= 0 and gained_pts < 0):
        c.execute(f"UPDATE word_info SET pts = (pts + {gained_pts}) WHERE word = '{word}' AND type = '{table}'")

    conn.commit()  # Commit changes
    conn.close()  # Close db connection
    return


def calculate_pts(grade: int) -> int:
    """Returns pts based of grade of submission."""
    return grade * 20 - 10  # +- 10 pts, 50% results in 0


def update_pts(word: str, table: str, grade: int) -> None:
    """Updates pts & sets pts_cap."""
    pts_gained = calculate_pts(grade)
    word_pts = get_pts(word, table)
    set_pts(word, table, word_pts, pts_gained)
    set_pts_cap(word, table)

    return


def set_cooldown(word: str, table: str, date: str) -> None:
    """Sets next review date for word."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"UPDATE word_info SET cooldown = '{date}' WHERE word = '{word}' AND type = '{table}'")

    conn.commit()  # Commit changes
    conn.close()  # Close db connection
    return


def calculate_cooldown_days(pts: int) -> int:
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


def calculate_cooldown_date(days: int) -> str:
    """Returns the date until next review."""
    cd: datetime = datetime.datetime.now() + datetime.timedelta(days=days)  # Add cooldown to today's date
    date: str = cd.strftime("%Y%m%d")  # format YYYYMMDD

    return date


def update_cooldown(word: str, table: str) -> None:
    """Updates cooldown date & removes pts_cap of word."""
    pts = get_pts(word, table)
    days = calculate_cooldown_days(pts)
    date = calculate_cooldown_date(days)
    set_cooldown(word, table, date)
    remove_pts_cap(word, table)

    return


def get_composite(table: str) -> bool:
    """Returns bool if word is a composite verb."""
    return table in ['passe_compose', 'futur_anterieur', 'plus_que_parfait']


def get_composite_verbs(word: str) -> list[str]:
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


def get_noun(table: str) -> bool:
    """Returns bool if word is a noun."""
    return table == 'noun'


def get_word(word: str, table: str) -> tuple:
    """Returns word properties of word."""
    conn = sqlite3.connect('en_fr_words.db')  # Connect to database
    c = conn.cursor()  # Create cursor
    c.execute(f"SELECT * FROM {table} WHERE en = '{word}'")
    word_properties: tuple = c.fetchone()
    conn.close()  # Close db connection

    return word_properties


def get_questions() -> list[str]:
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
    '''c.execute("SELECT word, type FROM word_info "
                  "WHERE word = 'big, tall'")'''
    '''c.execute("SELECT word, type FROM word_info "
              "WHERE word = 'time'")'''

    word_list = c.fetchmany(1)
    print(word_list)
    #word_list += c.fetchall()

    conn.close()  # Close db connection
    return word_list


def next_question(f_root: CTkFrame, word_list: list[str]):
    """Randomizes next question and sends program to page depending on the type of the word."""
    # Base condition
    if len(word_list) == 0:
        return Finish.Finish(f_root)

    selected_index: int = random.randint(0, len(word_list) - 1)  # Randomize next word
    word_table: str = word_list[selected_index][1]

    # Send to corresponding page
    if word_table == 'noun':
        Noun.Noun(f_root, [word_list, selected_index])
    elif word_table == 'adjective':
        Adjective.Adjective(f_root, [word_list, selected_index])
    else:
        Conjugation.Conjugation(f_root, [word_list, selected_index])

    return


def remove_question(word_list: list[str, int], remove_from_word_list: bool=True) -> list[str]:
    """Returns word_list with current question unselected or removed and index removed."""
    if remove_from_word_list:
        selected_index = word_list[1]
        word_list = word_list[0]
        word_list.remove(word_list[selected_index])
    else:
        word_list = word_list[0]

    return word_list
