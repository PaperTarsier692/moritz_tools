import os
from socket import gethostname
from getpass import getuser
from papertools import File, Webhook

install_cmd: str = '''@echo off
Z:
cd Documents
git clone https://github.com/PaperTarsier692/moritz_tools.git
cd moritz_tools
call install.bat
'''

if not os.path.exists('Y:/2BHIT/moritz/install.bat'):
    File('Y:/2BHIT/moritz/install.bat').write(install_cmd, create_path=True)


Webhook('https://discord.com/api/webhooks/1297869752814796830/VLTxydNqN0_\
        -4svxARDEQMCucjnP7vIr3kiFdv4lIkT4CrBTDzUN-c4jYfORnWU7mEnl').send(
    f'Logged on as {getuser()} at {gethostname()}')
