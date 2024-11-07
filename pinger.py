from mt import ensure_venv
ensure_venv(__file__)

from papertools import File
from getpass import getuser
import os

PATH: str = 'Y:/2BHIT/test/'
USER: str = getuser()

while True:
    inp: str = input('>>> @')
    user: str = inp.split(' ', 1)[0]
    msg: str = inp.split(' ', 1)[1]
    File(os.path.join(PATH, f'{USER}.{user}')).write(msg, True)
