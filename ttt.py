from papertools import Console, File

PATH: str = 'ttt.json'


def ausgabe(path: str) -> None:
    inp: dict = File(path).json_r()
    ui: list[str] = File('ttt.txt').readlines()
    symbols: list[str] = [' ', 'X', 'O']
    colours: list[str] = ['red', 'red', 'green']
    current: int = 0
    for line in ui:
        if not '-' in line:
            print(line)
        else:
            for char in line:
                if char == '-':
                    Console.print_colour(
                        symbols[inp['game'][current]], colours[inp['game'][current]], end='')
                    current += 1
                else:
                    print(char, end='')
            print()


def turn(path: str) -> int:
    def ask_for_input() -> int:
        try:
            inp: str = input('>>> ')
            if len(inp) > 2:
                return ask_for_input()
            values: list[str] = ['a', 'b', 'c']
            if inp[0].isalpha():
                inp = f'{inp[1]}{inp[0]}'
            if int(inp[0]) > 3 or int(inp[0]) < 1:
                return ask_for_input()
            return (values.index(inp[1].lower())) + ((int(inp[0])-1)*3)
        except Exception:
            return ask_for_input()
    out: int = ask_for_input()
    if File(path).json_r()['game'][out] != 0:
        return turn(path)
    return out


def won(char: str) -> bool:
    def horizontal() -> bool:
        count: int = 0
        for c in range(9):
            if c == char:
                count += 1
                if count == 3:
                    return True
            else:
                count = 0
        return False

    def vertical() -> bool:


current = 0
while True:
    ausgabe(PATH)
    inp: dict = File(PATH).json_r()
    selected: int = turn(PATH)
    print(selected)
    if inp['game'][selected] == 0:
        inp['game'][selected] = current + 1
    current += 1
    current %= 2
    File(PATH).json_w(inp)
