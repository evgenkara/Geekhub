import sqlite3
import sys


class BankException(Exception):
    pass


con = sqlite3.connect("ATM.db")
cur = con.cursor()


def create_tables():
    cur.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id integer PRIMARY KEY, username text, password text, 
                    is_incasator BOOLEAN NOT NULL CHECK (is_incasator IN (0,1)), UNIQUE (username)) ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS balance
                    ( id integer PRIMARY KEY, 
                    username text, 
                    user_balance integer, 
                    FOREIGN KEY (id) REFERENCES users(id))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS banknotes (key integer PRIMARY KEY, banknote integer, amount integer )''')
    con.commit()


def insert_tables():
    cur.execute('''INSERT OR IGNORE INTO users VALUES (1, "user1", "user1", 0), (2, "user2", "user2", 0), 
                (3, "admin", "admin", 1)''')
    cur.execute("INSERT OR IGNORE INTO balance VALUES (1, 'user1', 10000), (2, 'user2', 8800), (3, 'admin', 20000)")
    cur.execute('''INSERT OR IGNORE INTO banknotes VALUES (1, 1000, 10), (2, 500, 8), (3, 200, 5), 
                (4, 100, 10), (5, 50, 8), (6, 20, 5), (7, 10, 10)''')
    con.commit()


def validate(user_name, user_password):
    valid = False
    is_admin = False
    cur.execute("SELECT is_incasator FROM users WHERE username = ? AND password = ?", (user_name, user_password))
    user = cur.fetchone()
    if user:
        valid = True
        if 1 in user:
            is_admin = True
    return valid, is_admin


def check_balance(user_name):
    cur.execute("SELECT user_balance FROM balance WHERE username = ?", (user_name,))
    balance = cur.fetchone()[0]
    return f"Current balance: {str(balance)}"


def add_transaction(user_name, old_bal, new_bal):
    if new_bal > old_bal:
        transaction = "deposit"
    else:
        transaction = "withdraw"
    cur.execute(f"CREATE TABLE IF NOT EXISTS {user_name}_transactions (operation text, before integer, after integer)")
    cur.execute(f"INSERT INTO {user_name}_transactions VALUES (?, ?, ?)", (transaction, old_bal, new_bal))
    con.commit()


def replenish(user_name):
    dep = int(input("How much money do you want to deposit?\n: "))
    cur.execute("SELECT user_balance FROM balance WHERE username = ?", (user_name,))
    balance = cur.fetchone()[0]
    if dep > 0:
        new_balance = balance + dep
        cur.execute(''' UPDATE balance SET user_balance = ? WHERE username = ?''', (new_balance, user_name))
        con.commit()
        add_transaction(user_name, balance, new_balance)
    else:
        print("Wrong input")


def withdraw_balance(num):
    cur.execute("SELECT banknote, amount FROM banknotes")
    banknotes_load = {bank[0]: bank[1] for bank in cur.fetchall()}
    keys = list(map(int, banknotes_load.keys()))
    wit_banknotes = []
    counter = 0
    while sum(wit_banknotes) < num:
        skip = False
        if counter + 1 > len(keys):
            raise BankException
        for key in keys:
            if skip:
                break
            elif key + sum(wit_banknotes) <= num and banknotes_load[key] > 0:
                for k in keys:
                    if (num - sum(wit_banknotes) - key) % k == 0 and banknotes_load[k] > 0:
                        wit_banknotes.append(key)
                        banknotes_load[key] -= 1
                        skip = True
                        break
        counter += 1
    for key, val in zip(banknotes_load.keys(), banknotes_load.values()):
        cur.execute("UPDATE banknotes SET amount = ? WHERE banknote = ?", (val, key))
        con.commit()
    return f"Given banknotes: {wit_banknotes}"


def withdraw(user_name):
    bank_sum = 0
    cur.execute("SELECT banknote, amount FROM banknotes")
    for bank in cur.fetchall():
        bank_sum += bank[0] * bank[1]
    cur.execute("SELECT user_balance FROM balance WHERE username = ?", (user_name,))
    currency = cur.fetchone()[0]
    wit = int(input(f"Now in stock: {bank_sum}\nHow much money do you want to withdraw?\n: "))
    if wit > 0 and wit % 10 == 0:
        if wit <= bank_sum:
            balance_new = currency - wit
            cur.execute("UPDATE balance SET user_balance = ? WHERE username = ?", (balance_new, user_name))
            add_transaction(user_name, currency, balance_new)
            try:
                print(withdraw_balance(wit))
            except BankException:
                w = int(input("Not enough banknotes in ATM. Please, enter another value\n: "))
                print(withdraw_balance(w))
        else:
            print(f"Not enough money in the ATM. Now in stock: {bank_sum}")
    else:
        print("Please enter positive amount which is multiple by zero")
        withdraw(user_name)
    con.commit()


def register():
    reg_name = input("Enter username: ")
    reg_password = input("Enter password: ")
    not_occupied = True
    cur.execute("SELECT * FROM users WHERE username = ?", (reg_name,))
    user = cur.fetchall()
    cur.execute("SELECT max(id) FROM users")
    last_id = cur.fetchone()[0]
    if user:
        not_occupied = False
    if not_occupied:
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (last_id + 1, reg_name, reg_password, 0))
        cur.execute("INSERT INTO balance VALUES (?, ?, ?)", (last_id + 1, reg_name, 0))
        con.commit()
    else:
        print("Username is already occupied")


def user_menu(user_name):
    try:
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
    except ValueError:
        print("Wrong input. Please try again")


def check_banknotes():
    cur.execute("SELECT banknote, amount FROM banknotes")
    result = {bank[0]: bank[1] for bank in cur.fetchall()}
    return result


def change_banknotes():
    choice = input("Choose banknote: ")
    cur.execute("SELECT * FROM banknotes WHERE banknote = ?", (choice,))
    if cur.fetchone():
        new = int(input("Enter new amount: "))
        if new >= 0:
            cur.execute("UPDATE banknotes SET amount = ? WHERE banknote = ?", (new, choice))
        else:
            print("Can't change amount to negative. Please, try again")
            change_banknotes()
    else:
        print("Please, choose from available variants(10, 20, 50, 100, 200, 500, 1000)")
        change_banknotes()
    con.commit()


def admin_menu():
    try:
        action = int(input("Choose operation:\n1. View available banknotes\n2. Change banknotes\n3. Exit\n: "))
        if action == 1:
            print(check_banknotes())
        elif action == 2:
            change_banknotes()
        elif action == 3:
            sys.exit()
        else:
            print("Wrong input. Please try again")
    except ValueError:
        print("Wrong input. Please try again")


def start(user_name, user_password):
    create_tables()
    insert_tables()
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

con.close()
