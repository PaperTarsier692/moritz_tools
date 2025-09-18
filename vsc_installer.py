from mt import ensure_venv
ensure_venv(__file__)

import os
import requests
from shutil import rmtree
from getpass import getuser
from papertools import Console

try:
    oldFolder: str = f'C:\\Users\\{getuser()}\\vsc\\'
    Console.print_colour(
        "Stelle sicher dass keine Instanz von VSC noch läuft, dann drücke Enter", 'red')
    input()

    if os.path.exists(oldFolder):
        Console.print_colour(
            'Alte Installation von vsc von moritz_tools gefunden, wird gelöscht...', 'yellow')
        rmtree(oldFolder)

    folder: str = 'C:\\Users\\Public\\vsc\\'

    Console.print_colour(
        'Lädt VSC herunter...', 'red')

    response: requests.Response = requests.get(
        'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user')

    installer: str = f'C:\\Users\\{getuser()}\\vsc.exe'

    if response.status_code == 200:
        with open(installer, 'wb') as f:
            f.write(response.content)
        Console.print_colour('VSC heruntergeladen', 'green')
    else:
        Console.print_colour('VSC konnte nicht heruntergeladen werden', 'red')

    Console.print_colour('Installiert VSC', 'yellow')

    os.makedirs(
        folder, exist_ok=True)

    os.system(
        f'{installer} /SP- /VERYSILENT /LOG="log.txt" /NOCANCEL /NORESTART /FORCECLOSEAPPLICATIONS /DIR="{folder}"')

    Console.print_colour('VSC installiert, löscht Installationsdatei', 'green')
    os.remove(installer)

    os.system(
        f'{folder}code.exe --install-extension ms-vscode.cpptools --install-extension danielpinto8zz6.c-cpp-compile-rundanielpinto8zz6.c-cpp-compile-run')

    os.system('setx Path "C:\\Program Files\\CodeBlocks\\MinGW\\bin; %USERPROFILE%\\AppData\\Local\\Microsoft\\WindowsApps"')


finally:
    Console.print_colour('Drücke Enter um das Fenster zu schließen', 'green')
    input()
