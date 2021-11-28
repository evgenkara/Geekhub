"""
Написати функцію < bank > , яка працює за наступною логікою: користувач робить вклад у розмірі < a > одиниць строком на < years > років 
під < percents > відсотків (кожен рік сума вкладу збільшується на цей відсоток, ці гроші додаються до суми вкладу і в наступному році на них також нараховуються відсотки). 
Параметр < percents > є необов'язковим і має значення по замовчуванню < 10 > (10%). Функція повинна принтануть і вернуть суму, яка буде на рахунку.
"""

def bank(a, years, percents = 10):
    for year in range(years):
        a += a * (percents / 100)
        a = round(a, 2)
    print(f"Balance after {years} years: {a}")
    return a

try:
    cash = int(input("Your initial contribution: "))
    term = int(input("Deposit term: "))
    perc = int(input("Percent: "))
    bank(cash, term, perc)
except ValueError:
    bank(cash,term)