import os

test_env: bool = os.path.exists('.test_env')


def y_n(inp: str) -> bool:
    if inp is not None:
        print(inp)
    res: str = input().strip().lower()
    return res == 'y' or res == 'j'
