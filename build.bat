@echo off
python -m pip install -r requirements.txt
gunicorn --bind 0.0.0.0:5000 wsgi:app