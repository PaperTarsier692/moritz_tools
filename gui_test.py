from tkinter import Tk, Frame, Text, Event, PanedWindow, Button
from cryptography.fernet import Fernet
from papertools import Console, File
from datetime import datetime
from getpass import getpass
from typing import Callable
from time import sleep
import pyperclip
import ctypes
import base64
import json
import os


class GUI:
    def __init__(self, root: Tk) -> None:
        self.root: Tk = root
        self.root.title("Chat")

        self.paned_window: PanedWindow = PanedWindow(
            self.root, orient='horizontal')
        self.paned_window.pack(fill='both', expand=True)

        self.left_frame: Frame = Frame(self.paned_window)
        self.paned_window.add(self.left_frame)

        self.right_frame: Frame = Frame(self.paned_window, width=100)
        self.paned_window.add(self.right_frame)

        self.chat_widget: Text = Text(self.left_frame, state='disabled')
        self.chat_widget.pack(side='top', fill='both', expand=True)

        self.chat_input: Text = Text(self.left_frame, height=1)
        self.chat_input.pack(side='bottom', fill='x', expand=False)
        self.chat_input.bind("<Return>", self.on_enter)

        self.right_tab: Text = Text(self.right_frame, height=1)
        self.right_tab.pack(side='top', fill='both', expand=True)

        self.button_frame: Frame = Frame(self.right_frame)
        self.button_frame.pack(side='bottom', fill='x')

        self.button1: Button = Button(self.button_frame, text="Button 1")
        self.button1.pack(side='left', fill='x', expand=True)

        self.button2: Button = Button(self.button_frame, text="Button 2")
        self.button2.pack(side='left', fill='x', expand=True)

    def clear_input(self) -> None:
        self.chat_input.delete("1.0", "end")

    def add_messages(self, messages: list[str]) -> None:
        self.chat_widget.config(state='normal')
        for msg in messages:
            self.chat_widget.insert("end", msg)
        self.chat_widget.config(state='disabled')

    def on_enter(self, event: Event) -> None:
        def inner() -> None:
            content: str = self.chat_input.get("1.0", "end-1c").strip()
            if len(content) > 128:
                content = content[:128] + '...'
            if Chat.convert('gen') in content.lower() or Chat.convert('gin')\
                    in content.lower():
                return
            if len(content) == 0:
                return
            if len(content) > 10 and content in pyperclip.paste() \
                    and '\n' in pyperclip.paste():
                return
        inner()
        self.chat_input.delete("1.0", "end")


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


colours: dict = {
    # Specials
    "//reset//": "\033[0m",
    "\\**": "\033[22m",
    "**": "\033[1m",
    "\\*": "\033[23m",
    "*": "\033[3m",
    "\\__": "\033[24m",
    "__": "\033[4m",
    # Text Colours
    "//black//": "\033[30m",
    "//blue//": "\033[34m",
    "//cyan//": "\033[36m",
    "//green//": "\033[32m",
    "//purple//": "\033[35m",
    "//red//": "\033[31m",
    "//white//": "\033[37m",
    "//yellow//": "\033[33m",
    # Bg Colours
    "//bblack//": "\033[40m",
    "//bred//": "\033[41m",
    "//bgreen//": "\033[42m",
    "//byellow//": "\033[43m",
    "//bblue": "\033[44m",
    "//bpurple//": "\033[45m",
    "//bcyan//": "\033[46m",
    "//bwhite//": "\033[47m"
}


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
WINDOWS: bool = os.name == 'nt'
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
        self.fernet: Fernet = Fernet(base64.urlsafe_b64encode(
            key.encode("utf-8").ljust(32)[:32]))
        self.date: str = DATE
        self.nupdate: bool = False
        self.check_file()
        self.check_date()

    @staticmethod
    def s_print_colour(inp: str) -> str:
        for colour, value in colours.items():
            inp = inp.replace(colour, value)
        inp += '\033[0m'
        return inp

    @staticmethod
    def nexit() -> None:
        Console.print_colour(
            "Drücken Sie enter um das Programm zu beenden.", "red")
        input()
        exit()

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
            def y_n(inp: str) -> bool:
                if inp is not None:
                    print(inp)
                res: str = input().strip().lower()
                if res == 'y' or res == 'j':
                    return True
                return False

            if y_n(msg):
                os.makedirs(os.path.dirname(self.path), exist_ok=True)
                self.save_file({"days": {self.date: []}})
            else:
                self.nexit()

        if not File(self.path).exists():
            make_file(
                f"Datei '{self.path}' nicht gefunden,\
                      soll sie generiert werden? (Y/n)")

        try:
            self.get_chat()

        except json.JSONDecodeError:
            make_file(
                f"Datei '{self.path}' konnte nicht geladen werden, \
                    soll sie neu generiert werden? (Y/n)")

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
            temp2: str = self.s_print_colour(self.decrypt(i))
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
        return str(self.fernet.encrypt(string.encode())).replace("b'", "")\
            .replace("'", "")

    def decrypt(self, string: str) -> str:
        try:
            return str(self.fernet.decrypt(string).decode())
        except ValueError:
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
        is_cmd: Callable = cmd.is_cmd
        if is_cmd('exit'):
            self.nexit()
        elif is_cmd('leave'):
            global RUNNING
            RUNNING = False
        elif is_cmd('del'):
            self.delete(1)
        elif is_cmd('del', 1):
            try:
                len: int = int(msg.split('/del ', 1)[1])
                self.delete(len)
            except IndexError or ValueError:
                pass
        elif is_cmd('check'):
            self.check_date()
        elif is_cmd('reset'):
            self.save_file({"days": {self.date: []}})
        if cmd.exec or 'gen' in self.convert(msg).lower() \
                or 'gin' in self.convert(msg).lower():
            return True
        return False


root: Tk = Tk()
app: GUI = GUI(root)
root.mainloop()


# Restart
Console.clear()
if WINDOWS:
    os.system(f'start python {os.path.abspath(__file__)}')
