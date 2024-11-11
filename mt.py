import os
import sys
from typing import Any

test_env: bool = os.path.exists('.test_env')
current_path: str = os.path.abspath(
    os.path.join(os.path.abspath(__file__), os.pardir))
windows: bool = os.name == 'nt'


def y_n(inp: str, allow_empty: bool = False) -> bool:
    if inp is not None:
        print(inp, end=' ')
    res: str = input().strip().lower()
    if allow_empty and res == '':
        return False
    return res == 'y' or res == 'j'


def ensure_venv(file: str, args: list[str] = []) -> None:
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        pass
    else:
        if test_env:
            os.system(
                f'.\\.venv\\Scripts\\activate.bat && python "{file}" {" ".join(args)}')
        else:
            os.system(
                f"Z: && cd Z:\\Documents\\moritz_tools && .\\.venv\\Scripts\\activate.bat && python {file} {' '.join(args)}")
            exit()


def better_input(prompt: str, min_len: int = 0, max_len: int = 0, allow_spaces: bool = True, silent: bool = False, allow_empty: bool = False) -> str:
    inp: str = input(prompt).strip()
    if inp == '':
        if allow_empty:
            return ''
        else:
            better_input(prompt, min_len, max_len,
                         allow_spaces, silent, allow_empty)
    if max_len and len(inp) > max_len:
        if silent:
            inp = inp[:max_len]
        else:
            print('Eingabe zu lang')
            return better_input(prompt, min_len, max_len, allow_spaces, silent, allow_empty)
    if len(inp) < min_len:
        if not silent:
            print('Eingabe zu kurz')
        return better_input(prompt, min_len, max_len, allow_spaces, silent, allow_empty)
    if not allow_spaces and ' ' in inp:
        if not silent:
            print('Eingabe enthält Abstände')
        return better_input(prompt, min_len, max_len, allow_spaces, silent, allow_empty)
    return inp


def better_getpass(prompt: str, min_len: int = 0, max_len: int = 0, allow_spaces: bool = True, silent: bool = False, allow_empty: bool = False) -> str:
    from getpass import getpass
    inp: str = getpass(prompt).strip()
    if inp == '':
        if allow_empty:
            return ''
        else:
            better_getpass(prompt, min_len, max_len,
                           allow_spaces, silent, allow_empty)
    if max_len and len(inp) > max_len:
        if silent:
            inp = inp[:max_len]
        else:
            print('Eingabe zu lang')
            return better_getpass(prompt, min_len, max_len, allow_spaces, silent, allow_empty)
    if len(inp) < min_len:
        if not silent:
            print('Eingabe zu kurz')
        return better_getpass(prompt, min_len, max_len, allow_spaces, silent, allow_empty)
    if not allow_spaces and ' ' in inp:
        if not silent:
            print('Eingabe enthält Abstände')
        return better_getpass(prompt, min_len, max_len, allow_spaces, silent, allow_empty)
    return inp


def type_input(prompt: str, type: type, allow_empty: bool = False) -> Any:
    inp: str = input(prompt).strip()
    if allow_empty and inp == '':
        return False
    try:
        return type(inp)
    except ValueError:
        return type_input(prompt, type)


def popup(title: str, prompt: str) -> None:
    if windows:
        import ctypes
        ctypes.windll.user32.MessageBoxW(  # type: ignore
            None, prompt, title, 0)
    else:
        import subprocess
        applescript: str = f"""
        display dialog "{prompt}" ¬
        with title "{title}" ¬
        with icon caution ¬
        buttons {{"OK"}}
        """
        subprocess.call(f"osascript -e '{applescript}'", shell=True)


def fix_res() -> None:
    import ctypes
    if windows:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # type: ignore
