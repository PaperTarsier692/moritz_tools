from mt import ensure_venv
ensure_venv(__file__)

import os
import ctypes
from papertools import Console

while True:
    processes: list[str] = os.popen(
        'wmic process get description').read().splitlines()
    processes = [process.strip() for process in processes if process != '']

    if 'Code.exe' in processes:
        Console.print_colour(
            'Visual Studio Code rennt noch, bitte schließe es um Probleme zu vermeiden.', 'red')
        input()
    else:
        break

while True:
    free_bytes: ctypes.c_ulonglong = ctypes.c_ulonglong(0)
    storage: int = ctypes.windll.kernel32.GetDiskFreeSpaceExW(
        ctypes.c_wchar_p('Z:'), None, None, ctypes.pointer(free_bytes))
    Console.print_colour(f'Freier Speicherplatz: {storage}', 'yellow')
    input()
