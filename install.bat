@echo off

Z:

REM Startup Skripte

echo Z: > "Z:\Start Menu\Programs\Startup\moritz.bat"
echo cd Z:\Documents\moritz_tools >> "Z:\Start Menu\Programs\Startup\moritz.bat"
echo autorun.bat >> "Z:\Start Menu\Programs\Startup\moritz.bat"

REM Setup
cd Z:\Documents\moritz_tools
git pull
call autorun.bat

del "Z:\Start Menu\Programs\Startup\vsc_c.bat"


REM Python Setup

python -m venv .venv
call .venv\bin\activate.bat
pip install --upgrade pip
pip install --upgrade -r requirements.txt

