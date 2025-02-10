import customtkinter as ctk
from pages import Home
from Model import get_settings

# Define attributes of CTK from settings
settings = get_settings()
ctk.set_appearance_mode(settings['appearance'])
ctk.set_default_color_theme(f"themes/{settings['color']}.json")

# Define root widget
root = ctk.CTk()
# Set default size of program
root.geometry(f"{settings['screen_resolution']}")
# Start Home Page
Home.Home(root)
# Tkinter loop
root.mainloop()
