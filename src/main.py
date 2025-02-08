# main.py
import customtkinter as ctk
from gui_test import App
#from gui import SurahSelection, OverlayWindow

# def on_surah_selected(surah_id):
#     # When a surah is selected, open the overlay window.
#     overlay = OverlayWindow(surah_id)
#     overlay.mainloop()

if __name__ == "__main__":
    # Set CustomTkinter appearance to dark mode (minimalist design).
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    # Start the surah selection window.
    app = App()
    app.mainloop()
