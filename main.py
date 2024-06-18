from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
app = Flask(__name__)

useragent = UserAgent()

options = Options()
options.add_argument("--headless")

options.add_argument(f'user-agent={useragent.random}')

browser = webdriver.Chrome(chrome_options=options)

url = "https://yandex.ru/games/all-games"

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/')
def main_page():
    page = request.args.get('page', '')
    page = int(page) if page != '' else 1
    return render_template('index.html', page=page)

@app.route('/game/<int:id_>')
def game_page(id_):
    return render_template('game.html', id=id_)

@app.route('/get_list_of_names')
def api_get_list_of_names():
    page = request.args.get('page', '')
    json_info = {}

    temp_url = f"{url}?page={page}"

    browser.get(temp_url)

    temp_html = browser.page_source
    temp_soup = BeautifulSoup(temp_html, 'lxml')

    while len(temp_soup.findAll('span', class_='Text Text_weight_medium Text_typography_headline-s')) > 0 or len(temp_soup.findAll('a', class_='Link Link_color_secondary Link_view_captcha')) > 0:
        temp_html = browser.page_source
        temp_soup = BeautifulSoup(temp_html, 'lxml')

    lis = temp_soup.findAll('div', class_='game-card game-card_size_all_games_desktop game-card_transform game-card_type_suggested grid-list__card')
    if len(lis) == 0:
        lis = temp_soup.findAll('div', class_='game-card game-card_size_all_games_mobile game-card_transform game-card_type_suggested')
    for j in lis:
        id_ = str(j.findAll('a', class_='game-url game-card__game-url play')[0].get_attribute_list("href")[0]).split('/')[3]
        name = j.findAll('span', class_='game-card__title game-card__no-caption')[0].text
        img = j.findAll('img', class_='game-image game-image_size_all_games_desktop game-card__image')[0].get_attribute_list("src")[0]
        json_info[name] = {
            "img": img,
            "id": id_
        }

    return jsonify(json_info)

@app.route('/get_info_by_id')
def api_get_info_by_id():
    id_ = request.args.get('id', '')
    json_info = {}

    temp_url = f"https://yandex.ru/games/app/{id_}"

    browser.get(temp_url)

    temp_html = browser.page_source
    temp_soup = BeautifulSoup(temp_html, 'lxml')

    while len(temp_soup.findAll('span', class_='Text Text_weight_medium Text_typography_headline-s')) > 0 or len(temp_soup.findAll('a', class_='Link Link_color_secondary Link_view_captcha')) > 0:
        temp_html = browser.page_source
        temp_soup = BeautifulSoup(temp_html, 'lxml')

    score = temp_soup.findAll('span', class_='game-quality-score__value')
    rating = temp_soup.findAll('span', class_='game-rating-description__rating')
    name = temp_soup.findAll('h1', class_='play-guard-dialog__description-title')
    img = temp_soup.findAll('img', class_='image__img')#[0].get_attribute_list("src")[0]

    score = '00' if len(score) == 0 else score[0].text
    rating = '00' if len(rating) == 0 else rating[0].text
    name = temp_soup.findAll('h1', class_='game-page__title')[0].text if len(name) == 0 else name[0].text
    img = temp_soup.findAll('img', class_='game-image game-image_size_page_icon_mobile_with_play game-page__image')[0].get_attribute_list("src")[0] if len(img) == 0 else img[0].get_attribute_list("src")[0]
    
    json_info[name] = {
        "score": score,
        "rating": rating,
        "img": img
    }

    return jsonify(json_info)

@app.route('/get_info_by_length')
def api_get_info_by_length():
    length = request.args.get('length', '')
    json_info = {}

    browser.get(url)

    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')

    index = 0

    for i in range(1, 229):
        browser.get(f"{url}?page={i}")

        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')

        lis = soup.findAll('a', class_='game-url game-card__game-url play')
        for j in lis:
            href = j.get_attribute_list("href")[0]
            temp_url = f"https://yandex.ru{href}"

            browser.get(temp_url)

            temp_html = browser.page_source
            temp_soup = BeautifulSoup(temp_html, 'lxml')

            while len(temp_soup.findAll('span', class_='Text Text_weight_medium Text_typography_headline-s')) > 0 or len(temp_soup.findAll('a', class_='Link Link_color_secondary Link_view_captcha')) > 0:
                temp_html = browser.page_source
                temp_soup = BeautifulSoup(temp_html, 'lxml')

            score = temp_soup.findAll('span', class_='game-quality-score__value')
            rating = temp_soup.findAll('span', class_='game-rating-description__rating')
            name = temp_soup.findAll('h1', class_='play-guard-dialog__description-title')

            score = '00' if (len(score) == 0) else score[0].text
            rating = '00' if (len(rating) == 0) else rating[0].text
            name = temp_soup.findAll('h1', class_='game-page__title')[0].text if (len(name) == 0) else name[0].text
            
            json_info[name] = {
                "score": score,
                "rating": rating
            }

            if length != 'all':
                index += 1

                if index >= int(length):
                    return jsonify(json_info)

    return jsonify(json_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    