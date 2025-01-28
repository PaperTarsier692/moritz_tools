from mt import ensure_venv
ensure_venv(__file__)

from tkinter.ttk import Button, Label, Radiobutton, Frame
from tkinter import Text, BooleanVar
from ttkthemes import ThemedStyle
from papertools import File
from typing import Callable


class GUI:
    def __init__(self, root: Frame, themes: list[str], save_callback: Callable) -> None:
        self.root: Frame = root
        self.themes: list[str] = themes
        self.style: ThemedStyle = ThemedStyle(root)
        self.save_callback: Callable = save_callback

        self.main_frame: Frame = Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

        self.cfg: dict = File('config.json').json_r()
        self.entries: dict = {}
        for group in self.cfg.keys():
            self.add_group(group)
            self.entries[group] = {}
            for key, value in self.cfg[group].items():
                self.add_option(group, key, value, type(value))

        self.button_frame: Frame = Frame(self.root)
        self.button_frame.pack(side='bottom', fill='x')

        self.button1: Button = Button(
            self.button_frame, text="Speichern", command=self.save)
        self.button1.pack(fill='x')

    def add_option(self, group: str, name: str, value: str, type: type) -> None:
        frame: Frame = Frame(self.main_frame)
        frame.pack(fill='x', padx=20, pady=1)

        label: Label = Label(frame, text=name)
        label.pack(side='left')

        if type == bool:
            var = BooleanVar(value=bool(value))
            true_button = Radiobutton(
                frame, text="True", variable=var, value=True)
            false_button = Radiobutton(
                frame, text="False", variable=var, value=False)
            true_button.pack(side='left', padx=5)
            false_button.pack(side='left', padx=5)
            self.entries[group][name] = var
        else:
            text_field: Text = Text(frame, height=1, width=20)
            text_field.insert('1.0', value)
            text_field.pack(side='left', padx=5, fill='x', expand=True)
            self.entries[group][name] = text_field

    def add_group(self, name: str) -> None:
        frame: Frame = Frame(self.main_frame)
        frame.pack(fill='x', padx=5, pady=5)

        label: Label = Label(frame, text=name)
        label.pack(side='left')

    def save(self) -> None:
        for group, options in self.cfg.items():
            for name in options.keys():
                if isinstance(self.entries[group][name], BooleanVar):
                    self.cfg[group][name] = self.entries[group][name].get()
                elif name == 'theme':
                    if self.entries[group][name].get(
                            '1.0', 'end-1c') in self.themes:
                        self.cfg[group][name] = self.entries[group][name].get(
                            '1.0', 'end-1c')
                        self.entries[group][name].config(bg=self.style.lookup(
                            'TFrame', 'background') or '#000')
                    else:
                        self.entries[group][name].config(bg='#800')
                elif name == 'user':
                    if len(self.entries[group][name].get(
                            '1.0', 'end-1c')) <= 10:
                        self.cfg[group][name] = self.entries[group][name].get(
                            '1.0', 'end-1c')
                        self.entries[group][name].config(bg=self.style.lookup(
                            'TFrame', 'background') or '#000')
                    else:
                        self.entries[group][name].config(bg='#800')
                else:
                    self.cfg[group][name] = self.entries[group][name].get(
                        '1.0', 'end-1c')
        File('config.json').json_w(self.cfg)
        self.save_callback(self.cfg)
