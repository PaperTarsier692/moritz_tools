from mt import ensure_venv
ensure_venv(__file__)

import os
import requests
from papertools import Console
from getpass import getuser

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

response: requests.Response = requests.get(
    'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user')

if response.status_code == 200:
    with open('Z:\\Downloads\\vsc.exe', 'wb') as f:
        f.write(response.content)
    print('VSC heruntergeladen')
else:
    print('VSC konnte nicht heruntergeladen')

os.system(
    f'Z:\\Downloads\\vsc.exe /SP- /LOG="log.txt" /NOCANCEL /NORESTART /FORCECLOSEAPPLICATIONS /DIR="C:\\Users\\{getuser()}\\vsc\\')
