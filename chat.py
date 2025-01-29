from mt import ensure_venv, y_n, popup, generate_random_string, deprecated, check_str, Config, path
ensure_venv(__file__)
deprecated(__name__)

from tkinter.ttk import Frame, PanedWindow, Button, Label
from ttkthemes import ThemedStyle
from tkinter import Text
from cryptography.fernet import Fernet
from papertools import Console, File
from typing import Callable, Literal
from inspect import signature
import base64
import os


class Chat:
    def __init__(self, path: str, key: str, user: str, gui) -> None:
        self.user: str = user
        self.path: str = path
        self.file: File = File(path)
        self.fernet: Fernet = Fernet(base64.urlsafe_b64encode(
            key.encode("utf-8").ljust(32)[:32]))
        self.check_file()
        self.load_file()
        self.save_file()
        self.pre_cmd()
        self.gui = gui

    def load_file(self) -> None:
        try:
            self.inp: dict = self.file.json_r()
        except Exception as e:
            Console.print_colour(f'Fehler {e}', 'red')
            if not self.file.exists():
                Console.print_colour(f'Stellt Datei wieder her', 'red')
                self.save_file()

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
        self.inp['msgs'].append(self.encrypt(f"{self.user}: {msg}"))

    def check_members(self, members: list[str]) -> bool:
        seen: set = set()
        new_members: list[str] = []
        changes: bool = False
        for enc in self.inp['members']:
            if enc not in seen:
                seen.add(enc)
                new_members.append(enc)

        if len(new_members) != len(self.inp['members']):
            self.inp['members'] = new_members
            changes = True

        if self.user not in members:
            self.inp['members'].append(self.encrypt(self.user))
            changes = True

        return changes

    def get_msgs(self) -> list[str]:
        return [self.decrypt(msg) for msg in self.inp['msgs']]

    def get_members(self) -> list[str]:
        return [self.decrypt(member) for member in self.inp['members']]

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

    def pre_cmd(self) -> None:
        self.cmds: dict = {}
        self.theme: int = -1

        def _cmd(name: str = '', display: str = '', arguments: Literal['optional', 'required'] = 'required') -> Callable:
            def inner(func: Callable) -> Callable:
                cmd_name = name or func.__name__
                display_name = display or cmd_name
                if len(signature(func).parameters) > 0:
                    self.cmds[cmd_name] = {
                        'func': func, 'args': True, 'name': display_name, 'arguments': arguments}
                else:
                    self.cmds[cmd_name] = {
                        'func': func, 'args': False, 'name': display_name, 'arguments': 'optional'}
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

        @_cmd(display='del [int]', name='del', arguments='optional')
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

        @_cmd()
        def ttt() -> None:
            msg: str = f'[ttt]{generate_random_string(6)}'
            self.append(msg)

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
            if cmd['arguments'] == 'required' and cmd_args == []:
                Console.print_colour('Zu wenig Argumente angegeben', 'red')
                return True
            cmd['func'](cmd_args)
        else:
            cmd['func']()
        return True

    def close(self) -> None:
        print('ENDE')
        self.load_file()
        members_enc: list[str] = self.inp['members']
        for member_enc in members_enc:
            if self.decrypt(member_enc) == self.user:
                members_enc.remove(member_enc)
                break
        self.save_file()


class GUI:
    def __init__(self, root: Frame) -> None:
        self.messages: list[str] = []
        self.root: Frame = root

        self.paned_window: PanedWindow = PanedWindow(
            self.root, orient='horizontal')

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

        self.chat_widget.tag_configure(
            "link", underline=True, foreground='blue')

        self.chat_widget.tag_bind("hyperlink", "<Button-1>", self.ttt_request)

    def login(self, values: tuple[str, str, str]) -> None:
        self.chat: Chat = Chat(values[2], values[1], values[0], self)
        self.user: str = values[0]
        self.update()
        self.add_cmds()
        self.add_colours()

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

    def ttt_request(self, event) -> None:
        print('TTT Request')
        pass

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
            elif '[ttt]' in msg:
                self.chat_widget.insert("end", 'TTT Request', "hyperlink")
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
            if not check_str(content, silent=True):
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
            members.append(self.user)
            changes = True

        try:
            if f'@{self.user}' in msgs[-1]:
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


class InputGUI:
    def __init__(self, root: Frame, chat: GUI, style: ThemedStyle) -> None:
        self.root = root
        self.user_label: Label = Label(self.root, text="User:")
        self.user_label.pack(anchor='center', pady=2)
        self.user_text: Text = Text(self.root, height=1, width=20)
        self.user_text.pack(anchor='center', pady=2)

        self.pswd_label: Label = Label(self.root, text="Password:")
        self.pswd_label.pack(anchor='center', pady=2)
        self.pswd_text: Text = Text(self.root, height=1, width=20)
        self.pswd_text.pack(anchor='center', pady=2)

        self.chat_label: Label = Label(self.root, text="Chatroom:")
        self.chat_label.pack(anchor='center', pady=2)
        self.chat_text: Text = Text(self.root, height=1, width=20)
        self.chat_text.pack(anchor='center', pady=2)
        self.confirm: Button = Button(
            self.root, command=self.confirm_callback, text='Confirm')
        self.confirm.pack(anchor='center', pady=2)
        self.chat: GUI = chat
        self.style: ThemedStyle = style
        for text in self.root.winfo_children():
            if isinstance(text, Text):
                text.bind("<Tab>", self.focus_next_widget)
                text.bind("<Return>", self.confirm_callback)

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def check_values(self, values: tuple[str, str, str]) -> bool:
        global out
        user, key, path = values
        out = True
        bg_color = self.style.lookup('TFrame', 'background') or '#000'
        self.user_text.config(bg=bg_color)
        self.pswd_text.config(bg=bg_color)
        self.chat_text.config(bg=bg_color)

        def mark_wrong(**kwargs) -> None:
            print(f'Mark wrong: {kwargs}')
            global out
            out = False
            kwargs['mark'].config(bg='#800')  # type: ignore

        if not check_str(user, 3, 12, False, allow_empty=True):
            mark_wrong(mark=self.user_text)
        else:
            self.user_text.delete('1.0', 'end')
            self.user_text.insert('1.0', Config().smart_get(user, 'chat/user',
                                                            error_callback=mark_wrong, mark=self.user_text))
        if not check_str(key, 4, 20, False):
            mark_wrong(mark=self.pswd_text)
        if not check_str(path, 2):
            mark_wrong(mark=self.chat_text)
        return out

    def confirm_callback(self, event=None) -> None:
        print('MHM')
        if not self.check_values(self.get_values()):
            print('Falscher Input')
            return
        for child in self.root.winfo_children():
            child.pack_forget()
        self.root.pack_forget()
        self.chat.paned_window.pack(fill='both', expand=True)
        self.chat.login(self.get_values())

    def get_values(self) -> tuple[str, str, str]:
        chat: str = self.chat_text.get('1.0', 'end-1c').strip()
        if not chat.endswith('.json'):
            chat = f'{path}/c_{chat}.json'
        return self.user_text.get('1.0', 'end-1c').strip(), self.pswd_text.get('1.0', 'end-1c').strip(), chat


only_colours: list[str] = ['black', 'blue', 'cyan',
                           'green', 'purple', 'red', 'white', 'yellow']

colours: list[str] = ['//reset//', '__']
colours.extend([f'//{colour}//' for colour in only_colours])
colours.extend([f'//b{colour}//' for colour in only_colours])
