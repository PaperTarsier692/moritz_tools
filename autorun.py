from mt import ensure_venv
ensure_venv(__file__)

from papertools import File
import winreg as reg
import os

install_cmd: str = '''
Z:
cd Documents
git clone https://github.com/PaperTarsier692/moritz_tools.git
cd moritz_tools
call install.bat
'''

if not os.path.exists('Y:/2BHIT/moritz/install.bat'):
    File('Y:/2BHIT/moritz/install.bat').write(install_cmd, create_path=True)


def disable_unc_check() -> None:
    try:
        key: reg.HKEYType = reg.CreateKey(reg.HKEY_CURRENT_USER,
                                          'Software\\Microsoft\\Command Processor')
        reg.SetValueEx(key, 'DisableUNCCheck', 0, reg.REG_DWORD, 1)
        reg.CloseKey(key)
        print('UNC-Meldung erfolgreich ausgemacht')
    except Exception as e:
        print(f'Fehler bei UNC-Meldung ausmachen {e}')


# disable_unc_check()
