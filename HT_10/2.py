"""
Написати скрипт, який буде приймати від користувача назву валюти і початкову дату.
   - Перелік валют краще принтануть.
   - Також не забудьте указати, в якому форматі коритувач повинен ввести дату.
   - Додайте перевірку, чи введена дата не знаходиться у майбутньому ;)
   - Також перевірте, чи введена правильна валюта.
   Виконуючи запроси до API архіву курсу валют Приватбанку, вивести інформацію про зміну
   курсу обраної валюти (Нацбанк) від введеної дати до поточної.
"""


import requests
import datetime
import time


def currency_list():
    cur = []
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    delta = datetime.timedelta(days=1)
    today -= delta
    day = today.strftime('%d.%m.%Y')
    r = requests.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={day}')
    for i in r.json()["exchangeRate"][1::]:
        currency = i["currency"]
        if currency not in cur:
            cur.append(currency)
    return cur


def currency_change(cur, date):
    date_obj = datetime.datetime.strptime(date, '%d.%m.%Y')
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    if date_obj <= today:
        delta = datetime.timedelta(days=1)
        rate = 0
        while today >= date_obj:
            day = date_obj.strftime('%d.%m.%Y')
            today_r = requests.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={day}')
            print(f"Date: {today_r.json()['date']}")
            for i in today_r.json()["exchangeRate"][1::]:
                if cur == i["currency"]:
                    change = round(i["saleRateNB"] - rate, 4)
                    rate = i["saleRateNB"]
                    if change == rate:
                        change = "-------"
                    print(f"NB: {rate}  {change}")
            date_obj += delta
            time.sleep(0.5)
    else:
        print("Sorry, we can't predict future(")


available = currency_list()
print(f"Available currencies:\n{available}")
currency_input = input("Enter currency: ").upper()
if currency_input in available:
    date_input = input("Enter start date(dd.mm.yy): ")
    try:
        currency_change(currency_input, date_input)
    except ValueError:
        print("Wrong data format")
else:
    print("Wrong currency")
