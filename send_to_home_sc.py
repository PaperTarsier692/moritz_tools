from mt import ensure_venv, y_n
from sys import argv
ensure_venv(__file__, argv)

import os
from papertools import File, Webhook

path: str = argv[1]
print(path)

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

wh: Webhook = Webhook(settings['sth']['url'], settings['sth']['username'])

if os.path.isdir(path):
    zip_path: str = f"{path}.zip"
    if File(zip_path).exists():
        if y_n(f'Es gibt bereits eine Datei {zip_path}, soll sie überschrieben werden?'):
            os.remove(zip_path)
        else:
            exit()
    from shutil import make_archive
    print("Ordner erkannt, komprimiert Ordner...")
    try:
        make_archive(path,
                     'zip', path)
    except Exception as e:
        print(
            "Fehler beim komprimieren des Ordners, gibt es noch genug \
                Speicherplatz auf deinem Account?")
        print(e)
    wh.send_file(zip_path)
    os.remove(zip_path)


wh.send_file(path)
