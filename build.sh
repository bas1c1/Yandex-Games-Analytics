#Dockerfile нуждается в доработке, так как Selenium не запускается в Docker.

#docker buildx build -t yandex_game_analysis . --load
#docker run -d -p 5000:80 yandex_game_analysis

#python3 -m venv env
#source env/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install gunicorn
gunicorn --bind 0.0.0.0:5000 wsgi:app