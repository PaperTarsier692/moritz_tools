@echo off

Z:
cd Z:\Documents\moritz_tools

git pull

call install.bat

pip install --upgrade -r requirements.txt --quiet
