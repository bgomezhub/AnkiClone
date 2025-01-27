import customtkinter as ctk
import json
import Home
import Settings

def spinbox(f_settings_options, font_title, font_body, font_type):
    # Create frame to house all widgets
    temp_frame = ctk.CTkFrame(f_settings_options)
    # Placed in the middle
    size_entry = ctk.CTkEntry(temp_frame, font=font_body, justify='center',
                              width=(font_body.cget("size") + 20))
    size_entry.grid(column=1, row=0)

    size_title = font_title.cget("size")
    size_body = font_body.cget("size")
    # Input new size into entry
    if font_type == 'title':
        size_entry.insert(0, size_title)
    elif font_type == 'body':
        size_entry.insert(0, size_body)
    else:
        with open('settings.json', 'r') as file:
            daily_word_limit = json.load(file)['daily_word_limit']
        file.close()

        size_entry.insert(0, daily_word_limit)
        ctk.CTkButton(temp_frame, text="-", font=font_body,
                      command=lambda: spinbox_daily_options(size_entry, -1),
                      width=(size_body + 5)).grid(column=0, row=0)
        ctk.CTkButton(temp_frame, text="+", font=font_body,
                      command=lambda: spinbox_daily_options(size_entry, 1),
                      width=(size_body + 2)).grid(column=3, row=0)

        return temp_frame

    # Options placed on the sides, (-) == button, (+) == button2
    ctk.CTkButton(temp_frame, text="-", font=font_body,
                  command=lambda: spinbox_font_options(font_type, size_entry, -1),
                  width=(size_body + 5)).grid(column=0, row=0)
    ctk.CTkButton(temp_frame, text="+", font=font_body,
                  command=lambda: spinbox_font_options(font_type, size_entry, 1),
                  width=(size_body + 2)).grid(column=3, row=0)

    return temp_frame


def spinbox_daily_options(size_entry, change):
    if change == -1:
        size = int(size_entry.get()) - 1  # Decrease
    else:
        size = int(size_entry.get()) + 1  # Increase

    # Saves value into daily limit
    save_daily_limit(size)
    # Remove current entry value and replace with new limit
    remove_entry_value(size_entry, size)


def spinbox_font_options(font_type, size_entry, change):
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
    remove_entry_value(size_entry, size)

    return


def save_font_size(font_type, size, font_title):
    # Open current theme settings
    with open("settings.json", 'r') as file:
        color = json.load(file)['color']
    file.close()
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


def save_daily_limit(size):
    # Open file
    with open("settings.json", 'r') as file:
        settings = json.load(file)
    file.close()

    # Change value
    settings['daily_word_limit'] = size

    # Write into file
    with open("settings.json", 'w') as file:
        json.dump(settings, file, indent=2)
    file.close()


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
    b_widgets[1].configure(
        width=(size + 3))  # (-) button is smaller in pixels than (+), scales proportionally for most font sizes
    b_widgets[2].configure(width=(size + 2))
    b_widgets[0].configure(width=(size + 20))
    # title option
    t_widgets = title_spinbox.winfo_children()
    t_widgets[1].configure(width=(size + 3))
    t_widgets[2].configure(width=(size + 2))
    t_widgets[0].configure(width=(size + 20))

    return


def remove_entry_value(entry_w, new_value):
    # Remove current value of entry
    entry_w.delete(0, last_index=ctk.END)
    # Input new size into entry
    entry_w.insert(0, new_value)

    return


def set_appearance_mode(switch_var):
    # Open settings
    with open('settings.json', 'r') as file:
        settings = json.load(file)
    file.close()

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
    with open('settings.json', 'r') as file:
        settings = json.load(file)
    file.close()

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
    with open(f"settings.json", 'r') as file:
        settings = json.load(file)
    file.close()

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
    for widget in f_root.winfo_children():
        widget.destroy()

    Home.Home(f_root)

    return