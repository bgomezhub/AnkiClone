import customtkinter as ctk
import Model
import controllers.Settings


class Settings:
    def __init__(self, f_root):
        # Dynamic Font
        font = Model.get_fonts()
        self.font_title = ctk.CTkFont(family=font[0], size=font[1])
        self.font_body = ctk.CTkFont(family=font[0], size=font[2])
        # Root Frame
        self.f_page = ctk.CTkFrame(f_root)
        self.f_page.pack(fill='both', expand=True)

        # Title frame
        self.f_title = ctk.CTkFrame(self.f_page)
        self.f_title.pack(fill='y', expand=True)
        self.f_title_ws = ctk.CTkFrame(self.f_title)
        self.f_title_ws.pack(expand=True)

        self.title = ctk.CTkLabel(self.f_title_ws, text='Settings', font=self.font_title)
        self.title.pack(pady=11)
        self.title_body_ex = ctk.CTkLabel(self.f_title_ws, text='Font Body Example', font=self.font_body)
        self.title_body_ex.pack(pady=11)
        # Setting options frame
        self.f_settings_options = ctk.CTkFrame(self.f_page)

        self.f_settings_options.pack(fill='y', expand=True)

        # Submission frame
        self.f_submission = ctk.CTkFrame(self.f_page)
        self.f_submission.pack(fill='y', expand=True)

        self.load_options()

        # Return to Home
        ctk.CTkButton(self.f_submission, text='Done', font=self.font_body,
                      command=lambda: controllers.Settings.submission(f_root)).pack(expand=True)


    def load_options(self):
        # Set daily new word limit
        controllers.Settings.load_daily_word(self.f_settings_options, self.font_body).pack(fill='x', expand=True)

        # Set font sizes
        controllers.Settings.load_font_title(self.f_settings_options, self.font_title, self.font_body).pack(fill='x', expand=True)
        controllers.Settings.load_font_body(self.f_settings_options, self.font_body, self.title_body_ex).pack(fill='x', expand=True)
        # Toggle dark/light mode
        controllers.Settings.load_appearance_mode(self.f_settings_options, self.font_body).pack(fill='x', expand=True)
        # Color of program
        controllers.Settings.load_colors(self.f_settings_options, self.font_body).pack(fill='x', expand=True)

        return
