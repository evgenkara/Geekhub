"""
Конвертер валют. Прийматиме від користувача назву двох валют і суму (для першої).
   Робить запрос до API архіву курсу валют Приватбанку (на поточну дату) і виконує
   конвертацію введеної суми з однієї валюти в іншу
"""


import requests
import datetime


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


def convert(cur_1, cur_2, amount):
    new_amount = amount
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    delta = datetime.timedelta(days=1)
    while True:
        day = today.strftime('%d.%m.%Y')
        today_r = requests.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={day}')
        if len(today_r.json()["exchangeRate"]) == 0:
            today -= delta
            continue
        else:
            for i in today_r.json()["exchangeRate"][1::]:
                if cur_1 == i["currency"]:
                    new_amount *= i["saleRateNB"]
                    for j in today_r.json()["exchangeRate"][1::]:
                        if cur_2 == j["currency"]:
                            new_amount /= j["saleRateNB"]
                            return f"{amount} {cur_1} = {round(new_amount, 2)} {cur_2}"


available = currency_list()
print(f"Available currencies:\n{available}")
currency_1 = input("Enter first currency: ").upper()
currency_2 = input("Enter second currency: ").upper()


if currency_1 in available and currency_1 in available:
    amnt = int(input("Enter amount: "))
    if amnt >= 0:
        print(convert(currency_1, currency_2, amnt))
    else:
        print("Please, enter positive amount")
else:
    print("Wrong currency")
