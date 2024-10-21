from papertools import Console, File

PATH: str = 'ttt.json'

ROW: int = 3
COL: int = 3


def ausgabe(game: list[list[int]]) -> None:
    ui: list[str] = File('ttt.txt').readlines()
    symbols: list[str] = [' ', 'X', 'O']
    colours: list = ['red', 'red', 'green']
    x: int = 0
    y: int = 0
    for line in ui:
        if not '-' in line:
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

        x: int = ord(inp[0])-97
        y: int = int(inp[1])-1

        if game[x][y] != 0:
            return turn(game)

        return x, y
    except:
        return turn(game)


def won(char: str, game: list[list[int]]) -> bool:
    def horizontal() -> bool:
        for row in game:
            if all([c == char for c in row]):
                return True
        return False

    def vertical() -> bool:
        for col in zip([game[i] for i in range(COL)]):
            if all([c == char for c in col]):
                return True
        return False

    print(f'{horizontal() = }')
    print(f'{vertical() = }')


current = 0
while True:
    file: dict = File(PATH).json_r()
    game: list[list[int]] = file['game']
    ausgabe(game)
    won('O', game)
    x, y = turn(game)
    print(x, y)
    game[x][y] = current + 1
    current += 1
    current %= 2
    File(PATH).json_w(file)
