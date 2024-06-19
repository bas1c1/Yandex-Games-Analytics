@echo off
python -m pip install -r requirements.txt
python -m pip install waitress
python -m waitress --listen=*:5000 wsgi:app