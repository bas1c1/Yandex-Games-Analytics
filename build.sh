#Dockerfile нуждается в доработке, так как Selenium не запускается в Docker.

#docker buildx build -t yandex_game_analysis . --load
#docker run -d -p 5000:80 yandex_game_analysis

python3 main.py
