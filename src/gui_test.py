import customtkinter as ctk
import tkinter as tk

class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Quran Overlay")
        self.geometry("400x600")
