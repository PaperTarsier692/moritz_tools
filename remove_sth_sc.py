from mt import ensure_venv
ensure_venv(__file__)

from context_menu import menus

menus.removeMenu('Send To Home', 'FILES')
menus.removeMenu('Send to home', 'DIRECTORY')
