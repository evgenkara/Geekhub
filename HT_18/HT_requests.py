"""
Використовуючи бібліотеку requests написати скрейпер для отримання статей / записів із АПІ
Скрипт повинен отримувати із командного рядка одну із наступних категорій:
askstories, showstories, newstories, jobstories
Якщо жодної категорії не указано - використовувати newstories.
Якщо категорія не входить в список - вивести попередження про це і завершити роботу.
Результати роботи зберегти в CSV файл. Зберігати всі доступні поля. Зверніть увагу - інстанси різних типів мають різний
набір полів.
Код повинен притримуватися стандарту pep8.

"""

import csv
import requests
import sys


class CsvWriter(object):

    def __init__(self, data):
        self.data = data

    def get_fieldnames(self):
        fieldnames = []
        for post in self.data:
            for key in post.keys():
                if key not in fieldnames:
                    fieldnames.append(key)
        return fieldnames

    def to_csv(self, filename):
        with open(f'{filename}.csv', 'w', encoding="utf-8", newline='') as csvfile:
            fieldnames = self.get_fieldnames()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for post in self.data:
                writer.writerow(post)


class Scraper(object):

    categories_available = ['askstories', 'showstories', 'newstories', 'jobstories']

    @staticmethod
    def get_item(post_id):
        req_item = dict(requests.get(f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json").json())
        return req_item

    def get_articles(self, category_given):
        posts = []
        print(f"Script started. Chosen category: {category_given}")
        r = requests.get(f"https://hacker-news.firebaseio.com/v0/{category_given}.json")
        for item in r.json():
            posts.append(self.get_item(item))
        print("Completed")
        return posts

    def start(self, category):
        if category in self.categories_available:
            articles = self.get_articles(category)
            csv_writer = CsvWriter(articles)
            csv_writer.to_csv(category)
        else:
            print("Wrong input")
            sys.exit()


scraper = Scraper()
try:
    article_category = sys.argv[1].lower()
    scraper.start(article_category)
except IndexError:
    scraper.start('newstories')
