from context_menu import menus
from sys import executable
fc = menus.FastCommand('Send To Home', type='FILES', command=f'"{executable}" "Z:\\Documents\\moritz_tools\\send_to_home_sc.py" ? ', command_vars=['FILENAME'])
fc.compile()

