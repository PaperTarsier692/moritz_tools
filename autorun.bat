Z:
cd Z:\Documents\moritz_tools

echo executed>executed

git reset --hard HEAD
git pull | findstr /C:"Updating"
if %errorlevel% equ 0 goto update

setx Path "C:\Program Files\CodeBlocks\MinGW\bin; %USERPROFILE%\AppData\Local\Microsoft\WindowsApps"

mkdir Y:\2BHIT\test

call .venv\Scripts\activate.bat
pip install -r requirements.txt

goto finish

:update
call install.bat

:finish