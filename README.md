# Magmin Scanner

To Install:
- Make an enviroment: `python3 -m venv venv`
- Start that enviroment. Then `python3 -m pip install -r requirements.txt`
- Make a '.env' File in project root and create a line `SERVER_SECRET = This is a secret!`

To Run
- `python3 .\src\main.py`

To Build
- `pyinstaller main.spec`

Newest Version Uses FFProbe and compiles with it's binaries baked in.
Full credit to https://ffmpeg.org/ffprobe.html


