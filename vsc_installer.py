from mt import ensure_venv
ensure_venv(__file__)

import os
import ctypes
from papertools import Console
from psutil import disk_usage

while True:
    processes: list[str] = os.popen(
        'wmic process get description').read().splitlines()
    processes = [process.strip() for process in processes if process != '']

    if 'Code.exe' in processes:
        Console.print_colour(
            'Visual Studio Code rennt noch, bitte schließe es um Probleme zu vermeiden.', 'red')
        inp: str = input()
        if inp == 'c':
            break
    else:
        break

while True:
    free_bytes: int = disk_usage('Z:\\').free
    Console.print_colour(
        f'Freier Speicherplatz: {free_bytes}', 'yellow')
    input()
