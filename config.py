from mt import ensure_venv, fix_res, theme
ensure_venv(__file__)

from papertools import File, Cfg

fix_res()

config: str = '''
[chat]
user=
theme=

[ttt]
user=
clear=
confirm=

[sth]
url=
user=
context=
shortcut=

[other]
path=
unc=
'''


class GUI:
    def __init__(self) -> None:
        self.theme: str = 'equilux'
        self.root: ThemedTk = ThemedTk(theme='equilux')
        self.themes: list[str] = self.root.get_themes()

        self.style: ThemedStyle = ThemedStyle()

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

        self.apply_theme(self.theme)
        self.root.mainloop()

    def apply_theme(self, theme: str) -> None:
        self.root.title(f'Config - {theme.capitalize()}')
        self.root.set_theme(theme)
        self.style.theme_use(theme)
        bg_color = self.style.lookup('TFrame', 'background') or '#000'
        fg_color = self.style.lookup('TLabel', 'foreground') or '#FFF'

        for widget in self.root.winfo_children():
            self._apply_widget_theme(widget, bg_color, fg_color)

    def _apply_widget_theme(self, widget, bg_color, fg_color):
        if isinstance(widget, Frame):
            widget.config(bg=bg_color)
        elif isinstance(widget, Label):
            widget.config(background=bg_color, foreground=fg_color)
        elif isinstance(widget, Text):
            widget.config(background=bg_color, foreground=fg_color)
        for child in widget.winfo_children():
            self._apply_widget_theme(child, bg_color, fg_color)

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
                    if theme(self.entries[group][name].get(
                            '1.0', 'end-1c'), True).exists:
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


if __name__ == '__main__':
    from tkinter.ttk import Button, Label, Radiobutton
    from tkinter import Text, Frame, BooleanVar
    from ttkthemes import ThemedTk, ThemedStyle
    gui: GUI = GUI()
