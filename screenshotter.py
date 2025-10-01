from mt import ensure_venv
ensure_venv(__file__)

from papertools import Console, Dir, Webhook, File
from time import sleep

if not File('config.json').exists():
    print('config.json nicht gefunden, erstelle sie und führ das Programm erneut aus.')
    input()
    exit()

settings: dict = File('config.json').json_r()
try:
    settings['sth']['url']
    settings['sth']['username']
except:
    print('Fehler beim Laden der Werte, sind diese angegeben? Führe send_to_home.py aus um diese auszufüllen.')
    input()
    exit()

wh: Webhook = Webhook(settings['sth']['url'], settings['sth']['username'])

PATH: str = "Z:/Pictures/Screenshots/"

prev: list[str] = []
new: list[str] = []

while True:
    new = Dir.listfiles(PATH, False, True)
    for file in prev:
        if file in new:
            new.remove(file)
    for file in new:
        Console.print_colour(f'Sending "{file}"', 'green')
        wh.send_file(file)
    prev = new.copy()
    sleep(10)
