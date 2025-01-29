from mt import ensure_venv, y_n, better_input, type_input, path
ensure_venv(__file__)

import os
from time import sleep
from copy import deepcopy
from typing import Literal
from papertools import Console, File, Dir


def ausgabe(game: list[list[int]], mode: Literal['xy', 'y'] = 'xy') -> None:
    Console.clear()
    symbols: list[str] = [' ', 'X', 'O', '?']
    colours: list = ['red', 'red', 'green', 'yellow']
    for y in range(COL):
        print(f'   {chr(y + 97)}  ', end='')
    print()
    for x in range(ROW):
        print(' ', end='')
        for y in range(COL - 1):
            print('     |', end='')
        print(f'\n{x + 1}  ' if mode == 'xy' else '\n   ', end='')
        Console.print_colour(
            f'{symbols[game[x][0]]}  ', colours[game[x][0]], end='')
        for y in range(COL - 1):
            print('|  ', end='')
            Console.print_colour(
                f'{symbols[game[x][y + 1]]}  ', colours[game[x][y + 1]], end='')
        print('\n ', end='')

        if x != ROW - 1:
            for y in range(COL):
                print('_____|' if y != COL - 1 else '_____', end='')
        else:
            for y in range(COL - 1):
                print('     |', end='')
        print()


def turn(game: list[list[int]], second_pass: tuple[int, int] = (-1, -1)) -> tuple[int, int]:
    try:
        if second_pass != (-1, -1):
            game2: list[list[int]] = deepcopy(game)
            game2[second_pass[0]][second_pass[1]] = 3
            ausgabe(game2)
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
            return turn(game)

        return x, y
    except:
        return turn(game)


def turn_x(game: list[list[int]], second_pass: int = -1) -> int:
    try:
        if second_pass != -1:
            game2: list[list[int]] = deepcopy(game)
            game2[0][second_pass] = 3
            ausgabe(game2, 'y')
            inp: str = better_input('... ', 1, 1, False, True, True)
            if inp == '':
                return second_pass
        else:
            inp: str = better_input('>>> ', 1, 1, False, True)

        x = ord(inp) - 97

        if game[0][x] != 0:
            return turn_x(game)

        return x
    except:
        return turn_x(game, second_pass)


def won(char_inp: str, game: list[list[int]]) -> bool:
    char: int = [' ', 'X', 'O'].index(char_inp)

    def vertical() -> bool:
        for row in game:
            count: int = 0
            for c in row:
                if c == char:
                    count += 1
                    if count == NEEDED:
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
                    if count == NEEDED:
                        return True
                else:
                    count = 0
        return False

    def diagonal() -> bool:
        for i in range(ROW):
            for j in range(COL):
                if i + NEEDED <= ROW and j + NEEDED <= COL:
                    count: int = 0
                    for k in range(NEEDED):
                        if game[i + k][j + k] == char:
                            count += 1
                            if count == NEEDED:
                                return True
                        else:
                            count = 0
                if i + NEEDED <= ROW and j - NEEDED >= -1:
                    count: int = 0
                    for k in range(NEEDED):
                        if game[i + k][j - k] == char:
                            count += 1
                            if count == NEEDED:
                                return True
                        else:
                            count = 0
        return False

    return vertical() or horizontal() or diagonal()


def new_game() -> dict:
    settings: dict = {
        'p1': USER,
        'p2': '',
        'game': [[0 for _ in range(COL)] for _ in range(ROW)],
        'current': 1,
        'row': ROW,
        'col': COL,
        'needed': NEEDED,
        'gravity': GRAVITY
    }
    return settings


def add_w_gravity(game: list[list[int]], x: int, turn: int) -> None:
    for y in range(ROW):
        if game[y][x] != 0:
            game[y - 1][x] = turn + 1
            return
    game[ROW - 1][x] = turn + 1


def get_free_games() -> list[str]:
    games: list[str] = [file for file in Dir.listfiles(path)
                        if file.startswith('t_') and file.endswith('.json')]
    out: list[str] = []
    for file in games:
        content: dict = File(os.path.join(
            path, file)).json_r()
        if content.get('p2') == '':
            out.append(file.removeprefix('t_').removesuffix('.json'))
    return out


global CONFIRM, USER


def generate_config() -> None:
    global CONFIRM, USER
    print("config.json wurde erstellt, bitte fülle die Felder aus.")
    inp: dict = stgs_file.json_r()
    CONFIRM = y_n('Bestätigungsmodus an? (Y/n)')
    USER = better_input('Name: ', 3, 10, False)
    inp['ttt'] = {"confirm": CONFIRM, "user": USER}
    stgs_file.json_w(inp)


stgs_file: File = File("config.json")
if stgs_file.exists():
    try:
        stgs: dict = stgs_file.json_r()['ttt']
        CONFIRM = stgs['confirm']
        USER = stgs['user']
        USER = better_input('Name: ', 3, 10, False, True, True) or USER
    except:
        generate_config()
else:
    stgs_file.json_w({})
    generate_config()

print(f'Verfügbare Spiele: {", ".join(get_free_games())}')
SHORT_PATH: str = better_input('Pfad: ', 2, 10, False)
PATH: str = os.path.join(
    path, f't_{SHORT_PATH}.json')

if SHORT_PATH in get_free_games():
    print('Lädt Spiel')
    file: dict = File(PATH).json_r()
    file['p2'] = USER
    ROW: int = file['row']
    COL: int = file['col']
    NEEDED: int = file['needed']
    GRAVITY: bool = file['gravity']
    SELF: int = 0
    File(PATH).json_w(file)
    print('Spiel geladen')
    ausgabe(file['game'], 'y' if GRAVITY else 'xy')
else:
    print('Erstellt neues Spiel')
    ROW: int = type_input('Reihen: ', int, True) or 3
    COL: int = type_input('Spalten: ', int, True) or 3
    NEEDED: int = type_input('Benötigte Verbundene: ', int, True) or 3
    GRAVITY: bool = y_n('Schwerkraft? (Y/n)', True) or False
    file: dict = new_game()
    File(PATH).json_w(file)
    print('Spiel erstellt')
    print('Warte auf anderen Spieler', end='')
    while file.get('p2') == '':
        file = File(PATH).json_r()
        print('.', end='', flush=True)
        sleep(1)
    SELF: int = 1
    print(f'Spieler {file["p2"]} ist beigetreten')

current: int = file['current']
p1: str = file['p1']
p2: str = file['p2']
symbols: list[str] = [' ', 'X', 'O']
symbols2: list[str] = [' ', 'O', 'X']
end: bool = False

while True:
    while not file['current'] == SELF:
        file = File(PATH).json_r()
        sleep(0.5)
    game: list[list[int]] = file['game']
    ausgabe(game, 'y' if GRAVITY else 'xy')
    if won(symbols2[SELF + 1], game):
        print(f'{p2} hat gewonnen!!!')
        input()
        exit()

    if GRAVITY:
        x = turn_x(game)
        if CONFIRM:
            x = turn_x(game, x)
        print(f'{x=}')
        add_w_gravity(game, x, file['current'])
    else:
        x, y = turn(game)
        if CONFIRM:
            x, y = turn(game, (x, y))
        game[x][y] = file['current'] + 1

    file['current'] += 1
    file['current'] %= 2
    ausgabe(game, 'y' if GRAVITY else 'xy')
    if won(symbols[SELF + 1], game):
        print(f'{p1} hat gewonnen!!!')
        end = True

    File(PATH).json_w(file)
    if end:
        input()
        exit()
