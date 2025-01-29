from mt import ensure_venv, y_n, better_input, type_input, path
ensure_venv(__file__)

import os
import sys
from time import sleep
from copy import deepcopy
from papertools import Console, File, Dir
from typing import Literal, Any, TextIO, Union


class OutputRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert('end', string)
        self.text_widget.see('end')

    def flush(self):
        pass


class TTT:
    def __init__(self, stdout: Union[TextIO, None] = None) -> None:
        if stdout is not None:
            sys.stdout = stdout
        self.stgs_file: File = File("config.json")
        if self.stgs_file.exists():
            try:
                stgs: dict[str, Any] = self.stgs_file.json_r()['ttt']
                self.confirm: bool = stgs['confirm']
                self.user: str = stgs['user']
                self.user = better_input(
                    'Name: ', 3, 10, False, True, True) or self.user
            except:
                self.generate_config()
        else:
            self.stgs_file.json_w({})
            self.generate_config()

        print(f'Verfügbare Spiele: {", ".join(self.get_free_games())}')
        self.short_path: str = better_input('Pfad: ', 2, 10, False)
        self.path: str = os.path.join(
            path, f't_{self.short_path}.json')

        if self.short_path in self.get_free_games():
            print('Lädt Spiel')
            file: dict = File(self.path).json_r()
            file['p2'] = self.user
            self.row: int = file['row']
            self.col: int = file['col']
            self.needed: int = file['needed']
            self.gravity: bool = file['gravity']
            self.self: int = 0
            File(self.path).json_w(file)
            print('Spiel geladen')
            self.ausgabe(file['game'], 'y' if self.gravity else 'xy')
        else:
            print('Erstellt neues Spiel')
            self.row: int = type_input('Reihen: ', int, True) or 3
            self.col: int = type_input('Spalten: ', int, True) or 3
            self.needed: int = type_input(
                'Benötigte Verbundene: ', int, True) or 3
            self.gravity: bool = y_n('Schwerkraft? (Y/n)', True) or False
            file: dict = self.new_game()
            File(self.path).json_w(file)
            print('Spiel erstellt')
            print('Warte auf anderen Spieler', end='')
            while file.get('p2') == '':
                file = File(self.path).json_r()
                print('.', end='', flush=True)
                sleep(1)
            self.self: int = 1
            print(f'Spieler {file["p2"]} ist beigetreten')

        p1: str = file['p1']
        p2: str = file['p2']
        symbols: list[str] = [' ', 'X', 'O']
        symbols2: list[str] = [' ', 'O', 'X']
        end: bool = False

        while True:
            while not file['current'] == self.self:
                file = File(self.path).json_r()
                sleep(0.5)
            game: list[list[int]] = file['game']
            self.ausgabe(game, 'y' if self.gravity else 'xy')
            if self.won(symbols2[self.self + 1], game):
                print(f'{p2} hat gewonnen!!!')
                input()
                exit()

            if self.gravity:
                x = self.turn_x(game)
                if self.confirm:
                    x = self.turn_x(game, x)
                print(f'{x=}')
                self.add_w_gravity(game, x, file['current'])
            else:
                x, y = self.turn(game)
                if self.confirm:
                    x, y = self.turn(game, (x, y))
                game[x][y] = file['current'] + 1

            file['current'] += 1
            file['current'] %= 2
            self.ausgabe(game, 'y' if self.gravity else 'xy')
            if self.won(symbols[self.self + 1], game):
                print(f'{p1} hat gewonnen!!!')
                end = True

            File(self.path).json_w(file)
            if end:
                input()
                exit()

    def ausgabe(self, game: list[list[int]], mode: Literal['xy', 'y'] = 'xy') -> None:
        Console.clear()
        symbols: list[str] = [' ', 'X', 'O', '?']
        colours: list = ['red', 'red', 'green', 'yellow']
        for y in range(self.col):
            print(f'   {chr(y + 97)}  ', end='')
        print()
        for x in range(self.row):
            print(' ', end='')
            for y in range(self.col - 1):
                print('     |', end='')
            print(f'\n{x + 1}  ' if mode == 'xy' else '\n   ', end='')
            Console.print_colour(
                f'{symbols[game[x][0]]}  ', colours[game[x][0]], end='')
            for y in range(self.col - 1):
                print('|  ', end='')
                Console.print_colour(
                    f'{symbols[game[x][y + 1]]}  ', colours[game[x][y + 1]], end='')
            print('\n ', end='')

            if x != self.row - 1:
                for y in range(self.col):
                    print('_____|' if y != self.col - 1 else '_____', end='')
            else:
                for y in range(self.col - 1):
                    print('     |', end='')
            print()

    def turn(self, game: list[list[int]], second_pass: tuple[int, int] = (-1, -1)) -> tuple[int, int]:
        try:
            if second_pass != (-1, -1):
                game2: list[list[int]] = deepcopy(game)
                game2[second_pass[0]][second_pass[1]] = 3
                self.ausgabe(game2)
                inp: str = better_input('... ', 2, 2, False, True, True)
                if inp == '':
                    return second_pass
            else:
                inp: str = better_input('>>> ', 2, 2, False, True)

            if inp[1].isalpha():  # A1
                inp = f'{inp[1]}{inp[0]}'

            y: int = ord(inp[0]) - 97
            x: int = int(inp[1]) - 1

            if game[x][y] != 0:
                return self.turn(game)

            return x, y
        except:
            return self.turn(game)

    def turn_x(self, game: list[list[int]], second_pass: int = -1) -> int:
        try:
            if second_pass != -1:
                game2: list[list[int]] = deepcopy(game)
                game2[0][second_pass] = 3
                self.ausgabe(game2, 'y')
                inp: str = better_input('... ', 1, 1, False, True, True)
                if inp == '':
                    return second_pass
            else:
                inp: str = better_input('>>> ', 1, 1, False, True)

            x = ord(inp) - 97

            if game[0][x] != 0:
                return self.turn_x(game)

            return x
        except:
            return self.turn_x(game, second_pass)

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
            for i in range(self.row):
                for j in range(self.col):
                    if i + self.needed <= self.row and j + self.needed <= self.col:
                        count: int = 0
                        for k in range(self.needed):
                            if game[i + k][j + k] == char:
                                count += 1
                                if count == self.needed:
                                    return True
                            else:
                                count = 0
                    if i + self.needed <= self.row and j - self.needed >= -1:
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

    def new_game(self) -> dict:
        settings: dict = {
            'p1': self.user,
            'p2': '',
            'game': [[0 for _ in range(self.col)] for _ in range(self.row)],
            'current': 1,
            'row': self.row,
            'col': self.col,
            'needed': self.needed,
            'gravity': self.gravity
        }
        return settings

    def add_w_gravity(self, game: list[list[int]], x: int, turn: int) -> None:
        for y in range(self.row):
            if game[y][x] != 0:
                game[y - 1][x] = turn + 1
                return
        game[self.row - 1][x] = turn + 1

    def get_free_games(self) -> list[str]:
        games: list[str] = [file for file in Dir.listfiles(path)
                            if file.startswith('t_') and file.endswith('.json')]
        out: list[str] = []
        for file in games:
            content: dict = File(os.path.join(
                path, file)).json_r()
            if content.get('p2') == '':
                out.append(file.removeprefix('t_').removesuffix('.json'))
        return out

    def generate_config(self) -> None:
        print("config.json wurde erstellt, bitte fülle die Felder aus.")
        inp: dict = self.stgs_file.json_r()
        self.confirm = y_n('Bestätigungsmodus an? (Y/n)')
        self.user = better_input('Name: ', 3, 10, False)
        inp['ttt'] = {"confirm": self.confirm, "user": self.user}
        self.stgs_file.json_w(inp)


TTT()
