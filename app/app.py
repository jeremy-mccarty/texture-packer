import customtkinter as ctk

from tkinterdnd2 import TkinterDnD
from app.views.home_view import HomeView

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)

        self.title("Texture Packer")
        self.geometry("1080x640")
        self.configure(fg_color="#1c1c1c")

        container = ctk.CTkFrame(self, fg_color="#1c1c1c")
        container.pack(fill="both", expand=True)
        self.current_view = HomeView(container)
        self.current_view.pack(fill="both", expand=True)
