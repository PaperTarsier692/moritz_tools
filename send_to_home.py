from requests import post, exceptions, Response
from shutil import make_archive
from json import dump, load
import os

if os.name == 'nt':
    os.system("cls")
else:
    os.system("clear")

print("SEND TO HOME . PY von Moritz Harrer")
PATH: os.PathLike = os.path.abspath(os.path.join(__file__, os.pardir))
print(f'Path: {PATH}')

if os.path.isfile(f"{PATH}/settings.json"):
    with open(f'{PATH}/settings.json', 'r') as f:
        stgs: dict[str, str] = load(f)
else:
    print("settings.json wurde erstellt, bitte fülle die Felder aus.")
    username: str = input('Username: ')
    url: str = input('Webhook URL: ')
    stgs: dict[str, str] = {"url": url, "username": username}
    with open(f'{PATH}/settings.json', 'w') as f:
        dump(stgs, f, indent=4)

URL: str = stgs["url"]
USERNAME: str = stgs["username"]


class Webhook:
    def __init__(self, url: str, username: str) -> None:
        self.url: str = url
        self.username: str = username

    def send(self, content: str) -> int:
        try:
            return post(
                self.url, json={"content": content, "username": self.username}).status_code
        except exceptions.MissingSchema or exceptions.InvalidURL:
            print("<<<Webhook URL ist ungültig.>>>")

    def send_file(self, content: bytes, file_name: str) -> int:
        response: Response = post(self.url, json={"username": self.username}, files={
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
                f"<<<Fehler beim senden, Code {status_code}, ist die URL korrekt?>>>")


class SendToHome:
    def __init__(self, wh: Webhook) -> None:
        self.wh: Webhook = wh
        self.bat_content: str = f'@echo off\npython {
            os.path.abspath(__file__)}'
        self.bat()

    def run(self, inp: str) -> None:
        path: os.PathLike = os.path.abspath(inp.replace('"', ''))
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
                zip_path: os.PathLike = f"{path}.zip"
                with open(zip_path, "rb") as f:
                    content: bytes = f.read()
                print("Sendet Ordner")
                self.wh.print_status(self.wh.send_file(
                    content, f"{os.path.basename(path)}.zip"))
                os.remove(zip_path)
            except Exception as e:
                print(
                    "Fehler beim komprimieren des Ordners, gibt es noch genug Speicherplatz auf deinem Account?")
                print(e)
        else:
            self.wh.print_status(self.wh.send(inp))

    def bat(self) -> None:
        if os.path.isfile(f"Z:/Desktop/send_to_home.bat"):
            with open(f"Z:/Desktop/send_to_home.bat", "r") as f:
                if f.read() == self.bat_content:
                    return
        print("send_to_home.bat wird erstellt.")
        with open(f"Z:/Desktop/send_to_home.bat", "w") as f:
            f.write(self.bat_content)


sth: SendToHome = SendToHome(Webhook(URL, USERNAME))

while True:
    sth.run(input(">>> "))
