docker buildx build -t yandex_game_analysis . --load
docker run -d -p 5000:80 yandex_game_analysis