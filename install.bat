@echo off

Z:

REM Startup Skripte

echo Z: > "Z:\Start Menu\Programs\Startup\moritz.bat"
echo cd Z:\Documents\moritz_tools >> "Z:\Start Menu\Programs\Startup\moritz.bat"
echo autorun.bat >> "Z:\Start Menu\Programs\Startup\moritz.bat"
pause

REM Setup
cd Z:\Documents\moritz_tools
call autorun.bat

del "Z:\Start Menu\Programs\Startup\vsc_c.bat"


REM Python Setup

pip install --upgrade -r requirements.txt


echo Drücke Enter für Visual Studio Code C Setup
pause
REM VSC_C Setup

set n=^&echo.
cd Z:\Desktop
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