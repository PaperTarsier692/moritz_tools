import os
from papertools import File

install_cmd: str = '''@echo off
Z:
cd Documents
git clone https://github.com/PaperTarsier692/moritz_tools.git
cd moritz_tools
call install.bat
'''

if not os.path.exists('Y:/2BHIT/moritz/install.bat'):
    File('Y:/2BHIT/moritz/install.bat').write()
