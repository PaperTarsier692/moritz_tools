@echo off

Z:
cd Z:\Documents\moritz_tools

git pull | findstr /C:"Updating"
if %errorlevel% equ 0 goto update

setx Path "C:\Program Files\CodeBlocks\MinGW\bin; %USERPROFILE%\AppData\Local\Microsoft\WindowsApps"
pip install -r requirements.txt
python autorun.py

goto finish

:update
echo UPDATED>update.txt
call install.bat

:finish