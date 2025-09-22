from mt import ensure_venv
ensure_venv(__file__)

from papertools import Console, Dir
import os

if os.path.exists('Z:/Documents/moritz_tools/win11debloat'):
    Console.print_colour(
        'Win11Debloat gefunden, holt neueste Version ', 'green', end='')
    os.system('Z: && cd Z:/Documents/moritz_tools/win11debloat && git pull')
else:
    Console.print_colour('Lädt Win11Debloat herunter... ', 'green', end='')
    os.system(
        'Z: && cd Z:/Documents/moritz_tools && git clone https://github.com/Raphire/Win11Debloat.git win11debloat')


def apply_reg_file(reg_file_path: str) -> bool:
    if os.path.exists(reg_file_path):
        out: int = os.system(f'regedit /s "{reg_file_path}"')
        print(f'Code: {out}')
        return True
    else:
        Console.print_colour(
            f"Registry-Datei existiert nicht: {reg_file_path}", 'red')
        return False


for file in Dir.listfiles('Z:/Documents/moritz_tools/win11debloat/Regfiles/', abspath=True):
    Console.print_colour(f'Applying registry file {file}', 'yellow')
    apply_reg_file(file)
