from mt import ensure_venv
ensure_venv(__file__)

import os
import requests
from papertools import Console
from getpass import getuser

try:
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

    if os.path.exists(f'C:\\Users\\{getuser()}\\vsc.exe\\'):
        Console.print_colour(
            'Andere Installation von vsc.exe gefunden, wird gelöscht...', 'yellow')
        os.remove(f'C:\\Users\\{getuser()}\\vsc.exe')

    Console.print_colour(
        'Lädt VSC herunter...', 'red')

    response: requests.Response = requests.get(
        'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user')

    if response.status_code == 200:
        with open(f'C:\\Users\\{getuser()}\\vsc.exe', 'wb') as f:
            f.write(response.content)
        Console.print_colour('VSC heruntergeladen', 'green')
    else:
        Console.print_colour('VSC konnte nicht heruntergeladen werden', 'red')

    Console.print_colour('Installiert VSC', 'yellow')

    os.makedirs(
        f'C:\\Users\\{getuser()}\\vsc\\', exist_ok=True)

    os.system(
        f'C:\\Users\\{getuser()}\\vsc.exe /SP- /VERYSILENT /LOG="log.txt" /NOCANCEL /NORESTART /FORCECLOSEAPPLICATIONS /DIR="C:\\Users\\{getuser()}\\vsc\\')

    Console.print_colour('VSC installiert, löscht Installationsdatei', 'green')
    os.remove(f'C:\\Users\\{getuser()}\\vsc.exe')

    os.system(
        f'C:\\Users\\{getuser()}\\vsc\\code.exe --install-extension ms-vscode.cpptools --install-extension danielpinto8zz6.c-cpp-compile-rundanielpinto8zz6.c-cpp-compile-run')

    os.system('setx Path "C:\\Program Files\\CodeBlocks\\MinGW\\bin; %USERPROFILE%\\AppData\\Local\\Microsoft\\WindowsApps"')


finally:
    Console.print_colour('Drücke Enter um das Fenster zu schließen', 'green')
    input()
