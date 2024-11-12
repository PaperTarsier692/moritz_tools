from mt import ensure_venv, test_env, add_sth_sc
ensure_venv(__file__)

from papertools import File
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
    import winreg as reg
    try:
        key: reg.HKEYType = reg.CreateKey(reg.HKEY_CURRENT_USER,  # type: ignore
                                          'Software\\Microsoft\\Command Processor')
        reg.SetValueEx(key, 'DisableUNCCheck', 0,  # type: ignore
                       reg.REG_DWORD, 1)  # type: ignore
        reg.CloseKey(key)  # type: ignore
        print('UNC-Meldung erfolgreich ausgemacht')
    except Exception as e:
        print(f'Fehler bei UNC-Meldung ausmachen {e}')


def check_sth_sc() -> None:
    try:
        if File('config.json').json_r()['sth']['context']:
            add_sth_sc()
    except:
        pass


check_sth_sc()
# disable_unc_check()
