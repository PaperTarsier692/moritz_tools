Z:
cd Z:\Documents\moritz_tools

git reset --hard HEAD
git pull | findstr /C:"Updating"
if %errorlevel% equ 0 goto update

setx Path "C:\Program Files\CodeBlocks\MinGW\bin; %USERPROFILE%\AppData\Local\Microsoft\WindowsApps"

call .venv\Scripts\activate.bat
pip install -r requirements.txt
pip install --upgrade papertools
python autorun.py

goto finish

:update
call install.bat

:finish