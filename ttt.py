from mt import ensure_venv
ensure_venv(__file__)

from papertools import Console, File

PATH: str = 'ttt.json'

ROW: int = 3
COL: int = 3
NEEDED: int = 3


def ausgabe(game: list[list[int]]) -> None:
    symbols: list[str] = [' ', 'X', 'O']
    colours: list = ['red', 'red', 'green']
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
            f'{symbols[game[0][x]]}  ', colours[game[0][x]], end='')
        for y in range(COL - 1):
            print(f'|  ', end='')
            Console.print_colour(
                f'{symbols[game[y + 1][x]]}  ', colours[game[y + 1][x]], end='')
        print('\n ', end='')

        if x != ROW - 1:
            for y in range(COL):
                print('_____|' if y != COL - 1 else '_____', end='')
        else:
            for y in range(COL - 1):
                print('     |', end='')
        print()


def turn(game: list[list[int]]) -> tuple[int, int]:
    try:
        inp: str = input('>>> ')
        if len(inp) != 2:
            return turn(game)

        if inp[1].isalpha():  # A1
            inp = f'{inp[1]}{inp[0]}'

        x: int = ord(inp[0]) - 97
        y: int = int(inp[1]) - 1

        if game[x][y] != 0:
            return turn(game)

        return x, y
    except Exception:
        return turn(game)


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
    x, y = turn(game)
    game[x][y] = current + 1
    current += 1
    current %= 2
    File(PATH).json_w(file)
