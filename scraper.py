import string

import requests

from bs4 import BeautifulSoup

import os


# функция для преобразования имени
def file_name(title):
    title = title.strip()
    new_title = ''
    for letter in title:
        if letter == ' ':
            new_title += '_'
        elif letter not in string.punctuation:
            new_title += letter
    new_title += '.txt'
    return new_title


# количество страничек и имя типа статьи
count_of_pages = int(input())
artilce_type = input()
# запрос на основную ссылку
for num_of_page in range(1, count_of_pages + 1):
    inp_url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={num_of_page}'
    r = requests.get(inp_url)
    # создаем папку с номером страницы
    os.mkdir(f'Page_{num_of_page}')
    # задаем направление создания файлов со статьями в эту папку
    os.chdir(f'/Users/ilyalyashenko/PycharmProjects/Web Scraper/Web Scraper/task/Page_{num_of_page}')

    # проверяем ссылку и ищем article
    if r:
        soup = BeautifulSoup(r.content, 'html.parser')
        all_articles = soup.find_all('article')
        news_articles = []

        # ищем статьи
        for article in all_articles:
            a_type = article.find('span', {'data-test': 'article.type'}).text
            if a_type == f'\n{artilce_type}\n':
                a_link = article.find('a', {'data-track-action': 'view article'})
                news_articles.append(a_link)

        # работаем с ссылками статей с страницы
        for a_link in news_articles:
            # создаем имя файла
            a_title = file_name(a_link.text)
            # работаем с файлом и урлом
            article_file = open(a_title, 'w')
            a_url = 'https://www.nature.com' + a_link.get('href')
            r2 = requests.get(a_url)
            soup2 = BeautifulSoup(r2.content, 'html.parser')
            # записываем тело статьи в файл
            body = soup2.find('div', {'class': 'c-article-body'}, {'class': 'article-item__body'}).text

            article_file.write(body)
            article_file.close()
# меняем направление в исходную папку
    os.chdir('/Users/ilyalyashenko/PycharmProjects/Web Scraper/Web Scraper/task')
