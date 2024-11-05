from mt import ensure_venv
from sys import argv
ensure_venv(__file__, argv)

from papertools import File


print(argv)

input()
File('Z:\\Documents\\moritz_tools\\ausgefuert').write('Ausgeführt', True)
