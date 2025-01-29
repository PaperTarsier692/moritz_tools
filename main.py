from mt import ensure_venv, fix_res, Config
ensure_venv(__file__)

from ttkthemes import ThemedTk, ThemedStyle
from tkinter.ttk import Notebook, Frame
from papertools import File
import config
import chat

fix_res()


class GUI:
    def __init__(self, theme: str) -> None:
        self.theme: str = theme
        self.root: ThemedTk = ThemedTk(theme=self.theme)
        self.root.geometry('800x600')
        self.style: ThemedStyle = ThemedStyle(self.root, theme=self.theme)

        self.notebook: Notebook = Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.chat_frame: Frame = Frame(
            self.notebook)
        self.chat_input_frame: Frame = Frame(self.chat_frame)

        self.chat = chat.GUI(self.chat_frame)

        self.chat_input: chat.InputGUI = chat.InputGUI(
            self.chat_input_frame, self.chat, self.style)
        self.chat_input_frame.pack(fill='both', expand=True)

        self.notebook.add(self.chat_frame, text='Chat', state='normal')
        print('Chat added')

        self.config_frame: Frame = Frame(self.notebook)
        self.config: config.GUI = config.GUI(
            self.config_frame, self.root.get_themes(), self.save_callback)
        self.config_frame.pack(fill='both', expand=True)
        self.notebook.add(self.config_frame, text='Config', state='normal')
        print('Config added')

        print('Finished adding categories')
        self.notebook.bind('<<NotebookTabChanged>>', self.set_name)
        self.apply_theme(self.theme)
        self.root.mainloop()
        self.chat.chat.close()

    def set_name(self, *args) -> None:
        print('Titel aktualisiert')
        self.root.title(
            f'{self.notebook.tab(self.notebook.index("current"), "text")} - {self.theme.capitalize()}')

    def apply_theme(self, theme: str) -> None:
        self.theme = theme
        self.root.set_theme(theme)
        self.style.theme_use(theme)
        bg_color = self.style.lookup('TFrame', 'background') or '#000'
        fg_color = self.style.lookup('TLabel', 'foreground') or '#FFF'
        self.apply_theme_widgets(self.root, bg_color, fg_color)
        self.set_name()

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

    def save_callback(self, cfg: dict) -> None:
        print('Config gespeichert')
        self.apply_theme(cfg['common']['theme'])


cfg: Config = Config()
try:
    assert cfg.get_value_from_path('common/theme') == None
except:
    cfg.write_value_to_path('common/theme', 'equilux')

gui: GUI = GUI(cfg.cfg['common']['theme'])
