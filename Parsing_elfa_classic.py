import requests
from bs4 import BeautifulSoup
import csv

CSV = 'elfa_classic_products.csv'
HOST = 'https://a-c.com.ua/ua/elfa_classic/'
URL = 'https://a-c.com.ua/ua/elfa_classic/1.html'
HEADERS_HOST = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
}

# 1) Отправка запороса на URL и получение объекта с кодом HTML и другой информацией_____________________________________
def get_html(url):
    object_request = requests.get(url, headers=HEADERS_HOST)
    #object_request.encoding='utf8'
    return object_request

#_______________________________________________________________________________________________________________________
#print(get_html(URL))          # 1) проверка функции get_html
#_______________________________________________________________________________________________________________________


# 2) Сбор общих данных с 1 карточки_____________________________________________________________________________________
def get_card_info(html):
    soup = BeautifulSoup(html, 'lxml')
    cards = soup.select('#main #cpagecnt #rightcnt ul#shop li')          # полный путь к элементам списка из-за НЕуникальности id
    #print(cards)           # проверка

    info_one_card = []

    for card in cards:
        print('Сбор данных ' + card.find('div', id='title').find('a').get_text())

        info_one_card.append(
            {
                'title': card.find('div', id='title').find('a').get_text(),
                'price': card.find('div', id='price').get_text(),
                'image': card.find('img').get('src'),
                'link': HOST + card.find('div', id='title').find('a').get('href')
            }
        )

    return info_one_card

#_______________________________________________________________________________________________________________________
# html = get_html(URL)                    # 2) проверка работы функции get_card_info
# print(get_card_info(html.text))
#_______________________________________________________________________________________________________________________


# 3) Сохранение общих данных из карточек в файл csv_____________________________________________________________________
def save_doc(items, path):
    with open(path, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Наименование товара',
                         'Цена',
                         'Фото',
                         'Ссылка'])
        for item in items:
            #print('Запись данных ' + item)                            # проверка в консоли - распечатка словарей с данными по карточке
            writer.writerow([item['title'],
                             item['price'],
                             item['image'],
                             item['link']
                             ])

#_______________________________________________________________________________________________________________________
# html = get_html(URL)                                         # 3) проверка работы функции save_doc
# info_one_card = get_card_info(html.text)
# save_doc(info_one_card, CSV)
# #_______________________________________________________________________________________________________________________


# Основная программа парсинга с пагинацией______________________________________________________________________________
PAGINATION = 4
html = get_html(URL)
if html.status_code == 200:
    all_info_cards = []
    for page in range(1, PAGINATION+1):
        print()
        print(f'_____________Страница: {page}________________', end='\n\n\n')
        URL_page = f'{HOST}{page}.html'
        html = get_html(URL_page)
        all_info_cards.extend(get_card_info(html.text))
    save_doc(all_info_cards, CSV)
else:
    print('Error')

