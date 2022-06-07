import requests
from bs4 import BeautifulSoup as BS
import csv

CSV = 'cards.csv'
HOST = 'https://minfin.com.ua/'
URL = 'https://minfin.com.ua/ua/cards/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    r.encoding = 'utf8'
    return r


def get_content(html):
    soup = BS(html, 'html.parser')
    items = soup.find_all('div', class_='sc-182gfyr-0 jmBHNg')
    cards = []

    for item in items:
        cards.append(
            {
                'title': item.find('a', class_='cpshbz-0 knHhYO').get('alt'),
                'link': HOST + item.find('a', class_='cpshbz-0 knHhYO').get('href'),
                'brend': item.find('a', class_='be80pr-35 UOQtz').get('alt'),
                'image': item.find('img', class_='be80pr-10 jIGseK').get('src')
            }
        )
    return cards


def save_doc(items, path):
    with open(path, 'w', encoding = 'utf8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название карты', 'Ссылка на карту', 'Банк', 'Изображение карты'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['brend'], item['image']])


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        all_cards = []
        all_cards.extend(get_content(html.text))
        save_doc(all_cards, CSV)
    else:
        print('Error')


parser()
