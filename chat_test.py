from mt import ensure_venv, test_env, y_n, better_input, better_getpass, windows, current_path, popup, fix_res
ensure_venv(__file__)

from tkinter.ttk import Frame, PanedWindow, Button
from ttkthemes import ThemedTk, ThemedStyle
from tkinter import Text
from papertools import Console, File, Dir
from cryptography.fernet import Fernet
from inspect import signature
from typing import Callable
import base64
import os

from mt import path

fix_res()


class Chat:
    def __init__(self, path: str, key: str) -> None:
        self.path: str = path
        self.file: File = File(path)
        self.fernet: Fernet = Fernet(base64.urlsafe_b64encode(
            key.encode("utf-8").ljust(32)[:32]))
        self.check_file()
        self.load_file()
        self.save_file()
        self.pre_cmd()

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
            return
        self.inp['msgs'].append(self.encrypt(f"{USER}: {msg}"))

    def check_members(self, members: list[str]) -> bool:
        if USER not in self.get_members():
            self.inp['members'].append(self.encrypt(USER))
            return True
        return False

    def get_msgs(self) -> list[str]:
        msgs: list[str] = []
        for msg in self.inp['msgs']:
            msgs.append(self.decrypt(msg))
        return msgs

    def get_members(self) -> list[str]:
        members: list[str] = []
        for member in self.inp['members']:
            members.append(self.decrypt(member))
        return members

    def encrypt(self, string: str) -> str:
        return str(self.fernet.encrypt(string.encode())).replace("b'", "")\
            .replace("'", "")

    def decrypt(self, string: str) -> str:
        try:
            return str(self.fernet.decrypt(string).decode())
        except ValueError:
            raise ValueError("Falscher Key")

    def delete(self, length: int) -> None:
        del self.inp['msgs'][-length:]

    @staticmethod
    def convert(inp: str) -> str:
        output: str = ''
        for c in inp:
            output = c + output
        return output

    def pre_cmd(self) -> None:
        self.cmds: dict = {}
        self.theme: int = -1

        def _cmd(name: str = '', display: str = '') -> Callable:
            def inner(func: Callable) -> Callable:
                cmd_name = name or func.__name__
                display_name = display or cmd_name
                self.cmds[cmd_name] = {
                    'func': func, 'args': len(signature(func).parameters) > 0, 'name': display_name}
                return func
            return inner

        @_cmd(display='help <str>')
        def help(*args) -> None:
            '''Zeigt Informationen zu einen Befehl an
            Argumente:
            <str>: Befehl (benötigt)'''
            cmd_name: str = args[0][0]
            if cmd_name not in self.cmds.keys():
                Console.print_colour(
                    f'Help: Command {cmd_name} nicht gefunden', 'red')
                return
            cmd: dict = self.cmds[cmd_name]
            Console.print_colour(
                f'Command /{cmd_name}:\n{cmd["func"].__doc__}', 'green')

        @_cmd(name='exit')
        def _exit() -> None:
            '''Beendet das Programm'''
            exit()

        @_cmd()
        def reset() -> None:
            '''Setzt alle Nachrichten und die Mitgliederliste zurück'''
            self.inp = {"msgs": [], "members": []}

        @_cmd()
        def reset_names() -> None:
            '''Setzt die Mitgliederliste zurück'''
            self.inp = {"msgs": self.inp['msgs'], "members": []}

        @_cmd()
        def theme_cycle() -> None:
            '''Wechselt zum nächsten Theme'''
            self.theme = gui.themes.index(gui.theme)
            self.theme += 1
            self.theme %= len(gui.themes)
            theme: str = gui.themes[self.theme]
            Console.print_colour(
                f'Applying Theme {theme} {self.theme + 1}/{len(gui.themes)}', 'yellow')
            gui.apply_theme(theme)

        @_cmd(display='theme <str>')
        def theme(*args) -> None:
            '''Wechselt zum angegebenen Theme
            Argumente:
            <str>: theme (benötigt)'''
            theme: str = args[0][0]
            if theme in gui.themes:
                Console.print_colour(f'Applying Theme {theme}', 'yellow')
                gui.apply_theme(theme)
            else:
                Console.print_colour(f'Theme {theme} not found', 'red')

        @_cmd()
        def save_theme() -> None:
            '''Speichert das aktuelle Theme als Einstellung'''
            cfg: File = File('config.json')
            inp: dict = cfg.json_r()
            inp['chat']['theme'] = gui.theme
            Console.print_colour(f'Theme {gui.theme} saved', 'green')
            cfg.json_w(inp)

        @_cmd(display='del [int]', name='del')
        def rem(*args) -> None:
            '''Löscht 1 / die angegebene Anzahl an Nachrichten
            Argumente:
            [int]: Anzahl (optional)
            '''
            try:
                if args[0] == []:
                    length: int = 1
                else:
                    length: int = int(args[0][0])
                self.delete(length)
            except:
                pass

    def cmd(self, msg: str) -> bool:
        msg = msg.strip().lower()
        if not msg.startswith('/'):
            return False

        cmd_name: str = msg.split(' ')[0].replace('/', '', 1)
        if self.cmds.get(cmd_name) is None:
            return False
        cmd: dict = self.cmds[cmd_name]
        cmd_args: list[str] = msg.split(' ')[1:] or []
        if cmd['args']:
            cmd['func'](cmd_args)
        else:
            cmd['func']()
        return True


class GUI:
    def __init__(self, root: ThemedTk, chat: Chat) -> None:
        self.messages: list[str] = []
        self.root: ThemedTk = root
        self.chat: Chat = chat
        self.themes: list[str] = self.root.get_themes()

        self.style: ThemedStyle = ThemedStyle()

        self.root.title("Chat Test")

        self.paned_window: PanedWindow = PanedWindow(
            self.root, orient='horizontal')
        self.paned_window.pack(fill='both', expand=True)

        self.left_frame: Frame = Frame(self.paned_window)
        self.paned_window.add(self.left_frame)

        self.right_frame: Frame = Frame(self.paned_window, width=100)
        self.paned_window.add(self.right_frame)

        self.chat_widget: Text = Text(
            self.left_frame, state='disabled')
        self.chat_widget.pack(side='top', fill='both', expand=True)

        self.chat_input: Text = Text(
            self.left_frame, height=1)
        self.chat_input.pack(side='bottom', fill='x', expand=False)
        self.chat_input.bind("<Return>", self.on_enter)

        self.right_tab: Text = Text(
            self.right_frame, height=1, state='disabled')
        self.right_tab.pack(side='top', fill='both', expand=True)

        self.button_frame: Frame = Frame(self.right_frame)
        self.button_frame.pack(side='bottom', fill='x')

        self.cmds_open: bool = False
        self.button1: Button = Button(
            self.button_frame, text="Commands", command=self.toggle_cmds)
        self.button1.pack(side='left', fill='x', expand=True)

        self.button2: Button = Button(self.button_frame, text="Textstil")
        self.button2.pack(side='left', fill='x', expand=True)

        self.apply_theme(stgs['theme'])
        self.add_cmds()
        self.add_colours()
        self.update()

    def apply_theme(self, theme: str) -> None:
        self.theme: str = theme
        self.root.title(f'Chat Test: {CHATROOM} - {theme.capitalize()}')
        self.root.set_theme(theme)
        self.style.theme_use(theme)
        bg_color = self.style.lookup('TFrame', 'background') or '#000'
        fg_color = self.style.lookup('TLabel', 'foreground') or '#FFF'
        self.chat_widget.config(bg=bg_color, fg=fg_color)
        self.chat_input.config(bg=bg_color, fg=fg_color)
        self.right_tab.config(bg=bg_color, fg=fg_color)

    def write_cmd(self, cmd: str, args: bool) -> None:
        self.chat_input.delete("1.0", "end")
        self.chat_input.insert("end", f'/{cmd} ')
        if not args:
            self.on_enter()
        self.chat_input.focus()

    def add_cmds(self) -> None:
        self.cmds: list[Button] = []
        for name, values in self.chat.cmds.items():
            self.cmds.append(
                Button(self.button_frame, text=values['name'], command=lambda n=name, a=values['args']: self.write_cmd(n, a)))

    def toggle_cmds(self) -> None:
        if self.cmds_open:
            for cmd in self.cmds:
                cmd.pack_forget()
            self.cmds_open = False
            return
        else:
            for cmd in self.cmds:
                cmd.pack(side='top', fill='x', expand=True)
            self.cmds_open = True

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
                indexes.sort()
                self.chat_widget.insert("end", msg[:indexes[0]])
                colour_list.sort(key=msg.index)
                for i, colour in enumerate(colour_list):
                    self.chat_widget.insert(
                        "end", msg[msg.index(colour) + len(colour): indexes[i + 1]], colour)
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

    def on_enter(self, event=None) -> None:
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
        changes: bool = False
        self.chat.load_file()
        for msg in self.messages:
            changes = True
            self.chat.append(msg)
        self.messages = []
        msgs: list[str] = self.chat.get_msgs()
        members: list[str] = self.chat.get_members()
        if self.chat.check_members(members):
            members.append(USER)
            changes = True

        try:
            if f'@{USER}' in msgs[-1]:
                popup('Ping', msgs[-1])
                self.chat.append('OK')
                changes = True
        except IndexError:
            pass
        self.add_messages(msgs)
        self.add_members(members)

        if changes:
            self.chat.save_file()

        self.root.after(1000, self.update)

    def add_colours(self) -> None:
        for colour in only_colours:
            self.chat_widget.tag_config(f'//{colour}//', foreground=colour)
            self.chat_widget.tag_config(f'//b{colour}//', background=colour)
        self.chat_widget.tag_config('__', underline=True)
        self.chat_widget.tag_config('//reset//', font='normal')


only_colours: list[str] = ['black', 'blue', 'cyan',
                           'green', 'purple', 'red', 'white', 'yellow']

colours: list[str] = ['//reset//', '__']
colours.extend([f'//{colour}//' for colour in only_colours])
colours.extend([f'//b{colour}//' for colour in only_colours])
global USER, stgs


def generate_config() -> None:
    global USER, stgs
    print('config.json wurde erstellt')
    inp: dict = stgs_file.json_r()
    USER = better_input('User: ', 2, 10, False)
    inp['chat'] = {"user": USER, "theme": "equilux"}
    stgs = inp['chat']
    stgs_file.json_w(inp)


stgs_file: File = File('config.json')
if stgs_file.exists():
    try:
        stgs: dict = stgs_file.json_r()['chat']
        theme: str = stgs['theme']
        USER = better_input('User (Enter für Standard): ', 2, 10, False,
                            allow_empty=True) or stgs['user']
    except:
        generate_config()
else:
    stgs_file.json_w({})
    generate_config()

if not test_env:
    print(
        f'Verfügbare Chaträume: {", ".join(file.removeprefix("c_").removesuffix(".json") for file in Dir.listfiles(path, False) if file.startswith("c_"))}')
CHATROOM = better_input('Chatraum: ', 3, 10, False, allow_empty=True)
if CHATROOM == '':
    if test_env:
        PATH: str = os.path.join(current_path, 'c_chat_test.json')
    else:
        PATH: str = better_input('Pfad: ')
else:
    PATH: str = f"{path}/c_{CHATROOM}.json"

KEY: str = better_getpass('Passwort: ', 5, 32, False)
while KEY.lower() == CHATROOM.lower():
    Console.print_colour(
        "Passwort und Chatraum dürfen nicht gleich sein.", "red")
    KEY = better_getpass('Passwort: ', 5, 32, False)


if windows:
    Console.print_colour("OS: Windows", "yellow")
else:
    Console.print_colour("OS: MacOS/Linux", "yellow")


chat: Chat = Chat(PATH, KEY)
root: ThemedTk = ThemedTk()
gui: GUI = GUI(root, chat)
root.mainloop()

print('ENDE')
# _inp: dict = File(PATH).json_r()
# _inp['members'].remove(chat)
# File(PATH).json_w(_inp)
