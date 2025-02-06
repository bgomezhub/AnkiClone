import customtkinter as ctk
import Model
import SettingsController


class Settings:
    def __init__(self, f_root):
        # Dynamic Font
        font = Model.get_fonts()
        self.font_title = ctk.CTkFont(family=font[0], size=font[1])
        self.font_body = ctk.CTkFont(family=font[0], size=font[2])
        # Root Frame
        self.f_page = ctk.CTkScrollableFrame(f_root)
        self.f_page.pack(fill='both', expand=True)

        # Title frame
        self.f_title = ctk.CTkFrame(self.f_page)
        self.f_title.pack(fill='y', expand=True)
        self.title = ctk.CTkLabel(self.f_title, text='Settings', font=self.font_title)
        self.title.pack(expand=True)
        self.title_body_ex = ctk.CTkLabel(self.f_title, text='Font Body Example', font=self.font_body)
        self.title_body_ex.pack(expand=True)
        # Setting options frame
        self.f_settings_options = ctk.CTkFrame(self.f_page)
        self.f_settings_options.pack(fill='y', expand=True)

        # Submission frame
        self.f_submission = ctk.CTkFrame(self.f_page)
        self.f_submission.pack(fill='y', expand=True)

        self.load_options()

        # Return to Home
        ctk.CTkButton(self.f_submission, text='Done', font=self.font_body,
                      command=lambda: SettingsController.submission(f_root)).pack(expand=True)


    def load_options(self):
        # Set daily new word limit
        SettingsController.load_daily_word(self.f_settings_options, self.font_body).grid(column=0, row=0)

        # Set font sizes
        SettingsController.load_font_title(self.f_settings_options, self.font_title, self.font_body).grid(column=0, row=1)
        SettingsController.load_font_body(self.f_settings_options, self.font_body, self.title_body_ex).grid(column=0, row=2)
        # Toggle dark/light mode
        SettingsController.load_appearance_mode(self.f_settings_options, self.font_body).grid(column=0, row=3)
        # Color of program
        SettingsController.load_colors(self.f_settings_options, self.font_body).grid(column=0, row=4)

        return
