import os
import sys
from venv import create
from mt import ensure_venv, current_path, test_env, laptop, venv_available


def activate_venv() -> None:
    if os.path.basename(current_path) != 'moritz_tools':
        print('Parent Directory ist nicht moritz_tools, es könnten Daten verloren gehen. Drücke Enter um fortzufahren.')
        input()
    create('.venv', with_pip=True, upgrade_deps=True, clear=True)


def install_dependencies() -> None:
    os.system('pip install --upgrade -r requirements.txt')


print(f'Python Version: {sys.version}')

if not venv_available:
    print('Keine virtuelle Umgebung erkannt')
    if test_env:
        print('Test Umgebung festgestellt')
    if not laptop:
        print('.laptop nicht gefunden. Wenn du diese Datei auf deinem eigenen Laptop ausführst dann erstelle im moritz_tools Ordner eine Datei ".laptop" und führe dieses Skript erneut aus.')
        input()
        exit()
    activate_venv()

else:
    print('Virtuelle Umgebung erkannt')
    ensure_venv(__file__)
    install_dependencies()
