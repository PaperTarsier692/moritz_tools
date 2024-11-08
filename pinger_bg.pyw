from mt import ensure_venv
ensure_venv(__file__)

from papertools import File, Dir
from getpass import getuser
from time import sleep
import ctypes
import os

PATH: str = 'Y:/2BHIT/test/'
USER: str = getuser()

while True:
    for file in Dir.listfiles(PATH):
        file = os.path.join(PATH, file)
        if os.path.basename(file).endswith(USER):
            content: str = File(file).read()
            msgb = ctypes.windll.user32.MessageBoxW  # type: ignore
            msgb(None, content, 'Pinger', 0)
            os.remove(file)
        sleep(5)
