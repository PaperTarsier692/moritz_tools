from mt import ensure_venv
ensure_venv(__file__)

import os
import re
import shutil
import requests
from getpass import getuser
from typing import Optional
from papertools import Console


def get_portable_link() -> Optional[str]:
    api_url: str = f"https://gitlab.com/api/v4/projects/librewolf/releases"
    response: requests.Response = requests.get(api_url)

    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Releases: {response.status_code}")
        return None

    releases: dict = response.json()
    if not releases:
        print("Keine Releases gefunden")
        return None
    latest_release: dict = releases[0]

    for asset in latest_release.get("assets", {}).get("links", []):
        if re.search(r'windows-x86_64-portable\.zip$', asset["name"]):
            return asset["url"]

    print('Kein entsprechendes LibreWolf Paket gefunden')
    return None


try:
    folder: str = 'C:\\Users\\Public\\librewolf\\'

    Console.print_colour(
        'Lädt LibreWolf herunter...', 'red')

    link: Optional[str] = get_portable_link()
    if not link:
        print('Fehler beim Abfragen der richtigen LibreWolf Version')
        input()
        exit()

    response: requests.Response = requests.get(link)
    zip_path: str = 'C:\\Temp\\librewolf.zip'

    if response.status_code == 200:
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        Console.print_colour('Librewolf .zip heruntergeladen', 'green')
    else:
        Console.print_colour(
            'Librewolf konnte nicht heruntergeladen werden', 'red')

    Console.print_colour('Entpackt LibreWolf', 'yellow')

    os.makedirs(
        folder, exist_ok=True)
    shutil.unpack_archive(zip_path, folder)

    Console.print_colour(
        'LibreWolf installiert, löscht Archiv', 'green')
    os.remove(zip_path)


finally:
    Console.print_colour('Drücke Enter um das Fenster zu schließen', 'green')
    input()
