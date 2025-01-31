from mt import ensure_venv, fix_res, Config, path, check_str, deprecated
ensure_venv(__file__)
deprecated(__name__)

from ttkthemes import ThemedTk, ThemedStyle
from tkinter.ttk import Button, Frame, OptionMenu
from tkinter import Menu, StringVar
from papertools import File, Dir
from typing import Union
from tkinter import Text, Label, Event
import os

fix_res()


class TTT:
    def __init__(self, root: Frame) -> None:
        self.root: Frame = root
        self.root_frame: Frame = Frame(self.root)
        self.path: str = os.path.join(path, 't_ttt.json')
        self.user: str = 'User1'
        self.rows: int = 4
        self.cols: int = 3
        self.needed: int = 3
        self.gravity: bool = False
        self.game: list[list[int]] = [[0 for _ in range(self.cols)]
                                      for _ in range(self.rows)]
        self.buttons: list[list[Button]] = []
        self.generate_buttons()

    def new_game(self) -> dict:
        settings: dict = {
            'p1': self.user,
            'p2': '',
            'current': 0,
            'row': self.rows,
            'col': self.cols,
            'needed': self.needed,
            'gravity': self.gravity,
            'game': self.game
        }
        return settings

    def get_free_games(self) -> list[str]:
        games: list[str] = [file for file in Dir.listfiles(path)
                            if file.startswith('t_') and file.endswith('.json')]
        out: list[str] = []
        for file in games:
            content: dict = File(os.path.join(
                path, file)).json_r()
            if content.get('current') == 0:
                out.append(file.removeprefix('t_').removesuffix('.json'))
        return out

    def generate_buttons(self) -> None:
        for y in range(self.rows):
            self.buttons.append([])
            for x in range(self.cols):
                button = Button(
                    self.root_frame, text=f'{x} | {y}', command=lambda x=x, y=y: self.button_callback(x, y))
                button.grid(row=y * 2, column=x * 2, rowspan=2,
                            columnspan=2, sticky='nsew')
                self.buttons[y].append(button)
                self.root_frame.grid_rowconfigure(y * 2, weight=1)
                self.root_frame.grid_columnconfigure(x * 2, weight=1)

    def button_callback(self, x: int, y: int) -> None:
        print(f'Button {x} | {y} pressed')
        self.buttons[y][x].config(state='disabled', text='X')
        self.game[y][x] = 1

    def won(self, char_inp: str, game: list[list[int]]) -> bool:
        char: int = [' ', 'X', 'O'].index(char_inp)

        def vertical() -> bool:
            for row in game:
                count: int = 0
                for c in row:
                    if c == char:
                        count += 1
                        if count == self.needed:
                            return True
                    else:
                        count = 0
            return False

        def horizontal() -> bool:
            ngame: list[list[int]] = [list(row) for row in zip(*game)]
            for col in ngame:
                count: int = 0
                for c in col:
                    if c == char:
                        count += 1
                        if count == self.needed:
                            return True
                    else:
                        count = 0
            return False

        def diagonal() -> bool:
            for i in range(self.rows):
                for j in range(self.cols):
                    if i + self.needed <= self.rows and j + self.needed <= self.cols:
                        count: int = 0
                        for k in range(self.needed):
                            if game[i + k][j + k] == char:
                                count += 1
                                if count == self.needed:
                                    return True
                            else:
                                count = 0
                    if i + self.needed <= self.rows and j - self.needed >= -1:
                        count: int = 0
                        for k in range(self.needed):
                            if game[i + k][j - k] == char:
                                count += 1
                                if count == self.needed:
                                    return True
                            else:
                                count = 0
            return False

        return vertical() or horizontal() or diagonal()

    def wait_for_turn(self) -> None:
        self.root.after(1000, self.wait_for_turn)


class InputGUI:
    def __init__(self, root: Frame, ttt: TTT, style: ThemedStyle) -> None:
        self.root: Frame = root
        self.ttt: TTT = ttt
        self.user_label: Label = Label(self.root, text="User:")
        self.user_label.pack(anchor='center', pady=2)
        self.user_text: Text = Text(self.root, height=1, width=20)
        self.user_text.pack(anchor='center', pady=2)

        self.pswd_label: Label = Label(self.root, text="Password:")
        self.pswd_label.pack(anchor='center', pady=2)
        self.pswd_text: Text = Text(self.root, height=1, width=20)
        self.pswd_text.pack(anchor='center', pady=2)

        self.path_label: Label = Label(self.root, text="Game:")
        self.path_label.pack(anchor='center', pady=2)
        self.path_var: StringVar = StringVar(self.root)
        self.path_var.set("Select a game")
        self.path_menu: OptionMenu = OptionMenu(
            self.root, self.path_var, *self.ttt.get_free_games())
        self.path_menu.pack(anchor='center', pady=2)

        self.confirm: Button = Button(
            self.root, command=self.confirm_callback, text='Confirm')
        self.confirm.pack(anchor='center', pady=2)
        self.style: ThemedStyle = style
        for text in self.root.winfo_children():
            if isinstance(text, Text):
                text.bind("<Tab>", self.focus_next_widget)
                text.bind("<Return>", self.confirm_callback)
        self.update_games()

    def update_games(self) -> None:
        menu: Menu = self.path_menu['menu']
        print(type(menu))
        menu.delete(0, 'end')
        for game in self.ttt.get_free_games():
            menu.add_command(
                label=game, command=lambda value=game: self.path_var.set(value))
        self.root.after(2500, self.update_games)

    def focus_next_widget(self, event: Event) -> str:
        event.widget.tk_focusNext().focus()
        if isinstance(event.widget, Text):
            event.widget.tag_add("sel", "1.0", "end")
        return "break"

    def check_values(self, values: tuple[str, str]) -> bool:
        global out
        user, path = values
        out = True
        bg_color = self.style.lookup('TFrame', 'background') or '#000'
        self.user_text.config(bg=bg_color)

        def mark_wrong(**kwargs) -> None:
            print(f'Mark wrong: {kwargs}')
            global out
            out = False
            kwargs['mark'].config(bg='#800')  # type: ignore

        if not check_str(user, 3, 12, False, allow_empty=True):
            mark_wrong(mark=self.user_text)
        else:
            self.user_text.delete('1.0', 'end')
            self.user_text.insert('1.0', Config().smart_get(user, 'ttt/user',
                                                            error_callback=mark_wrong, mark=self.user_text))

        return out

    def confirm_callback(self, event: Union[Event, None] = None) -> None:
        print('MHM')
        if not self.check_values(self.get_values()):
            print('Falscher Input')
            return
        for child in self.root.winfo_children():
            child.pack_forget()
        self.root.after_cancel(self.update_games)  # type: ignore
        self.root.pack_forget()
        self.ttt.root_frame.pack(fill='both', expand=True)
        # self.ttt.login(self.get_values())

    def get_values(self) -> tuple[str, str]:
        path: str = self.path_var.get().strip()
        if not path.endswith('.json'):
            path = f'{path}/t_{path}.json'
        return self.user_text.get('1.0', 'end-1c').strip(), path
