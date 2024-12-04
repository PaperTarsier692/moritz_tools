Z:

cd Z:\Documents\moritz_tools
git pull

python -m venv .venv
call .venv\Scripts\activate.bat
pip install --upgrade -r requirements.txt

powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('Z:\Start Menu\Programs\Startup\moritz_tools.lnk');$s.TargetPath='Z:\Documents\moritz_tools\.venv\Scripts\pythonw.exe';$s.Arguments='Z:\Documents\moritz_tools\autorun.py';$s.IconLocation='Z:\Documents\moritz_tools\.venv\Scripts\pythonw.exe';$s.WorkingDirectory='Z:\Documents\moritz_tools';$s.WindowStyle=7;$s.Save()"


call autorun.bat
del "Z:\Start Menu\Programs\Startup\vsc_c.bat"
del "Z:\Start Menu\Programs\Startup\moritz.bat"
