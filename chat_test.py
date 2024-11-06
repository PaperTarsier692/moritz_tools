from mt import ensure_venv
ensure_venv(__file__)

from tkinter import Tk, Frame, Text, Event, PanedWindow, Button
from cryptography.fernet import Fernet
from papertools import Console, File
from mt import test_env, y_n
from getpass import getpass
from typing import Callable
import ctypes
import base64

import os


class Chat:
    def __init__(self, path: str, key: str) -> None:
        self.path: str = path
        self.file: File = File(path)
        self.fernet: Fernet = Fernet(base64.urlsafe_b64encode(
            key.encode("utf-8").ljust(32)[:32]))
        self.check_file()
        self.load_file()
        self.inp['members'].append(USER)
        self.save_file()

    def load_file(self) -> None:
        self.inp: dict = self.file.json_r()

    def save_file(self) -> None:
        self.file.json_w(self.inp)

    @staticmethod
    def nexit() -> None:
        Console.print_colour(
            "Drücken Sie enter um das Programm zu beenden.", "red")
        input()
        exit()

    def check_file(self) -> None:
        def make_file(msg: str) -> None:
            if y_n(msg):
                os.makedirs(os.path.dirname(self.path), exist_ok=True)
                self.file.json_w({"msgs": [], "members": []})
            else:
                self.nexit()

        if not File(self.path).exists():
            make_file(
                f"Datei '{self.path}' nicht gefunden, soll sie generiert werden? (Y/n)")

        try:
            self.load_file()
            self.inp['msgs']
            self.inp['members']
        except:
            make_file(
                f"Datei '{self.path}' konnte nicht geladen werden, soll sie neu generiert werden? (Y/n)")

    def append(self, msg: str) -> None:
        if self.cmd(msg):
            print('CMD')
            return
        self.inp['msgs'].append(self.encrypt(f"{USER}: {msg}"))

    def chat_to_list(self) -> tuple[list[str], list[str]]:
        out: list[str] = []
        for i in self.inp['msgs']:
            out.append(self.decrypt(i))
        try:
            if f'@{USER}' in out[-1]:
                try:
                    msgb = ctypes.windll.user32.MessageBoxW  # type: ignore
                    msgb(None, out[-1], 'Ping', 0)
                except AttributeError:
                    pass
                self.append('OK')
        except IndexError:
            pass
        return out, self.inp['members']

    def encrypt(self, string: str) -> str:
        return str(self.fernet.encrypt(string.encode())).replace("b'", "")\
            .replace("'", "")

    def decrypt(self, string: str) -> str:
        try:
            return str(self.fernet.decrypt(string).decode())
        except ValueError:
            raise ValueError("Falscher Key")

    def delete(self, len: int) -> None:
        del self.inp['msgs'][-len:]

    @staticmethod
    def convert(inp: str) -> str:
        output: str = ''
        for c in inp:
            output = c + output
        return output

    def cmd(self, msg: str) -> bool:
        cmd: Cmd = Cmd(msg, "/")
        is_cmd: Callable = cmd.is_cmd
        if is_cmd('exit'):
            self.nexit()
        elif is_cmd('del'):
            self.delete(1)
        elif is_cmd('del', 1):
            try:
                len: int = int(msg.split('/del ', 1)[1])
                self.delete(len)
            except IndexError or ValueError:
                pass
        elif is_cmd('reset'):
            self.inp = {"msgs": [], "members": []}
        if cmd.exec or 'gen' in self.convert(msg).lower() \
                or 'gin' in self.convert(msg).lower():
            return True
        return False


class GUI:
    def __init__(self, root: Tk, chat: Chat) -> None:
        self.messages: list[str] = []

        self.root: Tk = root
        self.chat: Chat = chat

        self.root.title("Chat Test")

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

        self.right_tab: Text = Text(
            self.right_frame, height=1, state='disabled')
        self.right_tab.pack(side='top', fill='both', expand=True)

        self.button_frame: Frame = Frame(self.right_frame)
        self.button_frame.pack(side='bottom', fill='x')

        self.button1: Button = Button(self.button_frame, text="Button 1")
        self.button1.pack(side='left', fill='x', expand=True)

        self.button2: Button = Button(self.button_frame, text="Button 2")
        self.button2.pack(side='left', fill='x', expand=True)

        self.add_colours()
        self.update()

    def add_messages(self, messages: list[str]) -> None:
        self.chat_widget.config(state='normal')
        self.chat_widget.delete("1.0", "end")
        for msg in messages:
            if any(colour in msg for colour in colours):
                colour_list: list[str] = [
                    colour for colour in colours if colour in msg]
                indexes: list[int] = []
                for colour in colour_list:
                    indexes.append(msg.index(colour))
                indexes.append(len(msg))
                self.chat_widget.insert("end", msg[:indexes[0]])
                for i, colour in enumerate(colour_list):
                    self.chat_widget.insert(
                        "end", msg[msg.index(colour) + len(colour):indexes[i + 1]], colour)
            else:
                self.chat_widget.insert("end", msg)
            self.chat_widget.insert("end", '\n')
        self.chat_widget.config(state='disabled')
        self.chat_widget.see("end")

    def add_members(self, members: list[str]) -> None:
        self.right_tab.config(state='normal')
        self.right_tab.delete("1.0", "end")
        msg: str = '\n'.join(members)
        self.right_tab.insert("end", msg)
        self.right_tab.config(state='disabled')

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
            if '\n' in content:
                return
            self.messages.append(content)
        inner()
        self.chat_input.delete("1.0", "end")

    def update(self) -> None:
        self.chat.load_file()
        before: dict = self.chat.inp.copy()
        for msg in self.messages:
            self.chat.append(msg)
        msgs, members = self.chat.chat_to_list()
        self.add_messages(msgs)
        self.add_members(members)
        if self.chat.inp != before:
            print('Changes')
            self.chat.save_file()
        self.root.after(1000, self.update)

    def add_colours(self) -> None:
        self.chat_widget.tag_config('//red//', foreground='red')
        self.chat_widget.tag_config('//green//', foreground='green')
        self.chat_widget.tag_config('//blue//', foreground='blue')
        self.chat_widget.tag_config('//yellow//', foreground='yellow')
        self.chat_widget.tag_config('//purple//', foreground='purple')
        self.chat_widget.tag_config('//cyan//', foreground='cyan')
        self.chat_widget.tag_config('//black//', foreground='black')
        self.chat_widget.tag_config('//white//', foreground='white')
        self.chat_widget.tag_config('//bblack//', background='black')
        self.chat_widget.tag_config('//bred//', background='red')
        self.chat_widget.tag_config('//bgreen//', background='green')
        self.chat_widget.tag_config('//bblue//', background='blue')
        self.chat_widget.tag_config('//byellow//', background='yellow')
        self.chat_widget.tag_config('//bpurple//', background='purple')
        self.chat_widget.tag_config('//bcyan//', background='cyan')
        self.chat_widget.tag_config('//bwhite//', background='white')
        self.chat_widget.tag_config('**', font='bold')
        self.chat_widget.tag_config('*', font='italic')
        self.chat_widget.tag_config('__', underline=True)
        self.chat_widget.tag_config('//reset//', font='normal')


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


colours: list[str] = ['//reset//', '#', '*', '__', '//black//', '//blue//', '//cyan//', '//green//', '//purple//', '//red//',
                      '//white//', '//yellow//', '//bblack//', '//bred//', '//bgreen//', '//byellow//', '//bblue', '//bpurple//', '//bcyan//', '//bwhite//']


USER: str = input('User: ')[:32].strip()
CHATROOM: str = input('Chatraum: ')[:10].strip()
if CHATROOM == '':
    if not test_env:
        PATH: str = input('Pfad: ').strip()
    else:
        PATH: str = os.path.abspath(os.path.join(
            __file__, os.pardir, 'chat_test.json'))
else:
    PATH: str = f"Y:/2BHIT/test/{CHATROOM}.json"

KEY: str = getpass('Passwort: ').strip()
while KEY.lower() == CHATROOM.lower():
    Console.print_colour(
        "Passwort und Chatraum dürfen nicht gleich sein.", "red")
    KEY = getpass('Passwort: ').strip()


WINDOWS: bool = os.name == 'nt'
if WINDOWS:
    Console.print_colour("OS: Windows", "yellow")
else:
    Console.print_colour("OS: MacOS/Linux", "yellow")


chat: Chat = Chat(PATH, KEY)
root: Tk = Tk()
app: GUI = GUI(root, chat)
root.mainloop()

print('ENDE')
_inp: dict = File(PATH).json_r()
_inp['members'].remove(USER)
File(PATH).json_w(_inp)
