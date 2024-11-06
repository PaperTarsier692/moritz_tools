from mt import ensure_venv
from sys import argv
ensure_venv(__file__, argv)

from papertools import File, Webhook

path: str = argv[1]
print(path)

if not File('settings.json').exists():
    print('settings.json nicht gefunden, erstelle sie und führ das Programm erneut aus.')
    input()
    exit()

settings: dict = File('settings.json').json_r()

wh: Webhook = Webhook(settings['url'], settings['username'])

wh.send_file(path)
