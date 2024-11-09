import os
import sys

test_env: bool = os.path.exists('.test_env')
current_path: str = os.path.abspath(
    os.path.join(os.path.abspath(__file__), os.pardir))
windows: bool = os.name == 'nt'


def y_n(inp: str) -> bool:
    if inp is not None:
        print(inp)
    res: str = input().strip().lower()
    return res == 'y' or res == 'j'


def ensure_venv(file: str, args: list[str] = []) -> None:
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        pass
    else:
        os.system(
            f"Z: && cd Z:\\Documents\\moritz_tools && .\\.venv\\Scripts\\activate.bat && python {file} {' '.join(args)}")
        exit()


def better_input(prompt: str, min_len: int = 0, max_len: int = 0, allow_spaces: bool = True, silent: bool = False) -> str:
    inp: str = input(prompt).strip()
    if max_len and len(inp) > max_len:
        if silent:
            inp = inp[:max_len]
        else:
            print('Eingabe zu lang')
            return better_input(prompt, min_len, max_len, allow_spaces, silent)
    if len(inp) < min_len:
        if not silent:
            print('Eingabe zu kurz')
        return better_input(prompt, min_len, max_len, allow_spaces, silent)
    if not allow_spaces and ' ' in inp:
        if not silent:
            print('Eingabe enthält Abstände')
        return better_input(prompt, min_len, max_len, allow_spaces, silent)
    return inp


def better_getpass(prompt: str, min_len: int = 0, max_len: int = 0, allow_spaces: bool = True, silent: bool = False) -> str:
    from getpass import getpass
    inp: str = getpass(prompt).strip()
    if max_len and len(inp) > max_len:
        if silent:
            inp = inp[:max_len]
        else:
            print('Eingabe zu lang')
            return better_getpass(prompt, min_len, max_len, allow_spaces, silent)
    if len(inp) < min_len:
        if not silent:
            print('Eingabe zu kurz')
        return better_getpass(prompt, min_len, max_len, allow_spaces, silent)
    if not allow_spaces and ' ' in inp:
        if not silent:
            print('Eingabe enthält Abstände')
        return better_getpass(prompt, min_len, max_len, allow_spaces, silent)
    return inp
