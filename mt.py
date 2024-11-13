import os
import sys
from typing import Any

test_env: bool = os.path.exists('.test_env')
laptop: bool = os.path.exists('.laptop')
venv: bool = hasattr(sys, 'real_prefix') or (
    hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
venv_available: bool = os.path.exists('.venv')
current_path: str = os.path.abspath(
    os.path.join(os.path.abspath(__file__), os.pardir))
windows: bool = os.name == 'nt'
try:
    from papertools import File
    path: str = File('config.json').json_r().get('path') or 'Y:/2BHIT/test/'
except:
    path: str = 'Y:/2BHIT/test/'


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
            if windows:
                os.system(
                    f'.\\.venv\\Scripts\\activate.bat && python "{file}" {" ".join(args)}')
            else:
                os.system(
                    f'source .venv/bin/activate && python "{file}" {" ".join(args)}')
        else:
            os.system(
                f"Z: && cd Z:\\Documents\\moritz_tools && .\\.venv\\Scripts\\activate.bat && python {file} {' '.join(args)}")
            exit()


def better_input(prompt: str, min_len: int = 0, max_len: int = 0, allow_spaces: bool = True, silent: bool = False, allow_empty: bool = False, halal: bool = True) -> str:
    while True:
        inp: str = input(prompt).strip()

        if inp == '' and allow_empty:
            return ''

        if len(inp) < min_len:
            if not silent:
                print('Eingabe zu kurz')
            continue

        if len(inp) > max_len:
            if not silent:
                print('Eingabe zu lang')
            continue

        if not allow_spaces and ' ' in inp:
            if not silent:
                print('Eingabe enthält Abstände')
            continue

        return inp


def better_getpass(prompt: str, min_len: int = 0, max_len: int = 0, allow_spaces: bool = True, silent: bool = False, allow_empty: bool = False, halal: bool = True) -> str:
    from getpass import getpass

    while True:
        inp: str = getpass(prompt).strip()

        if inp == '' and allow_empty:
            return ''

        if halal and ('neg' in inp or 'nig' in inp):
            continue

        if len(inp) < min_len:
            if not silent:
                print('Eingabe zu kurz')
            continue

        if len(inp) > max_len:
            if not silent:
                print('Eingabe zu lang')
            continue

        if not allow_spaces and ' ' in inp:
            if not silent:
                print('Eingabe enthält Abstände')
            continue

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


class theme:
    def __init__(self, theme: str, error_ok: bool = False) -> None:
        from ttkthemes.themed_style import ThemedStyle
        self.exists: bool = theme in ThemedStyle().theme_names()
        if not error_ok and not self.exists:
            raise ValueError('Theme not found')


def add_sth_sc() -> None:
    from context_menu import menus
    from sys import executable
    fc = menus.FastCommand('Send To Home', type='FILES',
                           command=f'Z: && cd Z:\\Documents\\moritz_tools && "{executable}" "Z:\\Documents\\moritz_tools\\send_to_home_sc.py" ?', command_vars=['FILENAME'])
    fc.compile()
    fc2 = menus.FastCommand('Send To Home', type='DIRECTORY',
                            command=f'Z: && cd Z:\\Documents\\moritz_tools && "{executable}" "Z:\\Documents\\moritz_tools\\send_to_home_sc.py" ?', command_vars=['FILENAME'])
    fc2.compile()
