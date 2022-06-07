import requests
from bs4 import BeautifulSoup
import csv

CSV = 'vacuum_cleaner.csv'
HOST = 'https://rozetka.com.ua/'
URL = 'https://rozetka.com.ua/clean_robots/c237815/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    r.encoding='utf8'
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('li', class_='catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted')
    vacuum_cleaner = []

#________________________________________________________________________
#     print(items)
# html = get_html(URL)        # проверка работы get_content
# get_content(html.text)
#________________________________________________________________________


    for item in items:
        #print(item.find('a', class_='goods-tile__heading ng-star-inserted').get('title'))
        #print(item.find('a', class_='goods-tile__heading ng-star-inserted').get('href'))

        vacuum_cleaner.append(
            {
                'title': item.find('a', class_='goods-tile__heading ng-star-inserted').get('title'),
                'link': HOST + item.find('a', class_='goods-tile__heading ng-star-inserted').get('href'),                 # HOST + item.find() - если ссылка не отображается
                'rating': item.find('div', class_='goods-tile__stars ng-star-inserted').find('svg').get('aria-label'),
                'comments_count': item.find('div', class_='goods-tile__stars ng-star-inserted').text.strip(),
                'price': item.find('div', class_='goods-tile__price').find('p', class_='ng-star-inserted').text.strip().replace('\xa0', ' '),
                #'cleaning_type': item.find('div', class_='goods-tile__hidden-holder').find('li', class_='goods-tile__description-item ng-star-inserted').text.strip(),
                #'cleaning_type': item.select_one('.goods-tile .goods-tile__inner .goods-tile__hidden-holder .goods-tile__hidden-content .goods-tile__description .goods-tile__description-item a').get_text(),
                'status': item.find('div', class_='goods-tile__availability goods-tile__availability--available ng-star-inserted').text.strip()
            }
        )

    return vacuum_cleaner

#____________________________________________________________________
# html = get_html(URL)                    # проверка работы цикла
# print(get_content(html.text))
#____________________________________________________________________


def save_doc(items, path):
    with open(path, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название пылесоса',
                         'Ссылка на товар',
                         'Цена',
                         'Рейтинг',
                         'Количество отзывов',
                         'Наличие'])
        for item in items:
            writer.writerow([item['title'],
                             item['link'],
                             item['price'],
                             item['rating'],
                             item['comments_count'],
                             item['status']])


def parser():
    PAGINATION = 1
    html = get_html(URL)
    if html.status_code == 200:                     # можно пользоваться методом __.ok, он включает значения до 400
        all_vacuum_cleaner = get_content(html.text)
        for page in range(2, PAGINATION+1):
            print(f'_____________Страница: {page}________________', end='\n\n\n')
            URL_page = f'{URL}/page={page}'
            html = get_html(URL_page)
            all_vacuum_cleaner.extend(get_content(html.text))
        save_doc(all_vacuum_cleaner, CSV)
    else:
        print('Error')

parser()

