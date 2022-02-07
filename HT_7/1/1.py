"""
Програма-банкомат.
   Створити програму з наступним функціоналом:
      - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл <users.data>);
      - кожен з користувачів має свій поточний баланс (файл <{username}_balance.data>) та історію транзакцій (файл <{username}_transactions.data>);
      - є можливість як вносити гроші, так і знімати їх. Обов'язкова перевірка введених даних (введено число; знімається не більше, ніж є на рахунку).
   Особливості реалізації:
      - файл з балансом - оновлюється кожен раз при зміні балансу (містить просто цифру з балансом);
      - файл - транзакціями - кожна транзакція у вигляді JSON рядка додається в кінець файла;
      - файл з користувачами: тільки читається. Якщо захочете реалізувати функціонал додавання нового користувача - не стримуйте себе :)
   Особливості функціонала:
      - за кожен функціонал відповідає окрема функція;
      - основна функція - <start()> - буде в собі містити весь workflow банкомата:
      - спочатку - логін користувача - програма запитує ім'я/пароль. Якщо вони неправильні - вивести повідомлення про це і закінчити роботу 
      (хочете - зробіть 3 спроби, а потім вже закінчити роботу - все на ентузіазмі :) )
      - потім - елементарне меню типа:
        Введіть дію:
           1. Продивитись баланс
           2. Поповнити баланс
           3. Вихід
"""


import json
import sys


def validate(user_name, user_password):
    inp = {"name": user_name, "password": user_password}
    valid = False
    with open("users_data.json", "r") as users_data:
        data = json.load(users_data)
        for user in data.values():
            if inp == user:
                valid = True
                break
    return valid


def add_transaction(user_name, prev_val, new_val):
    if new_val > prev_val:
        transaction = "replenish"
    else:
        transaction = "withdraw"
    data = {"transaction": transaction, "previous": prev_val, "new": new_val}
    with open(f"{user_name}_transactions.json", "a") as transactions:
        json.dump(data, transactions)
        transactions.write("\n")


def check_balance(user_name):
    with open(f"{user_name}_balance.txt", "r") as balance:
        currency = int(balance.readline())
        return f"Your current balance: {currency}"


def replenish(user_name):
    with open(f"{user_name}_balance.txt", "r") as balance:
        currency = int(balance.readline())
    add = int(input("How much money do you want to deposit?\n: "))
    if add >= 0:
        balance_new = currency + add
        with open(f"{user_name}_balance.txt", "w") as balance:
            balance.write(str(balance_new))
        add_transaction(user_name, currency, balance_new)
    else:
        print("Wrong input")


def withdraw(user_name):
    with open(f"{user_name}_balance.txt", "r") as balance:
        currency = int(balance.readline())
    wit = int(input("How much money do you want to withdraw?\n: "))
    if wit > 0:
        if wit <= currency:
            balance_new = currency - wit
            with open(f"{user_name}_balance.txt", "w") as balance:
                balance.write(str(balance_new))
            add_transaction(user_name, currency, balance_new)
        else:
            print("Can't withdraw more than available")
            withdraw(user_name)
    else:
        print("Wrong input")


def start():
    def back():
        choose = int(input("1. Back to menu\n2. Exit\n: "))
        if choose == 1:
            start()
        elif choose == 2:
            sys.exit()
    if validate(login, password):
        action = int(input("Choose operation:\n1. Check balance\n2. Replenish balance\n3. Withdraw money\n4. Exit\n: "))
        if action == 1:
            print(check_balance(login))
            back()
        elif action == 2:
            replenish(login)
            back()
        elif action == 3:
            withdraw(login)
            back()
        elif action == 4:
            sys.exit()
        else:
            print("Wrong input. Please try again\n")
            start()
    else:
        print("Wrong user data")


login = input("Enter login: ")
password = input("Enter password: ")
try:
    start()
except ValueError:
    print("Wrong input. Please try again")
    start()
