import requests
from bs4 import BeautifulSoup

# Функция для получения всех мемов с нескольких страниц
def get_all_memes(pages=1):
    memes = []
    base_url = 'https://www.memify.ru/top/?page='

    for page in range(1, pages + 1):
        url = f'{base_url}{page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        meme_container = soup.find('div', class_='meme-list infinite-container')

        meme_links = meme_container.find_all('a', href=True)

        for link in meme_links:
            if link['href'].startswith('https://www.cdn.memify.ru'):
                memes.append(link['href'])

    return memes