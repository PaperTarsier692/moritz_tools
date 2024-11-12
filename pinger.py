from mt import ensure_venv, test_env, current_path, path
ensure_venv(__file__)

from papertools import File
from getpass import getuser
import os

PATH: str = path if not test_env else current_path
USER: str = getuser()

while True:
    inp: str = input('>>> @')
    user: str = inp.split(' ', 1)[0]
    msg: str = inp.split(' ', 1)[1]
    File(os.path.join(PATH, f'{USER}.{user}')).write(msg, True)
