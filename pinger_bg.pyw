from mt import ensure_venv, test_env, current_path, popup, path
ensure_venv(__file__)

from papertools import File, Dir
from getpass import getuser
from time import sleep
import os

PATH: str = path if not test_env else current_path
USER: str = getuser()

while True:
    for file in Dir.listfiles(PATH):
        file = os.path.join(PATH, file)
        if os.path.basename(file).endswith(USER):
            content: str = File(file).read()
            popup('Pinger', content)
            os.remove(file)
    sleep(5)
