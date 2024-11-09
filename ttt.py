from mt import ensure_venv, y_n
ensure_venv(__file__)

import copy
from papertools import Console, File

PATH: str = 'ttt.json'

ROW: int = 4
COL: int = 5
NEEDED: int = 4
GRAVITY: bool = True


def ausgabe(game: list[list[int]]) -> None:
    symbols: list[str] = [' ', 'X', 'O', '?']
    colours: list = ['red', 'red', 'green', 'yellow']
    x: int = 0
    y: int = 0
    for y in range(COL):
        print(f'   {chr(y + 97)}  ', end='')
    print()
    for x in range(ROW):
        print(' ', end='')
        for y in range(COL - 1):
            print('     |', end='')
        print(f'\n{x + 1}  ', end='')
        Console.print_colour(
            f'{symbols[game[x][0]]}  ', colours[game[x][0]], end='')
        for y in range(COL - 1):
            print(f'|  ', end='')
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
            game2: list[list[int]] = copy.deepcopy(game)
            game2[second_pass[0]][second_pass[1]] = 3
            ausgabe(game2)
            inp: str = input('... ')
            if inp == '':
                return second_pass
        else:
            inp: str = input('>>> ')

        if len(inp) != 2:
            return turn(game)

        if inp[1].isalpha():  # A1
            inp = f'{inp[1]}{inp[0]}'

        y: int = ord(inp[0]) - 97
        x: int = int(inp[1]) - 1

        if game[x][y] != 0:
            return turn(game)

        return x, y
    except Exception:
        return turn(game)


def turn_x(game: list[list[int]], second_pass: int = -1) -> int:
    try:
        if second_pass != -1:
            inp: str = input('... ')
            if inp == '':
                return second_pass
        else:
            inp: str = input('>>> ')

        if len(inp) != 1:
            return turn_x(game)

        x = ord(inp) - 97

        if game[0][x] != 0:
            return turn_x(game)

        return x
    except Exception:
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
    return {'p1': 'SP1', 'p2': "SP2",
            'game': [[0 for _ in range(COL)]
                     for _ in range(ROW)], 'current': 1}
    return {'p1': input('<<<Spieler 1: >>> '),
            'p2': input('<<<Spieler 2: >>> '),
            'game': [[0 for _ in range(COL)]
                     for _ in range(ROW)], 'current': 1}


def add_w_gravity(game: list[list[int]], x: int, turn: int) -> None:
    for y in range(ROW):
        if game[y][x] != 0:
            game[y - 1][x] = turn + 1
            return
    game[ROW - 1][x] = turn + 1


global CONFIRM


def generate_config() -> None:
    global CONFIRM
    print("config.json wurde erstellt, bitte fülle die Felder aus.")
    inp: dict = stgs_file.json_r()
    CONFIRM = y_n('Bestätigungsmodus an? (Y/n)')
    inp['ttt'] = {"confirm": CONFIRM}
    stgs_file.json_w(inp)


stgs_file: File = File("config.json")
if stgs_file.exists():
    try:
        stgs: dict = stgs_file.json_r()['ttt']
        CONFIRM = stgs['confirm']
    except:
        generate_config()
else:
    stgs_file.json_w({})
    generate_config()

File(PATH).json_w(new_game())

current = 0

file: dict = File(PATH).json_r()

p1: str = file['p1']
p2: str = file['p2']


while True:
    file = File(PATH).json_r()
    game: list[list[int]] = file['game']
    ausgabe(game)
    if won('X', game):
        print(f'{p1} hat gewonnen!!!')
    elif won('O', game):
        print(f'{p2} hat gewonnen!!!')
    if GRAVITY:
        x = turn_x(game)
        if CONFIRM:
            x = turn_x(game, x)
        print(f'{x=}')
        add_w_gravity(game, x, current)
    else:
        x, y = turn(game)
        if CONFIRM:
            x, y = turn(game, (x, y))
        game[x][y] = current + 1
    current += 1
    current %= 2
    File(PATH).json_w(file)
