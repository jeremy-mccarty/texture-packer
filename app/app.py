import customtkinter as ctk

from pathlib import Path
from PIL import Image, ImageTk
from tkinterdnd2 import TkinterDnD
from app.views.home_view import HomeView

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

_ICON_PATH = Path(__file__).parent.parent / "assets" / "icon.png"


class App(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)

        self.title("Texture Packer")
        self.geometry("1480x860")
        self.configure(fg_color="#1c1c1c")

        try:
            self._icon = ImageTk.PhotoImage(Image.open(_ICON_PATH))
            self.iconphoto(True, self._icon)
        except Exception:
            pass

        container = ctk.CTkFrame(self, fg_color="#1c1c1c")
        container.pack(fill="both", expand=True)
        self.current_view = HomeView(container)
        self.current_view.pack(fill="both", expand=True)
