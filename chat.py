import os
import json
import base64
import ctypes
import platform
import threading
import pyperclip
from time import sleep
from getpass import getpass
from datetime import datetime
from papertools import Console, File


def nexit() -> None:
    Console.print_colour(
        "Drücken Sie enter um das Programm zu beenden.", "red")
    input()
    exit()


def y_n(inp: str) -> bool:
    if not inp == None:
        print(inp)
    res: str = input().strip().lower()
    if res == 'y' or res == 'j':
        return True
    return False


try:
    from cryptography.fernet import Fernet
except ModuleNotFoundError or ImportError:
    if y_n("Modul Cryptography nicht gefunden, soll es heruntergeladen werden? (Y/n)"):
        os.system("pip install cryptography")
        from cryptography.fernet import Fernet
    else:
        Console.print_colour("Beenden...", "red")
        nexit()

USER: str = input('User: ')[:32].strip()
CHATROOM: str = input('Chatraum: ')[:10].strip()
if CHATROOM == '':
    PATH: str = input('Pfad: ').strip()
else:
    PATH: str = f"Y:/2BHIT/test/{CHATROOM}.json"
KEY: str = getpass('Passwort: ').strip()
while KEY.lower() == CHATROOM.lower():
    Console.print_colour(
        "Passwort und Chatraum dürfen nicht gleich sein.", "red")
    KEY = getpass('Passwort: ').strip()


DATE: str = f'{str(datetime.now().day)}_{str(datetime.now().month)}'
WINDOWS: bool = True if platform.system() == 'Windows' else False
if WINDOWS:
    Console.print_colour("OS: Windows", "yellow")
else:
    Console.print_colour("OS: MacOS/Linux", "yellow")

global RUNNING
RUNNING: bool = True

class Chat:
    def __init__(self, path: str, key: str) -> None:
        self.path: str = path
        self.file: File = File(path)
        self.key: bytes = base64.urlsafe_b64encode(
            key.encode("utf-8").ljust(32)[:32])
        self.fernet: Fernet = Fernet(self.key)
        self.date: str = DATE
        self.nupdate: bool = False
        self.check_file()
        self.check_date()

    def check_date(self) -> None:
        data: dict = self.get_file()
        temp: list = []
        for day in data['days']:
            if day != self.date:
                temp.append(day)
        for day in temp:
            del data['days'][day]
        try:
            data['days'][self.date]
        except KeyError:
            data['days'][self.date] = []
        self.save_file(data)

    def check_file(self) -> None:
        def make_file(msg: str) -> None:
            if y_n(msg):
                os.makedirs(os.path.dirname(self.path), exist_ok=True)
                self.save_file({"days": {self.date: []}})
            else:
                nexit()

        if not File(self.path).exists():
            make_file(
                f"Datei '{self.path}' nicht gefunden, soll sie generiert werden? (Y/n)")

        try:
            self.get_chat()

        except json.JSONDecodeError:
            make_file(
                f"Datei '{self.path}' konnte nicht geladen werden, soll sie neu generiert werden? (Y/n)")

    def get_chat(self) -> dict:
        try:
            return self.get_file()['days'][self.date]
        except Exception as e:
            print("Fehler beim Laden: ", e)
            sleep(0.5)
            return self.get_chat()

    def append(self, msg: str, user: str) -> None:
        if self.cmd(msg):
            self.update()
            return
        temp: dict = self.get_file()
        temp['days'][self.date].append(
            str(self.encrypt(f"{user}: {msg}")))
        self.save_file(temp)

    def beatiful(self) -> str:
        temp: str = ''
        chat: dict = self.get_chat()
        for i in chat:
            temp2: str = self.decrypt(i)
            temp += f"\n{temp2}"
        try:
            if f'@{USER}' in self.decrypt(chat[-1]):
                try:
                    msgb = ctypes.windll.user32.MessageBoxW  # type: ignore
                    msgb(None, temp2, 'Ping', 0)
                except AttributeError:
                    pass
                self.append('OK', USER)
        except IndexError:
            pass
        if self.nupdate:
            temp += ' '
            self.nupdate = False
        return temp

    def encrypt(self, string: str) -> str:
        return str(self.fernet.encrypt(string.encode())).replace("b'", "").replace("'", "")

    def decrypt(self, string: str) -> str:
        try:
            return str(self.fernet.decrypt(string).decode())
        except:
            raise ValueError("Falscher Key")

    def delete(self, len: int) -> None:
        temp: dict = self.get_file()
        del temp['days'][self.date][-len:]
        self.save_file(temp)

    @staticmethod
    def convert(inp: str) -> str:
        output: str = ''
        for c in inp:
            output = c + output
        return output

    def update(self) -> None:
        self.nupdate = True

    def get_file(self) -> dict:
        return self.file.json_r()

    def save_file(self, data: dict) -> None:
        return self.file.json_w(data)

    def cmd(self, msg: str) -> bool:
        cmd: Cmd = Cmd(msg, "/")
        is_cmd: function = cmd.is_cmd
        if is_cmd('exit'):
            nexit()
        elif is_cmd('leave'):
            global RUNNING
            RUNNING = False
        elif is_cmd('del'):
            self.delete(1)
        elif is_cmd('del', 1):
            try:
                len: int = int(msg.split('/del ')[1])
                self.delete(len)
            except:
                pass
        elif is_cmd('check'):
            self.check_date()
        elif is_cmd('reset'):
            self.save_file({"days": {self.date: []}})
        if cmd.exec or 'gen' in self.convert(msg) or 'gin' in self.convert(msg):
            return True
        return False


class Cmd:
    def __init__(self, msg: str, prefix: str = '/') -> None:
        self.prefix: str = prefix
        self.msg: str = msg
        self.exec: bool = False

    def is_cmd(self, cmd: str, mode: int = 0) -> bool:
        temp: bool = self._is_cmd(cmd, mode)
        if temp:
            self.exec = True
        return temp

    def _is_cmd(self, cmd: str, mode: int = 0) -> bool:
        cmd = self.prefix + cmd
        if mode == 0:
            return self.msg == cmd
        elif mode == 1:
            return self.msg.startswith(cmd + ' ')
        return False


class KeyboardThread(threading.Thread):
    def __init__(self, chat: Chat, name: str = 'keyboard-input-thread') -> None:
        self.chat: Chat = chat
        super(KeyboardThread, self).__init__(name=name, daemon=True)
        self.start()

    def run(self) -> None:
        while True:
            self.callback(input())

    def callback(self, inp: str) -> None:
        if len(inp) > 10 and inp in pyperclip.paste() and '\n' in pyperclip.paste():
            self.chat.update()
            return
        if len(inp) > 128:
            inp = inp[:128] + '...'
        if len(inp) == 0:
            self.chat.update()
            return
        self.chat.append(inp, USER)


if 'ggen' in Chat.convert(USER) or 'ggin' in Chat.convert(USER):
    exit()


chat: Chat = Chat(PATH, KEY)
KeyboardThread(chat)


while RUNNING:
    Console.clear()
    prev: str = chat.beatiful()
    print(chat.beatiful() + '\n>>> ', end='')
    while chat.beatiful() == prev:
        sleep(0.5)


Console.clear()
os.system(f'python {os.path.abspath(__file__)}')
