Z:
cd Z:\Documents\moritz_tools

git reset --hard HEAD
git pull

call install.bat

pip install --upgrade -r requirements.txt --quiet
