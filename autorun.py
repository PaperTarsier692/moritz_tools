from mt import ensure_venv
ensure_venv(__file__)

from papertools import File, Webhook
from socket import gethostname
from getpass import getuser
import os

install_cmd: str = '''@echo on
Z:
cd Documents
git clone --branch dev https://github.com/PaperTarsier692/moritz_tools.git
cd moritz_tools
call install.bat
'''

if not os.path.exists('Y:/2BHIT/moritz/install-dev.bat'):
    File('Y:/2BHIT/moritz/install-dev.bat').write(install_cmd, create_path=True)


Webhook('https://discord.com/api/webhooks/1297869752814796830/VLTxydNqN0_-4svxARDEQMCucjnP7vIr3kiFdv4lIkT4CrBTDzUN-c4jYfORnWU7mEnl').send(
    f'Dev, Logged on as {getuser()} at {gethostname()}')
