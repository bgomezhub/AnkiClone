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

        # Title
        self.f_title = ctk.CTkFrame(self.f_page)
        self.f_title.pack(fill='y', expand=True)
        self.title = ctk.CTkLabel(self.f_title, text='Settings', font=self.font_title)
        self.title.pack(expand=True)
        # Handle Setting Options
        self.f_settings_options = ctk.CTkFrame(self.f_page)
        self.f_settings_options.pack(fill='y', expand=True)

        # Submission frame
        self.f_submission = ctk.CTkFrame(self.f_page)
        self.f_submission.pack(fill='y', expand=True)

        self.load_options()

        # Return to Home
        ctk.CTkButton(self.f_submission, text='Done', font=self.font_body,
                      command=lambda: SettingsController.submission(self.f_page)).pack(expand=True)


    def load_options(self):
        # Set daily new word limit
        SettingsController.load_daily_word(self.f_settings_options, self.font_body).grid(column=0, row=0)

        # Set font sizes
        SettingsController.load_font_title(self.f_settings_options, self.font_title, self.font_body).grid(column=0, row=1)
        # SettingsController.load_font_body(self.f_settings_options, self.font_body).grid(column=0, row=2)
        '''
        ctk.CTkLabel(f_settings_options, text="Title Font:", font=font_body).grid(column=0, row=1, columnspan=2)
        self.title_spinbox.grid(column=2, row=1, pady=11, columnspan=2)
    
        ctk.CTkLabel(f_settings_options, text="Body Font:", font=font_body).grid(column=0, row=2, columnspan=2)
        self.body_spinbox.grid(column=2, row=2, pady=11, columnspan=2)
    
        # Toggle dark/light mode
        ctk.CTkLabel(f_settings_options, text="Appearance (Dark/Light):", font=font_body).grid(column=0, row=3,
        settings = Model.get_settings()                                                                                       columnspan=2)
        if settings['appearance'] == 'light':
            switch_var = ctk.StringVar(value="on")
        else:
            switch_var = ctk.StringVar(value="off")
        appearance_switch = ctk.CTkSwitch(f_settings_options, text='', onvalue='on', offvalue='off',
                                          font=font_body, command=lambda: set_appearance_mode(switch_var),
                                          variable=switch_var)
        appearance_switch.grid(column=2, row=3, pady=11, padx=10, columnspan=2)
    
        # Set color of program
        SettingsController.color_options().grid(column=0, row=4, columnspan=4)'''

        return
