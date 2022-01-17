"""
Напишіть скрейпер для сайту "vikka.ua", який буде приймати від користувача дату, збирати і зберігати інформацію
про новини за вказаний день.
Особливості реалізації:
    - використовувати лише Scrapy, BeautifulSoup (опціонально), lxml (опціонально) та вбудовані модулі Python
    - дані повинні зберігатися у csv файл з датою в якості назви у форматі "рік_місяць_число.csv" (напр. 2022_01_13.csv)
    - дані, які потрібно зберігати (саме в такому порядку вони мають бути у файлі):
        1. Заголовок новини
        2. Текст новини у форматі рядка без HTML тегів та у вигляді суцільного тексту
        3. Теги у форматі рядка, де всі теги записані з решіткою через кому (#назва_тегу, #назва_тегу, ...)
        4. URL новини
    - збереження даних у файл може відбуватися за бажанням або в самому спайдері, або через Pipelines
    - код повинен бути написаний з дотриманням вимог PEP8 (іменування змінних, функцій, класів, порядок імпортів,
    відступи, коментарі, документація і т.д.)
    - клієнт не повинен здогадуватися, що у вас в голові - додайте якісь підказки там, де це необхідно
    - клієнт може випадково ввести некорректні дані, пам'ятайте про це
    - Перед відправкою завдання - впевніться, що все працює і відповідає ТЗ.
    - не забудьте про requirements.txt
    - клієнт буде запускати бота через термінал командою "scrapy crawl назва_скрейпера"
"""

import datetime
import urllib.request

import scrapy
import lxml
from bs4 import BeautifulSoup
from scrapy.exceptions import CloseSpider


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.vikka.ua']
    start_urls = ['http://https://www.vikka.ua//']
    # asking for date input
    start_page = input("Enter date(Expected format: Year_month_date)\n: ")
    # saving to csv
    custom_settings = {
        'FEEDS': {
            f'{start_page}.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }

    def start_requests(self):
        try:
            # Validating date input
            date_obj = datetime.datetime.strptime(self.start_page, '%Y_%m_%d')
            today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            if date_obj <= today:
                start_url = f'https://www.vikka.ua/{self.start_page.replace("_", "/")}/'
                yield scrapy.Request(
                    url=start_url,
                    callback=self.parse_news
                )
            else:
                raise CloseSpider("Sorry, we can't predict future(")
        except ValueError:
            raise CloseSpider("Wrong date format.")

    def parse_news(self, response):
        """
        parses news archive page and sends article urls to parse_page method
        """
        soup = BeautifulSoup(response.text, 'lxml')
        for post in soup.select('.item-cat-post'):
            page = post.select_one('.more-link-style').get('href')
            news_data = self.parse_page(page)
            news_data.update({'url': page})
            yield news_data

    def parse_page(self, url):
        """
        Parses article page
        :param url: article url
        :return: dict with scraped information
        """
        data = urllib.request.urlopen(url)
        soup = BeautifulSoup(data.read(), 'lxml')
        fulltext = ""
        tags = [f'#{tag.text}' for tag in soup.select('.post-tag')]
        for item in soup.select('.entry-content div'):
            fulltext += ' ' + item.text
        if len(fulltext) <= 1:
            for item in soup.select('.entry-content p'):
                fulltext += ' ' + item.text
        return {
            'title': soup.select_one('.post-title').text,
            'text': fulltext.replace("\xa0", ""),
            'tags': ", ".join(tags),
        }
