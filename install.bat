@echo off


REM Startup Skripte

setx Path "C:\Program Files\CodeBlocks\MinGW\bin; %USERPROFILE%\AppData\Local\Microsoft\WindowsApps"

set vsc_c_command=setx Path "C:\Program Files\CodeBlocks\MinGW\bin; %USERPROFILE%\AppData\Local\Microsoft\WindowsApps"
set folder_command=python Z:Documents\moritz_tools\autorun.py

echo %vsc_c_command% > "Z:\Start Menu\Programs\Startup\moritz.bat"
echo %folder_command% >> "Z:\Start Menu\Programs\Startup\moritz.bat"
echo git pull >> "Z:\Start Menu\Programs\Startup\moritz.bat"


REM Python Setup

pip install -r requirements.txt


REM VSC_C Setup

set n=^&echo.
Z:
cd \
cd Desktop
mkdir VSC_C
cd VSC_C
echo #include ^<stdlib.h^>> main.c
echo #include ^<stdio.h^>>> main.c
echo %n%>>main.c
echo int main(){>> main.c
echo %n%    >>main.c
echo     return 0;>> main.c
echo }>> main.c
cd ..
echo [InternetShortcut]>VSC_C.url
echo URL="vscode://file/Z:/Desktop/VSC_C/">>VSC_C.url
cd VSC_C
code --goto main.c:5:4 --install-extension ms-vscode.cpptools --force --install-extension danielpinto8zz6.c-cpp-compile-run --force
pause