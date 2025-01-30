from mt import ensure_venv, fix_res
ensure_venv(__file__)

from ttkthemes import ThemedTk
from tkinter.ttk import Notebook, Frame, Button
from tkinter import Text

fix_res()


class TTT:
    def __init__(self) -> None:
        self.root: ThemedTk = ThemedTk()
        self.rows: int = 4
        self.cols: int = 3
        self.generate_gui()
        self.root.geometry('800x800')
        self.root.mainloop()

    def generate_gui(self) -> None:
        for y in range(self.rows):
            for x in range(self.cols):
                button = Button(
                    self.root, text=f'{x} | {y}', command=lambda x=x, y=y: self.button_callback(x, y))
                button.grid(row=y * 2, column=x * 2, rowspan=2,
                            columnspan=2, sticky='nsew')
                self.root.grid_rowconfigure(y * 2, weight=1)
                self.root.grid_columnconfigure(x * 2, weight=1)

    def button_callback(self, x: int, y: int) -> None:
        print(f'Button {x} | {y} pressed')


TTT()
