import customtkinter as ctk

import Home

# Define attributes of CTK
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("themes/mytheme.json")

# Define root widget
root = ctk.CTk()
# Start Home Page
Home.Home(root)
# Tkinter loop
root.mainloop()
