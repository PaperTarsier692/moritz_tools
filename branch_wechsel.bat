@echo off
echo Diese Datei wechselt zurück zu der Hauptversion von moritz_tools, einige Features werden evtl. Fehlen
pause
Z:
cd Documents\moritz_tools
git switch main
git reset --hard
git pull