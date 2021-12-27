import requests
import lxml
import csv
from bs4 import BeautifulSoup
import time
import sqlite3


def scrape_author(url):
    author_inf = requests.get(url)
    author_soup = BeautifulSoup(author_inf.text, 'lxml')
    author_date = author_soup.select_one(".author-born-date").text
    author_loc = author_soup.select_one(".author-born-location").text
    author_born = author_date + " " + author_loc
    author_info = author_soup.select_one(".author-description").text
    return author_born, author_info


def to_csv(data_list):
    with open('quotes.csv', 'w') as quotes:
        fieldnames = ["Quote", "Author", "Author_birth", "Author_info"]
        writer = csv.DictWriter(quotes, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)


def scrape(url, data_list):
    con = sqlite3.connect("Quotes.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS quotes (Quote text, Author text)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS authors(Author text PRIMARY KEY, 
                    Author_born text, Author_info text, FOREIGN KEY (Author) REFERENCES quotes(Author))''')
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    quotes = soup.select('.quote')
    for quote in quotes:
        text = quote.find('span', {'class': 'text'}).text
        text = text.replace(";", ":")
        author = quote.find('small', {'class': 'author'}).text
        ref = quote.select_one("a").get('href')
        author_born = scrape_author('http://quotes.toscrape.com' + ref)[0]
        author_info = scrape_author('http://quotes.toscrape.com' + ref)[1].strip()
        data_list.append({"Quote": text, "Author": author, "Author_birth": author_born, "Author_info": author_info})
        cur.execute('''INSERT INTO quotes (Quote, Author) VALUES (?,?)''',
                    (text, author))
        cur.execute('''INSERT OR IGNORE INTO authors VALUES (?,?,?)''',
                    (author, author_born, author_info))
    con.commit()
    ref_next = soup.select_one('.next a')
    if ref_next:
        next_url = ref_next.get('href')
        time.sleep(0.5)
        scrape(f"http://quotes.toscrape.com{next_url}", data_list)


data = []
start_url = "http://quotes.toscrape.com/page/1/"
scrape(start_url, data)
to_csv(data)
print("Scrapping completed")
