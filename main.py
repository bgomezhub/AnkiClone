import customtkinter as ctk
import json
import Home

with open("settings.json", 'r') as file:
    settings = json.load(file)

# Define attributes of CTK from settings
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
