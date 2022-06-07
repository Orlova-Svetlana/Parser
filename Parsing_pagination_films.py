import requests
from bs4 import BeautifulSoup as BS
import csv

CSV = 'film.csv'
HOST = 'https://filmix.ac/'
URL = 'https://filmix.ac/filmi/komedia/c2/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    'cookie': 'FILMIXNET=eqm9q789a48bmb92fcqsst22tf; premiere_country=world; _ga=GA1.1.1984658493.1625917210; main_page_cat=0; x-a-key=sinatra; _listView=line; per_page_news=15; _ga_GYLWSWSZ3C=GS1.1.1653501414.74.1.1653504069.0'
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    #r.encoding = 'utf8'
    return r



def get_content(html):
    soup = BS(html, 'html.parser')
    items = soup.find_all('article', class_='shortstory line')
    films = []
    #print(items)
#html = get_html(URL)        # проверка работы get_content
#get_content(html.text)

    for item in items:
        print(item.find('h2', class_='name').get('content'))
        films.append(
            {
                'title': item.find('h2', class_='name').get('content'),
                'link': HOST + item.find('h2', class_='name').find('a').get('href'),                 # HOST + item.find() - если ссылка не отображается
                'yаer': item.find('div', class_='item year').find('a').get_text(),
                'like': item.find('span', class_='like').find('span').get_text()
            }
        )
    return films

# html = get_html(URL)                    # проверка работы цикла
# print(get_content(html.text))

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название фильма', 'Ссылка на фильм', 'Год выхода', 'Рейтинг'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['yаer'], item['like']])


def parser():
    PAGINATION = 2
    html = get_html(URL)
    if html.status_code == 200:                     # можно пользоваться методом __.ok, он включает значения до 400
        all_films = get_content(html.text)
        for page in range(2, PAGINATION+1):
            print(f'****Страница: {page}****')
            URL_page = f'{URL}pages/{page}/'
            html = get_html(URL_page)
            all_films.extend(get_content(html.text))
        save_doc(all_films, CSV)
    else:
        print('Error')

parser()