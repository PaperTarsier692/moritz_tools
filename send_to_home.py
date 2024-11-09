from mt import ensure_venv
ensure_venv(__file__)

from papertools import File, Console
from shutil import make_archive
from mt import y_n
import os

Console.clear()

try:
    from requests import post, exceptions, Response
except ModuleNotFoundError or ImportError:
    if y_n("Modul Requests nicht gefunden, soll es heruntergeladen werden?\
            (Y/n)"):
        os.system("pip install requests")
        from requests import post, exceptions, Response
    else:
        print('Beenden')
        exit()

print("SEND TO HOME . PY von Moritz Harrer")

PATH: str = os.path.abspath(os.path.join(__file__, os.pardir))
print(f'Path: {PATH}')

stgs_file: File = File(f"{PATH}/config.json")
if stgs_file.exists():
    stgs: dict = stgs_file.json_r()
else:
    print("config.json wurde erstellt, bitte fülle die Felder aus.")
    username: str = input('Username: ').strip()
    url: str = 'https://discord.com/api/webhooks/' + \
        input('Webhook URL: https://discord.com/api/webhooks/').strip()
    stgs: dict = {"url": url, "username": username}
    stgs_file.json_w(stgs)

URL: str = stgs["url"]
USERNAME: str = stgs["username"]

Console.print_colour(
    '"/shortcut_on" / "/shortcut_off" für das einstellen des Kontextmenü Shortcuts', 'yellow')


class Webhook:
    def __init__(self, url: str, username: str) -> None:
        self.url: str = url
        self.username: str = username

    def send(self, content: str) -> int:
        try:
            return post(
                self.url, json={"content": content, "username":
                                self.username}).status_code
        except exceptions.MissingSchema or exceptions.InvalidURL:
            print("<<<Webhook URL ist ungültig.>>>")
            return 0

    def send_file(self, content: bytes, file_name: str) -> int:
        response: Response = post(self.url, json={"username": self.username},
                                  files={
            'file': (file_name, content)})
        try:
            if int(response.json().get('code')) == 40005:
                print("<<<Datei zu groß für Discord>>>")
                return 0
        except TypeError:
            pass
        return response.status_code

    def print_status(self, status_code: int) -> None:
        if status_code == 204 or status_code == 200:
            print(f"<<<Erfolgreich versendet, Code {status_code}.>>>")
        elif status_code != 0:
            print(
                f"<<<Fehler beim senden, Code {status_code}, \
                    ist die URL korrekt?>>>")


class SendToHome:
    def __init__(self, wh: Webhook) -> None:
        self.wh: Webhook = wh
        self.bat_content: str = f'''@echo off
        python {os.path.abspath(__file__)}'''
        self.bat()

    def run(self, inp: str) -> None:
        if inp == '/shortcut_on':
            self.create_sc()
        elif inp == '/shortcut_off':
            self.remove_sc()
        path: str = os.path.abspath(inp.replace('"', ''))
        if os.path.isfile(path):
            file_name: str = os.path.basename(path)
            with open(path, "rb") as f:
                content: bytes = f.read()
            print("Pfad erkannt, sendet Datei.")
            self.wh.print_status(self.wh.send_file(content, file_name))

        elif os.path.isdir(path):
            try:
                print("Ordner erkannt, komprimiert Ordner...")
                make_archive(path,
                             'zip', path)
                zip_path: str = f"{path}.zip"
                with open(zip_path, "rb") as f:
                    content: bytes = f.read()
                print("Sendet Ordner")
                self.wh.print_status(self.wh.send_file(
                    content, f"{os.path.basename(path)}.zip"))
                os.remove(zip_path)
            except Exception as e:
                print(
                    "Fehler beim komprimieren des Ordners, gibt es noch genug \
                        Speicherplatz auf deinem Account?")
                print(e)
        else:
            self.wh.print_status(self.wh.send(inp))

    def bat(self) -> None:
        shortcut: File = File("Z:/Desktop/send_to_home.bat")
        if shortcut.exists() and shortcut.read() == self.bat_content:
            return
        print("send_to_home.bat wird erstellt.")
        shortcut.write(self.bat_content)

    def create_sc(self) -> None:
        from context_menu import menus
        from sys import executable
        fc = menus.FastCommand('Send To Home', type='FILES',
                               command=f'Z: && cd Z:\\Documents\\moritz_tools && "{executable}" "Z:\\Documents\\moritz_tools\\send_to_home_sc.py" ?', command_vars=['FILENAME'])
        fc.compile()
        fc2 = menus.FastCommand('Send To Home', type='DIRECTORY',
                                command=f'Z: && cd Z:\\Documents\\moritz_tools && "{executable}" "Z:\\Documents\\moritz_tools\\send_to_home_sc.py" ?', command_vars=['FILENAME'])
        fc2.compile()

    def remove_sc(self) -> None:
        from context_menu import menus
        menus.removeMenu('Send To Home', 'FILES')
        menus.removeMenu('Send to home', 'DIRECTORY')


sth: SendToHome = SendToHome(Webhook(URL, USERNAME))

while True:
    sth.run(input(">>> ").strip())
