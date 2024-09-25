import json

import customtkinter as ctk
import Home
import QuizManager


class SettingsPage:
    def __init__(self, frame):
        self.root_frame = frame
        # Dynamic Font
        font = QuizManager.get_fonts()
        self.font_title = ctk.CTkFont(family=font[0], size=font[1])
        self.font_body = ctk.CTkFont(family=font[0], size=font[2])
        # Title
        self.f_title = ctk.CTkFrame(frame)
        self.f_title.pack(padx=200, pady=50)
        self.title = ctk.CTkLabel(self.f_title, text='Settings', font=self.font_title)
        self.title.pack()
        # Handle Setting Options
        self.f_setting_options = ctk.CTkFrame(frame)
        self.f_setting_options.pack(padx=200, pady=50)
        self.title_spinbox = self.spinbox('title')
        self.body_spinbox = self.spinbox('body')
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
        file.close()

        # Set font sizes
        ctk.CTkLabel(self.f_setting_options, text="Title Font:", font=self.font_body).grid(column=0, row=0)
        self.title_spinbox.grid(column=1, row=0, pady=11)

        ctk.CTkLabel(self.f_setting_options, text="Body Font:", font=self.font_body).grid(column=0, row=1)
        self.body_spinbox.grid(column=1, row=1, pady=11)

        # Toggle dark/light mode
        ctk.CTkLabel(self.f_setting_options, text="Appearance (Dark/Light):", font=self.font_body).grid(column=0, row=2)
        if settings['appearance'] == 'light':
            switch_var = ctk.StringVar(value="on")
        else:
            switch_var = ctk.StringVar(value="off")
        appearance_switch = ctk.CTkSwitch(self.f_setting_options, text='', onvalue='on', offvalue='off',
                                          font=self.font_body, command=lambda: self.set_appearance_mode(switch_var),
                                          variable=switch_var)
        appearance_switch.grid(column=1, row=2, pady=11, padx=10)

        # Set color of program
        ctk.CTkLabel(self.f_setting_options, text="Color:", font=self.font_body).grid(column=0, row=3)

    def spinbox(self, font_type):
        # Create frame to house all widgets
        temp_frame = ctk.CTkFrame(self.f_setting_options)
        # Placed in the middle
        size_entry = ctk.CTkEntry(temp_frame, font=self.font_body, justify='center', width=(self.font_body.cget("size")+ 20))
        size_entry.grid(column=1, row=0)

        size_body = self.font_body.cget("size")
        # Input new size into entry
        if font_type == 'title':
            size_entry.insert(0, self.font_title.cget("size"))
        else:
            size_entry.insert(0, size_body)

        # Options placed on the sides, (-) == button, (+) == button2
        ctk.CTkButton(temp_frame, text="-", font=self.font_body,
                      command=lambda: self.spinbox_options(font_type, size_entry, -1),
                      width=(size_body + 5)).grid(column=0, row=0)
        ctk.CTkButton(temp_frame, text="+", font=self.font_body,
                      command=lambda: self.spinbox_options(font_type, size_entry, 1),
                      width=(size_body + 2)).grid(column=3, row=0)


        return temp_frame

    def spinbox_options(self, font_type, size_entry, change):
        if change == -1:
            size = int(size_entry.get()) - 1  # Decrease
        else:
            size = int(size_entry.get()) + 1  # Increase

        # Updates title size, writes default_size = size
        self.save_font_size(font_type, size)
        # Updates all body values and spinbox options
        if font_type == 'body':
            self.update_body_values(size)
        # Remove current entry value and replace with new size
        self.remove_font_entry(size_entry, size)

        return

    def save_font_size(self, font_type, size):
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
            self.font_title.configure(size=size)
        else:
            theme['CTkFont']['Windows']['size'] = size

        # Write into settings for startup of program
        with open(f"themes/{color}.json", 'w') as file:
            json.dump(theme, file, indent=2)
        file.close()

        return

    def update_body_values(self, size):
        # Update font size
        self.font_body.configure(size=size)
        # Update widgets to scale with body font size (Entry to contain number and buttons to be semi-congruent to entry)
        # body option
        b_widgets = self.body_spinbox.winfo_children()
        b_widgets[1].configure(width=(size + 3))  # (-) button is smaller in pixels than (+), scales proportionally for most font sizes
        b_widgets[2].configure(width=(size + 2))
        b_widgets[0].configure(width=(size + 20))
        # title option
        t_widgets = self.title_spinbox.winfo_children()
        t_widgets[1].configure(width=(size + 3))
        t_widgets[2].configure(width=(size + 2))
        t_widgets[0].configure(width=(size + 20))

        return

    def remove_font_entry(self, font_entry, new_size):
        # Remove current value of entry
        font_entry.delete(0, last_index=ctk.END)
        # Input new size into entry
        font_entry.insert(0, new_size)

        return

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

    def submission(self, root_frame):
        for widget in root_frame.winfo_children():
            widget.destroy()

        Home.Home(root_frame)

        return