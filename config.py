from mt import ensure_venv
ensure_venv(__file__)

from tkinter import Text
from tkinter.ttk import Button
from ttkthemes import ThemedTk, ThemedStyle


class GUI:
    def __init__(self) -> None:
        self.theme: str = 'equilux'
        self.root: ThemedTk = ThemedTk(theme='equilux')
        self.themes: list[str] = self.root.get_themes()

        self.style: ThemedStyle = ThemedStyle()

        self.root.title("Config")

        self.cmds_open: bool = False
        self.button1: Button = Button(
            self.root, text="Speichern", command=self.save)
        self.button1.pack(side='left', fill='x', expand=True)

        self.apply_theme(self.theme)
        self.root.mainloop()

    def apply_theme(self, theme: str) -> None:
        self.root.title(f'Chat Test {theme}')
        self.root.set_theme(theme)
        self.style.theme_use(theme)
        bg_color = self.style.lookup('TFrame', 'background') or '#000'
        fg_color = self.style.lookup('TLabel', 'foreground') or '#FFF'

    def save(self) -> None:
        pass


gui: GUI = GUI()
