from mt import ensure_venv, fix_res
ensure_venv(__file__)

from tkinter.ttk import Notebook, Frame
from ttkthemes import ThemedTk, ThemedStyle
import chat

fix_res()

pswd: str = 'testpswd'


class GUI:
    def __init__(self, theme: str) -> None:
        self.theme: str = theme
        self.root: ThemedTk = ThemedTk(theme=self.theme)
        self.style: ThemedStyle = ThemedStyle(self.root, theme=self.theme)

        self.notebook: Notebook = Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.chat_widget: Frame = Frame(
            self.notebook)
        self.chat: chat.GUI = chat.GUI(self.chat_widget, 'c_chat_test.json',
                                       pswd, 'Ich')
        self.chat_widget.pack(fill='both', expand=True)
        self.notebook.add(self.chat_widget, text='Chat', state='normal')
        print('Es ist so weit gekommen')
        self.apply_theme(self.theme)
        self.root.mainloop()
        self.chat.chat.close()

    def apply_theme(self, theme: str) -> None:
        self.root.title(f'Config - {theme.capitalize()}')
        self.root.set_theme(theme)
        self.style.theme_use(theme)
        bg_color = self.style.lookup('TFrame', 'background') or '#000'
        fg_color = self.style.lookup('TLabel', 'foreground') or '#FFF'
        self.apply_theme_widgets(self.root, bg_color, fg_color)

    def apply_theme_widgets(self, widget, bg_color, fg_color):
        try:
            widget.config(background=bg_color, foreground=fg_color)
        except:
            pass
        try:
            widget.config(foreground=fg_color)
        except:
            pass
        for child in widget.winfo_children():
            self.apply_theme_widgets(child, bg_color, fg_color)

    def add_categorys(self, theme):
        pass


gui: GUI = GUI('equilux')
