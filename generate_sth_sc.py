from mt import ensure_venv
ensure_venv(__file__)

from context_menu import menus
from sys import executable
fc = menus.FastCommand('Send To Home', type='FILES',
                       command=f'Z: && cd Z:\\Documents\\moritz_tools && "{executable}" "Z:\\Documents\\moritz_tools\\send_to_home_sc.py" ?', command_vars=['FILENAME'])
fc.compile()

fc2 = menus.FastCommand('Send To Home', type='DIRECTORY',
                        command=f'Z: && cd Z:\\Documents\\moritz_tools && "{executable}" "Z:\\Documents\\moritz_tools\\send_to_home_sc.py" ?', command_vars=['DIRECTORY'])
fc2.compile()
