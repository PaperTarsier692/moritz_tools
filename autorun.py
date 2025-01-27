from mt import ensure_venv, add_sth_sc, Webhook
ensure_venv(__file__)

from papertools import File
from getpass import getuser
import subprocess
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


def vsc() -> None:
    if os.path.exists(f'C:\\Users\\{getuser()}\\vsc\\'):
        print('VSC gefunden')
        os.system(fr'''powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('Z:\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk');$s.TargetPath='C:\Users\{
                  getuser()}\vsc\code';$s.Save()"''')


def name_list() -> None:
    if not getuser() in File('Y:/2BHIT/moritz/users.txt').read(True):
        File('Y:/2BHIT/moritz/users.txt').append(getuser(), True)


def log() -> None:
    Webhook(
        'https://discord.com/api/webhooks/1333368102817104024/p1_gzb1zV3CVYyrjKce2GgkH5pYAnKDRS8pn4NXsOzvQ9ciFyoEywpr5AwUUV89vMV31', getuser)


subprocess.run(['cmd', '/c', r'Z:\Documents\moritz_tools\autorun.bat'],
               shell=True,
               creationflags=subprocess.CREATE_NO_WINDOW)  # type: ignore

vsc()
check_sth_sc()
name_list()
log()

try:
    if File('config.json').json_r()['other']['unc']:
        disable_unc_check()
except:
    pass
