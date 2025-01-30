from mt import ensure_venv, fix_res, Config, path
ensure_venv(__file__)

from ttkthemes import ThemedTk
from tkinter.ttk import Button
from papertools import File, Dir
from tkinter import Text
import os

fix_res()


class TTT:
    def __init__(self) -> None:
        self.root: ThemedTk = ThemedTk()
        self.root.geometry('800x800')
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
        self.root.mainloop()

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
                    self.root, text=f'{x} | {y}', command=lambda x=x, y=y: self.button_callback(x, y))
                button.grid(row=y * 2, column=x * 2, rowspan=2,
                            columnspan=2, sticky='nsew')
                self.buttons[y].append(button)
                self.root.grid_rowconfigure(y * 2, weight=1)
                self.root.grid_columnconfigure(x * 2, weight=1)

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


TTT()
