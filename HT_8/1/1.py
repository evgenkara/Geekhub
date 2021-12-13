import json
import sys


def validate(user_name, user_password):
    valid = False
    is_admin = False
    with open("users_data.json", "r") as users_data:
        data = json.load(users_data)
        for user in data:
            if user_name == user["name"] and user_password == user["password"]:
                valid = True
                if user["role"] == "admin":
                    is_admin = True
                break
    return valid, is_admin


def check_balance(user_name):
    with open(f"{user_name}_balance.txt", "r") as user_balance:
        balance = int(user_balance.readline())
        return f"Current balance: {balance}"


def add_transaction(user_name, old_bal, new_bal):
    if new_bal > old_bal:
        transaction = "deposit"
    else:
        transaction = "withdraw"
    data = {"transaction": transaction, "before": old_bal, "after": new_bal}
    with open(f"{user_name}_transactions.json", "a") as transactions:
        json.dump(data, transactions)
        transactions.write("\n")


def replenish(user_name):
    dep = int(input("How much money do you want to deposit?\n: "))
    with open(f"{user_name}_balance.txt", "r") as user_balance:
        balance = int(user_balance.readline())
    if dep > 0:
        new_balance = balance + dep
        with open(f"{user_name}_balance.txt", "w") as user_balance:
            user_balance.write(str(new_balance))
            add_transaction(user_name, balance, new_balance)
    else:
        print("Wrong input")


def withdraw_balance(num):
    with open("banknotes.json", "r+") as banknotes_change:
        banknotes_load = json.load(banknotes_change)
        keys = list(map(int, banknotes_load.keys()))
        dic = {}
        new_bank = {}
        for key, val in zip(keys, banknotes_load.values()):
            if num >= key:
                dic[key] = num // key
                val -= num // key
                num -= dic[key] * key
            new_bank[key] = val

    with open("banknotes.json", "w") as banknotes_change:
        json.dump(new_bank, banknotes_change)
    print(f"Given banknotes: {dic}")


def withdraw(user_name):
    bank_sum = 0
    with open("banknotes.json", "r+") as banknotes, open(f"{user_name}_balance.txt", "r") as balance:
        currency = int(balance.readline())
        load = json.load(banknotes)
        for key, value in zip(load.keys(), load.values()):
            bank_sum += int(key) * value
    wit = int(input(f"Now in stock: {bank_sum}\nHow much money do you want to withdraw?\n: "))
    if wit > 0 and wit % 10 == 0:
        if wit <= bank_sum:
            balance_new = currency - wit
            with open(f"{user_name}_balance.txt", "w") as balance:
                balance.write(str(balance_new))
            add_transaction(user_name, currency, balance_new)
            print(withdraw_balance(wit))
        else:
            print(f"Not enough money in the ATM. Now in stock: {bank_sum}")
    else:
        print("Please enter positive amount which is multiple by zero")
        withdraw(user_name)


def register():
    reg_name = input("Enter username: ")
    reg_password = input("Enter password: ")
    not_occupied = True
    with open("users_data.json", "r+") as users_data:
        data = json.load(users_data)
        reg_data = {"name": reg_name, "password": reg_password, "role": "user"}
        for user in data:
            if user["name"] == reg_name:
                not_occupied = False
                break
        if not_occupied:
            data.append(reg_data)
            with open("users_data.json", "w") as write_data:
                json.dump(data, write_data)
        else:
            print("Username is already occupied")


def user_menu(user_name):
    action = int(input("Choose operation:\n1. Check balance\n2. Replenish balance\n3. Withdraw money\n4. Exit\n: "))
    if action == 1:
        print(check_balance(user_name))
    elif action == 2:
        replenish(user_name)
    elif action == 3:
        withdraw(user_name)
    elif action == 4:
        sys.exit()
    else:
        print("Wrong input")


def check_banknotes():
    with open("banknotes.json", "r") as banknotes:
        return json.load(banknotes)


def change_banknotes():
    choice = input("Choose banknote: ")
    with open("banknotes.json", "r+") as banknotes:
        available = json.load(banknotes)
        if choice in available.keys():
            new = int(input("Enter new amount: "))
            if new >= 0:
                available[choice] = new
                with open("banknotes.json", "w+") as changed_banknotes:
                    json.dump(available, changed_banknotes)
            else:
                print("Can't change amount to negative. Please, try again")
                change_banknotes()
        else:
            print("Please, choose from available variants(10, 20, 50, 100, 200, 500, 1000)")
            change_banknotes()


def admin_menu():
    action = int(input("Choose operation:\n1. View available banknotes\n2. Change banknotes\n3. Exit\n: "))
    if action == 1:
        print(check_banknotes())
    elif action == 2:
        change_banknotes()
    elif action == 3:
        sys.exit()
    else:
        print("Wrong input. Please try again")


def start(user_name, user_password):
    if validate(user_name, user_password)[0]:
        if validate(user_name, user_password)[1]:
            admin_menu()
            start(user_name, user_password)
        else:
            user_menu(user_name)
            start(user_name, user_password)
    else:
        reg = int(input("User doesn't exist. Do you want to register?\n1. Yes\n2. No\n: "))
        if reg == 1:
            register()
        else:
            sys.exit()


username = input("Enter username: ")
password = input("Enter password: ")

start(username, password)
