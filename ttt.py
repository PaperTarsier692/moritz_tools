from mt import ensure_venv
ensure_venv(__file__)

from papertools import Console, File

PATH: str = 'ttt.json'

ROW: int = 3
COL: int = 3
NEEDED: int = 3


def ausgabe(game: list[list[int]]) -> None:
    ui: list[str] = File('ttt.txt').readlines()
    symbols: list[str] = [' ', 'X', 'O']
    colours: list = ['red', 'red', 'green']
    x: int = 0
    y: int = 0
    for line in ui:
        if '-' not in line:
            print(line)
        else:
            for char in line:
                if char == '-':
                    Console.print_colour(
                        symbols[game[x][y]], colours[game[x][y]], end='')
                    x += 1
                else:
                    print(char, end='')
            print()
            y += 1
            x = 0


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
