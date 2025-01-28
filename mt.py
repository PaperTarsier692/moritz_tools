import os
import sys
from typing import Any, Callable, Union

test_env: bool = os.path.exists('.test_env')
venv: bool = hasattr(sys, 'real_prefix') or (
    hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
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
    inp: Union[str, None] = None
    while not check_str(inp, min_len, max_len, allow_spaces, silent, allow_empty, halal):
        inp = input(prompt).strip()
    return str(inp)


def better_getpass(prompt: str, min_len: int = 0, max_len: int = 0, allow_spaces: bool = True, silent: bool = False, allow_empty: bool = False, halal: bool = True) -> str:
    from getpass import getpass
    inp: Union[str, None] = None
    while not check_str(inp, min_len, max_len, allow_spaces, silent, allow_empty, halal):
        inp = getpass(prompt).strip()
    return str(inp)


def check_str(inp: Union[str, None], min_len: int = 0, max_len: int = 0, allow_spaces: bool = True, silent: bool = False, allow_empty: bool = False, halal: bool = True) -> bool:
    if inp is None:
        return False

    if inp == '' and allow_empty:
        return True

    if halal and ('neg' in inp or 'nig' in inp):
        return False

    if len(inp) < min_len:
        if not silent:
            print('Eingabe zu kurz')
        return False

    if max_len > 0 and len(inp) > max_len:
        if not silent:
            print('Eingabe zu lang')
        return False

    if not allow_spaces and ' ' in inp:
        if not silent:
            print('Eingabe enthält Abstände')
        return False

    return True


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


def add_sth_sc() -> None:
    from context_menu import menus
    from sys import executable
    fc = menus.FastCommand('Send To Home', type='FILES',
                           command=f'Z: && cd Z:\\Documents\\moritz_tools && "{executable}" "Z:\\Documents\\moritz_tools\\send_to_home_sc.py" ?', command_vars=['FILENAME'])
    fc.compile()
    fc2 = menus.FastCommand('Send To Home', type='DIRECTORY',
                            command=f'Z: && cd Z:\\Documents\\moritz_tools && "{executable}" "Z:\\Documents\\moritz_tools\\send_to_home_sc.py" ?', command_vars=['FILENAME'])
    fc2.compile()


def generate_random_string(length: int) -> str:
    import string
    import random
    letters: str = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def Webhook(url: str, content: Callable) -> None:
    from requests import post
    post(url, json={'content': f'{content()} {content}'})


def deprecated(name: str) -> None:
    if name == '__main__':
        from papertools import Console
        Console.print_colour(
            'Dieses Programm funktioniert nicht mehr so wie vorher und ist nun ein Teil von main.py. Führe main.py aus um das Programm weiterhin zu benutzen.', 'red')
        input()
        exit()


class Config:
    def __init__(self) -> None:
        self.file: File = File('config.json')
        self.check_cfg()
        self.cfg: dict[str, Any] = self.file.json_r()

    def check_cfg(self) -> None:
        if not self.file.exists():
            print('Config Datei nicht gefunden, wird neu erstellt')
            self.file.json_w({})
        try:
            self.cfg: dict[str, Any] = self.file.json_r()
        except Exception as e:
            print(f'Fehler beim Lesen der Config Datei: {e}')
            input()
            exit()

    def read(self) -> dict[str, Any]:
        self.cfg = self.file.json_r()
        return self.cfg

    def write(self, cfg: dict[str, Any]) -> None:
        self.cfg = cfg
        self.file.json_w(cfg)

    def smart_get(self, inp: str, path: str) -> Any:
        if inp.strip() == '':
            try:
                return self.get_value_from_path(path)
            except:
                self.write_value_to_path(path, inp)
                return inp
        else:
            return inp

    def get_value_from_path(self, path: str) -> Any:
        keys: list[str] = path.strip('/').split('/')
        value: Any = self.cfg
        for key in keys:
            value = value[key]
        return value

    def write_value_to_path(self, path: str, value: Any) -> None:
        keys: list[str] = path.strip('/').split('/')
        for key in keys[:-1]:
            value = value[key]
        value[keys[-1]] = value
