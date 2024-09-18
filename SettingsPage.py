import json

import customtkinter as ctk
import Home
import QuizManager


class SettingsPage:
    def __init__(self, frame):
        self.root_frame = frame
        # Title
        self.f_title = ctk.CTkFrame(frame)
        self.f_title.pack(padx=200, pady=50)
        self.title = ctk.CTkLabel(self.f_title, text='Settings', font=QuizManager.get_title_font())
        self.title.pack()
        # Handle Setting Options
        self.f_setting_options = ctk.CTkFrame(frame)
        self.f_setting_options.pack(padx=200, pady=50)
        # Submission frame
        self.f_submission = ctk.CTkFrame(frame)
        self.f_submission.pack(padx=200, pady=50)

        self.options()

        # Return to Home
        ctk.CTkButton(self.f_submission, text='Done', font=('Roboto', 20),
                      command=lambda: self.submission(frame)).grid(column=0, row=0, sticky='N')

    def options(self):
        # Open settings
        with open('settings.json', 'r') as file:
            settings = json.load(file)

        # Set font sizes
        ctk.CTkLabel(self.f_setting_options, text="Title Font:").grid(column=0, row=0)
        self.spinbox().grid(column=1, row=0)
        ctk.CTkLabel(self.f_setting_options, text="Body Font:").grid(column=0, row=1)

        # Toggle dark/light mode
        ctk.CTkLabel(self.f_setting_options, text="Appearance (Dark/Light):").grid(column=0, row=2)
        if settings['appearance'] == 'light':
            switch_var = ctk.StringVar(value="on")
        else:
            switch_var = ctk.StringVar(value="off")
        appearance_switch = (ctk.CTkSwitch(self.f_setting_options, text='', onvalue='on', offvalue='off',
                                           command=lambda: self.set_appearance_mode(switch_var), variable=switch_var))
        appearance_switch.grid(column=1, row=2, pady=11, padx=10)

        # Set color of program
        ctk.CTkLabel(self.f_setting_options, text="Color:").grid(column=0, row=3)

    def set_appearance_mode(self, switch_var):
        # Open settings
        with open('settings.json', 'r') as file:
            settings = json.load(file)

        # Change value in settings
        if switch_var.get() == 'on':
            settings['appearance'] = 'light'
        else:
            settings['appearance'] = 'dark'

        # Write it into settings.json to be remembered on startup of program
        with open('settings.json', 'w') as file:
            json.dump(settings, file)

        # Change the appearance now
        ctk.set_appearance_mode(settings['appearance'])

    def spinbox(self):
        # Create frame to house all widgets
        temp_frame = ctk.CTkFrame(self.f_setting_options)

        # Placed in the middle
        size_entry = ctk.CTkEntry(temp_frame, width=30)
        size_entry.grid(column=1, row=0)
        size_entry.insert(0, QuizManager.get_title_font()[1])
        # Placed on the sides
        ctk.CTkButton(temp_frame, text="-", command=lambda: self.spinbox_options(size_entry, -1),
                      width=25).grid(column=0, row=0)

        ctk.CTkButton(temp_frame, text="+", command=lambda: self.spinbox_options(size_entry, 1),
                      width=25).grid(column=3, row=0)

        return temp_frame

    def spinbox_options(self, size_entry, change):
        if change == -1:
            size = int(size_entry.get()) - 1  # Decrease
        else:
            size = int(size_entry.get()) + 1  # Increase

        self.update_font_size(size)
        self.remove_font_entry(size_entry, size)

        return

    def update_font_size(self, size):
        with open("settings.json", 'r') as file:
            settings = json.load(file)
        file.close()

        settings["title_size"] = size

        with open("settings.json", 'w') as file:
            json.dump(settings, file)
        file.close()

        # Update the size on this page
        self.title.destroy()
        self.title = ctk.CTkLabel(self.f_title, text='Settings', font=QuizManager.get_title_font())
        self.title.pack()

        return


    def remove_font_entry(self, font_entry, new_size):
        # Remove current value of entry
        font_entry.delete(0, last_index=ctk.END)
        font_entry.insert(0, new_size)

    def submission(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        Home.Home(frame)
