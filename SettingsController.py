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


def load_font_body(f_settings_options, font_body, body_ex) -> ctk.CTkFrame:
    f_temp = ctk.CTkFrame(f_settings_options)
    ctk.CTkLabel(f_temp, text="Body Font:", font=font_body).grid(column=0, row=0, columnspan=2)

    f_spinbox = spinbox(f_temp, font_body)
    spinbox_assign_body_font(f_spinbox.winfo_children(), font_body, body_ex)
    f_spinbox.grid(column=2, row=0, pady=11, columnspan=2)

    return f_temp


def load_appearance_mode(f_settings_options, font_body):
    f_temp = ctk.CTkFrame(f_settings_options)
    ctk.CTkLabel(f_temp, text="Appearance (Dark/Light):").grid(column=0, row=0, columnspan=2)
    switch_appearance_mode(f_temp, font_body).grid(column=2, row=0, pady=11, columnspan=2)

    return f_temp


def spinbox(frame, font_body):
    """Return a spinbox with no functionality assigned."""
    font_size = font_body.cget("size")
    f_temp = ctk.CTkFrame(frame)

    size_entry = ctk.CTkEntry(f_temp, font=font_body, justify='center', width=(font_size + 20))
    size_entry.grid(column=1, row=0)

    ctk.CTkButton(f_temp, text="-", font=font_body, width=(font_size + 5)).grid(column=0, row=0)
    ctk.CTkButton(f_temp, text="+", font=font_body, width=(font_size + 2)).grid(column=3, row=0)

    return f_temp


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


def spinbox_assign_body_font(widgets, font_body, body_ex):
    entry, button_1, button_2 = widgets

    body_size = font_body.cget("size")
    entry.insert(0, body_size)

    button_1.configure(command=lambda: spinbox_font_body_update(entry, -1, font_body, body_ex))
    button_2.configure(command=lambda: spinbox_font_body_update(entry, 1, font_body, body_ex))

    return


def spinbox_daily_update(entry, change):
    """Applies changes based on spinbox button pressed."""
    new_size = calculate_new_size(entry, change)

    set_daily_limit(new_size)
    replace_entry_value(entry, new_size)

    return

def spinbox_font_title_update(entry, change, font_title):
    new_size = calculate_new_size(entry, change)

    set_font_title_size(new_size)
    update_font_title(font_title, new_size)
    replace_entry_value(entry, new_size)

    return


def spinbox_font_body_update(entry, change, font_body, body_ex):
    new_size = calculate_new_size(entry, change)

    set_font_body_size(new_size)
    update_font_body(body_ex, new_size)
    replace_entry_value(entry, new_size)

    return


def calculate_new_size(entry, change):
    old_size = int(entry.get())
    return old_size - 1 if change == -1 else old_size + 1


def set_daily_limit(size):
    """Size is saved to settings.json file."""
    settings = Model.get_settings()
    settings['daily_word_limit'] = size
    Model.set_settings(settings)

    return


def set_font_title_size(new_size):
    """Font Title size is saved to the current themes/color.json file"""
    theme = Model.get_theme()
    theme['CTkFont']['Windows']['title_size'] = new_size
    Model.set_theme(theme)

    return


def set_font_body_size(new_size):
    """Font Title size is saved to the current themes/color.json file"""
    theme = Model.get_theme()
    theme['CTkFont']['Windows']['size'] = new_size
    Model.set_theme(theme)

    return


def update_font_title(font_title, size):
    font_title.configure(size=size)

    return


def update_font_body(body_ex, size):
    font_family = Model.get_fonts()[0]
    body_ex.configure(font=(font_family, size))

    return


def replace_entry_value(entry: ctk.CTkEntry, new_value: int) -> None:
    entry.delete(0, last_index=ctk.END)  # Remove current value of entry
    entry.insert(0, new_value)  # Input new size into entry

    return


def switch_appearance_mode(frame, font_body):
    f_temp = ctk.CTkFrame(frame)
    # Set up switch variable
    settings = Model.get_settings()
    switch_var = ctk.StringVar(value="on") if settings['appearance'] == 'light' else ctk.StringVar(value="off")

    appearance_switch = ctk.CTkSwitch(f_temp, text='', onvalue='on', offvalue='off',
    font = font_body, command = lambda: set_appearance_mode(switch_var), variable = switch_var)
    appearance_switch.pack()

    return f_temp


def set_appearance_mode(switch_var):
    settings = Model.get_settings()
    settings['appearance'] = 'light' if switch_var.get() == 'on' else 'dark'
    Model.set_settings(settings)

    ctk.set_appearance_mode(settings['appearance'])  # Change the appearance now
    # reload_settings_page()  # Reload Page (for buttons)

    return


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