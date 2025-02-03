import customtkinter as ctk
import json
import Home
import Model
import Settings


def load_daily_word(f_settings_options, font_body) -> ctk.CTkFrame:
    f_temp = ctk.CTkFrame(f_settings_options)
    ctk.CTkLabel(f_temp, text="Daily New Word Limit:", font=font_body).grid(column=0, row=0,
                                                                                        columnspan=2)
    f_spinbox = spinbox(f_temp, font_body)
    spinbox_assign_daily(f_spinbox.winfo_children())
    f_spinbox.grid(column=2, row=0, pady=11, columnspan=2)

    return f_temp


def load_font_title(f_settings_options, font_title, font_body) -> ctk.CTkFrame:
    f_temp = ctk.CTkFrame(f_settings_options)
    ctk.CTkLabel(f_temp, text="Title Font:", font=font_body).grid(column=0, row=0, columnspan=2)

    f_spinbox = spinbox(f_temp, font_body)
    spinbox_assign_title_font(f_spinbox.winfo_children(), font_title)
    f_spinbox.grid(column=2, row=0, pady=11, columnspan=2)

    return f_temp


def load_font_body(f_settings_options, font_body) -> ctk.CTkFrame:
    pass


def spinbox(f_settings_options, font_body):
    """Return a spinbox with no functionality assigned."""
    font_size = font_body.cget("size")
    temp_frame = ctk.CTkFrame(f_settings_options)

    size_entry = ctk.CTkEntry(temp_frame, font=font_body, justify='center', width=(font_size + 20))
    size_entry.grid(column=1, row=0)

    ctk.CTkButton(temp_frame, text="-", font=font_body, width=(font_size + 5)).grid(column=0, row=0)
    ctk.CTkButton(temp_frame, text="+", font=font_body, width=(font_size + 2)).grid(column=3, row=0)

    return temp_frame


def spinbox_assign_daily(widgets):
    """Assigns spinbox with daily word limit functionality."""
    entry, button_1, button_2 = widgets

    daily_word_limit = Model.get_settings()['daily_word_limit']
    entry.insert(0, daily_word_limit)

    button_1.configure(command=lambda: spinbox_daily_update(entry, -1))
    button_2.configure(command=lambda: spinbox_daily_update(entry, 1))

    return

def spinbox_assign_title_font(widgets, font_title):
    entry, button_1, button_2 = widgets

    title_size = font_title.cget("size")
    entry.insert(0, title_size)

    button_1.configure(command=lambda: spinbox_font_title_update(entry, -1, font_title))
    button_2.configure(command=lambda: spinbox_font_title_update(entry, 1, font_title))

    return


def spinbox_daily_update(entry, change):
    """Applies changes based on spinbox button pressed."""
    new_size = calculate_new_size(entry, change)

    save_daily_limit(new_size)
    replace_entry_value(entry, new_size)

    return

def spinbox_font_title_update(entry, change, font_title):
    new_size = calculate_new_size(entry, change)

    save_font_title_size(new_size)
    update_font_title(font_title, new_size)
    replace_entry_value(entry, new_size)

    return


def calculate_new_size(entry, change):
    old_size = int(entry.get())
    return old_size - 1 if change == -1 else old_size + 1


def save_daily_limit(size):
    """Size is saved to settings.json file."""
    settings = Model.get_settings()
    settings['daily_word_limit'] = size
    Model.set_settings(settings)

    return


def save_font_title_size(new_size):
    """Font Title size is saved to the current themes/color.json file"""
    theme = Model.get_theme()
    theme['CTkFont']['Windows']['title_size'] = new_size
    Model.set_theme(theme)

    return


def update_font_title(font_title, size):
    font_title.configure(size=size)

    return


def spinbox_font_options(size_entry, change, font_type):
    if change == -1:
        size = int(size_entry.get()) - 1  # Decrease
    else:
        size = int(size_entry.get()) + 1  # Increase

    # Updates title size, writes default_size = size
    save_font_size(font_type, size)
    # Updates all body values and spinbox options
    if font_type == 'body':
        update_body_values(size)
    # Remove current entry value and replace with new size
    replace_entry_value(size_entry, size)

    return


def save_font_size(font_type, size, font_title):
    # Open current theme settings
    color = Model.get_settings()['color']

    with open(f"themes/{color}.json", 'r') as file:
        theme = json.load(file)
    file.close()

    # Change body font size
    if font_type == 'title':
        theme['CTkFont']['Windows']['title_size'] = size
        # Update the title size on this page
        font_title.configure(size=size)
    else:
        theme['CTkFont']['Windows']['size'] = size

    # Write into settings for startup of program
    with open(f"themes/{color}.json", 'w') as file:
        json.dump(theme, file, indent=2)
    file.close()

    return


def update_body_values(font_body, daily_spinbox, body_spinbox, title_spinbox, size):
    # Update font size
    font_body.configure(size=size)
    # Update widgets to scale with body font size (Entry to contain number and buttons to be semi-congruent to entry)
    # Daily option
    d_widgets = daily_spinbox.winfo_children()
    d_widgets[1].configure(width=(size + 3))
    d_widgets[2].configure(width=(size + 2))
    d_widgets[0].configure(width=(size + 20))
    # body option
    b_widgets = body_spinbox.winfo_children()
    b_widgets[1].configure(width=(size + 3))
    b_widgets[2].configure(width=(size + 2))
    b_widgets[0].configure(width=(size + 20))
    # title option
    t_widgets = title_spinbox.winfo_children()
    t_widgets[1].configure(width=(size + 3))
    t_widgets[2].configure(width=(size + 2))
    t_widgets[0].configure(width=(size + 20))

    return


def replace_entry_value(entry: ctk.CTkEntry, new_value: int) -> None:
    # Remove current value of entry
    entry.delete(0, last_index=ctk.END)
    # Input new size into entry
    entry.insert(0, new_value)

    return


def set_appearance_mode(switch_var):
    # Open settings
    settings = Model.get_settings()

    # Change value in settings
    if switch_var.get() == 'on':
        settings['appearance'] = 'light'
    else:
        settings['appearance'] = 'dark'

    # Write it into settings.json to be remembered on startup of program
    with open('settings.json', 'w') as file:
        json.dump(settings, file, indent=2)
    file.close()

    # Change the appearance now
    ctk.set_appearance_mode(settings['appearance'])

    # Reload Page (for buttons)
    reload_settings_page()


def color_options(f_settings_options, font_body):
    temp_frame = ctk.CTkFrame(f_settings_options)
    ctk.CTkLabel(temp_frame, text="Color", font=font_body).grid(column=0, row=0, columnspan=4)

    # Open settings
    settings = Model.get_settings()

    current_color = settings['color']
    appearance = settings['appearance']

    color_options = {"blue": ["#3a7ebf", "#1f538d"], "cyan": ["#00bbbb", "#00aaaa"],
                     "green": ["#2CC985", "#2FA572"], "orange": ["#EE9F00", "#DD9F00"],
                     "pink": ["#F8486D", "#F04660"], "purple": ["#682cc9", "#682fa5"],
                     "red": ["#DD2222", "#DD1616"], "yellow": ["#CCCC22", "#CCCC0F"]}
    c_o_keys = list(color_options.keys())

    # Set light or dark colors
    if appearance == 'light':
        index = 0
    else:
        index = 1

    # Should be in a loop. Could not get arguments to send of specific button. All returned info of last button.
    ctk.CTkButton(temp_frame, text=' ', font=font_body, fg_color=color_options[c_o_keys[0]][index], hover=False,
                  command=lambda: set_color(c_o_keys[0], current_color)).grid(column=0, row=1, padx=1, pady=1,
                                                                                   sticky='ew')
    ctk.CTkButton(temp_frame, text=' ', font=font_body, fg_color=color_options[c_o_keys[1]][index], hover=False,
                  command=lambda: set_color(c_o_keys[1], current_color)).grid(column=1, row=1, padx=1, pady=1,
                                                                                   sticky='ew')
    ctk.CTkButton(temp_frame, text=' ', font=font_body, fg_color=color_options[c_o_keys[2]][index], hover=False,
                  command=lambda: set_color(c_o_keys[2], current_color)).grid(column=2, row=1, padx=1, pady=1,
                                                                                   sticky='ew')
    ctk.CTkButton(temp_frame, text=' ', font=font_body, fg_color=color_options[c_o_keys[3]][index], hover=False,
                  command=lambda: set_color(c_o_keys[3], current_color)).grid(column=3, row=1, padx=1, pady=1,
                                                                                   sticky='ew')
    ctk.CTkButton(temp_frame, text=' ', font=font_body, fg_color=color_options[c_o_keys[4]][index], hover=False,
                  command=lambda: set_color(c_o_keys[4], current_color)).grid(column=0, row=2, padx=1, pady=1,
                                                                                   sticky='ew')
    ctk.CTkButton(temp_frame, text=' ', font=font_body, fg_color=color_options[c_o_keys[5]][index], hover=False,
                  command=lambda: set_color(c_o_keys[5], current_color)).grid(column=1, row=2, padx=1, pady=1,
                                                                                   sticky='ew')
    ctk.CTkButton(temp_frame, text=' ', font=font_body, fg_color=color_options[c_o_keys[6]][index], hover=False,
                  command=lambda: set_color(c_o_keys[6], current_color)).grid(column=2, row=2, padx=1, pady=1,
                                                                                   sticky='ew')
    ctk.CTkButton(temp_frame, text=' ', font=font_body, fg_color=color_options[c_o_keys[7]][index], hover=False,
                  command=lambda: set_color(c_o_keys[7], current_color)).grid(column=3, row=2, padx=1, pady=1,
                                                                                   sticky='ew')

    return temp_frame


def set_color(f_root, new_color, past_color):
    # Save info of last theme
    with open(f"themes/{past_color}.json", 'r') as file:
        old_theme = json.load(file)
    file.close()
    title_size = old_theme['CTkFont']['Windows']['title_size']
    body_size = old_theme['CTkFont']['Windows']['size']

    # Save to new selected theme
    with open(f"themes/{new_color}.json", 'r') as file:
        new_theme = json.load(file)
    file.close()

    new_theme['CTkFont']['Windows']['title_size'] = title_size
    new_theme['CTkFont']['Windows']['size'] = body_size

    with open(f"themes/{new_color}.json", 'w') as file:
        json.dump(new_theme, file, indent=2)
    file.close()

    # Set the new selected theme
    ctk.set_default_color_theme(f"themes/{new_color}.json")

    # Set new theme color in settings
    settings = Model.get_settings()

    settings["color"] = new_color

    with open(f"settings.json", 'w') as file:
        json.dump(settings, file, indent=2)
    file.close()

    # Reload page
    reload_settings_page(f_root)

    return


def reload_settings_page(f_root):
    for widget in f_root.winfo_children():
        widget.destroy()

    return Settings.Settings(f_root)


def submission(f_root):
    f_root = f_root.master.master
    for widget in f_root.winfo_children():
        widget.destroy()

    Home.Home(f_root)

    return