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
