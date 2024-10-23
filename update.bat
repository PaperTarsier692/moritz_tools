@echo off

Z:
cd Z:\Documents\moritz_tools

git pull 

call install.bat

setx Path "C:\Program Files\CodeBlocks\MinGW\bin; %USERPROFILE%\AppData\Local\Microsoft\WindowsApps"
pip install --upgrade -r requirements.txt --quiet
python autorun.py
