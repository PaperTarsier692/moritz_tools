from mt import ensure_venv
ensure_venv(__file__)

from papertools import Console, Dir
import os

if os.path.exists('Z:/Documents/moritz_tools/win11debloat'):
    Console.print_colour(
        'Win11Debloat gefunden, holt neueste Version ', 'green', end='')
    os.system('Z: && cd Z:/Documents/moritz_tools/win11debloat && git pull')
else:
    Console.print_colour('Lädt Win11Debloat herunter... ', 'green', end='')
    os.system(
        'Z: && cd Z:/Documents/moritz_tools && git clone https://github.com/Raphire/Win11Debloat.git win11debloat')

for file in Dir.listfiles('Z:/Documents/moritz_tools/win11debloat/Regfiles/', abspath=True):
    pass
