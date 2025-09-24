from mt import ensure_venv, run_as_admin
ensure_venv(__file__)
run_as_admin()

from papertools import Console, Dir
from getpass import getuser
import os

PAR_DIR: str = f'C:\\Users\\{getuser()}\\moritz_tools\\'
os.makedirs(PAR_DIR, exist_ok=True)
PATH: str = f'{PAR_DIR}win11debloat'

STANDARD: list[str] = ['Disable_AI_Recall.reg', 'Disable_Bing_Cortana_In_Search.reg', 'Disable_Chat_Taskbar.reg', 'Disable_Click_to_Do.reg', 'Disable_Copilot.reg', 'Disable_Desktop_Spotlight.reg', 'Disable_Edge_Ads_And_Suggestions.reg', 'Disable_Edge_AI_Features.reg', 'Disable_Give_access_to_context_menu.reg', 'Disable_Include_in_library_from_context_menu.reg', 'Disable_Lockscreen_Tips.reg', 'Disable_Notepad_AI_Features.reg', 'Disable_Paint_AI_Features.reg', 'Disable_Phone_Link_In_Start.reg', 'Disable_Settings_365_Ads.reg', 'Disable_Settings_Home.reg',
                       'Show_Extensions_For_Known_File_Types.reg', 'Show_Hidden_Folders.reg']


try:
    if os.path.exists(PATH):
        Console.print_colour(
            'Win11Debloat gefunden, holt neueste Version ', 'green', end='')
        os.system(f'C: && cd {PATH} && git pull')
    else:
        Console.print_colour('Lädt Win11Debloat herunter... ', 'green', end='')
        os.system(
            f'C: && cd {PAR_DIR} && git clone https://github.com/Raphire/Win11Debloat.git win11debloat')
        Console.print_colour('    Done.', 'green')

    def apply_reg_file(reg_file_path: str) -> bool:
        if os.path.exists(reg_file_path):
            out: int = os.system(f'C: && regedit /s "{reg_file_path}"')
            print(f'Code: {out}')
            return True
        else:
            Console.print_colour(
                f"Registry-Datei existiert nicht: {reg_file_path}", 'red')
            return False

    print(f'{PATH}\\regfiles')
    for file in Dir.listfiles(f'{PATH}\\regfiles', abspath=True):
        if os.path.basename(file) in STANDARD:
            Console.print_colour(f'Applying registry file {file}', 'green')
            apply_reg_file(file)
        else:
            Console.print_colour(f'Skipping registry file {file}', 'yellow')


finally:
    Console.print_colour('Press any key to exit the program...', 'blue')
    input()
