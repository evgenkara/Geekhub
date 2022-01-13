"""
Переписати останню версію банкомата з використанням ООП
"""


import requests
import sqlite3
import sys


class BankException(Exception):
    pass


con = sqlite3.connect("ATM.db")
cur = con.cursor()


class Rates(object):
    @staticmethod
    def get_rates():
        r = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
        for j in r.json():
            print(f"{j['ccy']}: {round(float(j['buy']), 2)} {j['base_ccy']}  {round(float(j['sale']), 2)} "
                  f"{j['base_ccy']} ")


class DataBase(object):
    def __init__(self, user_name):
        self.username = user_name

    @staticmethod
    def create_tables():
        cur.execute('''CREATE TABLE IF NOT EXISTS users 
                        (id integer PRIMARY KEY, username text, password text, 
                        is_incasator BOOLEAN NOT NULL CHECK (is_incasator IN (0,1)), UNIQUE (username)) ''')
        cur.execute('''CREATE TABLE IF NOT EXISTS balance
                        ( id integer PRIMARY KEY, 
                        username text, 
                        user_balance integer, 
                        FOREIGN KEY (id) REFERENCES users(id))''')
        cur.execute('''CREATE TABLE IF NOT EXISTS users_transactions (id integer, username text, operation text, 
                        before integer, after integer, FOREIGN KEY (id) REFERENCES users(id))''')
        cur.execute('''CREATE TABLE IF NOT EXISTS banknotes (key integer PRIMARY KEY, 
                        banknote integer, amount integer )''')
        con.commit()

    @staticmethod
    def insert_tables():
        cur.execute('''INSERT OR IGNORE INTO users VALUES (1, "user1", "user1", 0), (2, "user2", "user2", 0), 
                    (3, "admin", "admin", 1)''')
        cur.execute("INSERT OR IGNORE INTO balance VALUES (1, 'user1', 10000), (2, 'user2', 8800), (3, 'admin', 20000)")
        cur.execute('''INSERT OR IGNORE INTO banknotes VALUES (1, 1000, 10), (2, 500, 8), (3, 200, 5), 
                    (4, 100, 10), (5, 50, 8), (6, 20, 5), (7, 10, 10)''')
        con.commit()

    def add_transaction(self, old_bal, new_bal):
        if new_bal > old_bal:
            transaction = "deposit"
        else:
            transaction = "withdraw"
        cur.execute("SELECT id FROM users WHERE username = ?", (self.username,))
        user_id = cur.fetchone()[0]
        cur.execute(f"INSERT INTO users_transactions VALUES (?, ?, ?, ?, ?)", (user_id, self.username,
                                                                               transaction, old_bal, new_bal))
        con.commit()

    @staticmethod
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


class Person(object):
    def __init__(self, user_name, user_password):
        self.username = user_name
        self.password = user_password


class User(Person):

    def check_balance(self):
        cur.execute("SELECT user_balance FROM balance WHERE username = ?", (self.username,))
        balance = cur.fetchone()[0]
        return f"Current balance: {str(balance)}"

    def replenish(self):
        dep = int(input("How much money do you want to deposit?\n: "))
        cur.execute("SELECT user_balance FROM balance WHERE username = ?", (self.username,))
        balance = cur.fetchone()[0]
        if dep > 0:
            new_balance = balance + dep
            cur.execute(''' UPDATE balance SET user_balance = ? WHERE username = ?''', (new_balance, self.username))
            con.commit()
            return balance, new_balance
        else:
            print("Wrong input")

    def withdraw(self):
        bank_sum = 0
        cur.execute("SELECT banknote, amount FROM banknotes")
        for bank in cur.fetchall():
            bank_sum += bank[0] * bank[1]
        cur.execute("SELECT user_balance FROM balance WHERE username = ?", (self.username,))
        currency = cur.fetchone()[0]
        wit = int(input(f"Now in stock: {bank_sum}\nHow much money do you want to withdraw?\n: "))
        if wit > 0 and wit % 10 == 0:
            if wit <= bank_sum:
                balance_new = currency - wit
                cur.execute("UPDATE balance SET user_balance = ? WHERE username = ?", (balance_new, self.username))
                try:
                    print(DataBase.withdraw_balance(wit))
                except BankException:
                    w = int(input("Not enough banknotes in ATM. Please, enter another value\n: "))
                    print(DataBase.withdraw_balance(w))
                return currency, balance_new
            else:
                print(f"Not enough money in the ATM. Now in stock: {bank_sum}")
        else:
            print("Please enter positive amount which is multiple by zero")
            self.withdraw()
        con.commit()

    def menu(self):
        db = DataBase(self.username)
        try:
            action = int(input("Choose operation:\n1. Check balance\n2. Replenish balance\n3. Withdraw money\n"
                               "4. Check exchange rates\n5. Exit\n: "))
            if action == 1:
                print(self.check_balance())
            elif action == 2:
                rep = self.replenish()
                if rep:
                    db.add_transaction(rep[0], rep[1])
            elif action == 3:
                wit = self.withdraw()
                if wit:
                    db.add_transaction(wit[0], wit[1])
            elif action == 4:
                Rates.get_rates()
            elif action == 5:
                sys.exit()
            else:
                print("Wrong input")
        except ValueError:
            print("Wrong input. Please try again")


class Incasator(Person):

    @staticmethod
    def check_banknotes():
        cur.execute("SELECT banknote, amount FROM banknotes")
        result = {bank[0]: bank[1] for bank in cur.fetchall()}
        return result

    def change_banknotes(self):
        choice = input("Choose banknote: ")
        cur.execute("SELECT * FROM banknotes WHERE banknote = ?", (choice,))
        if cur.fetchone():
            new = int(input("Enter new amount: "))
            if new >= 0:
                cur.execute("UPDATE banknotes SET amount = ? WHERE banknote = ?", (new, choice))
            else:
                print("Can't change amount to negative. Please, try again")
                self.change_banknotes()
        else:
            print("Please, choose from available variants(10, 20, 50, 100, 200, 500, 1000)")
            self.change_banknotes()
        con.commit()

    def menu(self):
        try:
            action = int(input("Choose operation:\n1. View available banknotes\n2. Change banknotes\n"
                               "3. Check exchange rates\n4. Exit\n: "))
            if action == 1:
                print(self.check_banknotes())
            elif action == 2:
                self.change_banknotes()
            elif action == 3:
                Rates.get_rates()
            elif action == 4:
                sys.exit()
            else:
                print("Wrong input. Please try again")
        except ValueError:
            print("Wrong input. Please try again")


class Auth(object):
    def __init__(self, user_name, user_password):
        self.user_name = user_name
        self.user_password = user_password

    @staticmethod
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

    def validate(self):
        cur.execute("SELECT is_incasator FROM users WHERE username = ? AND password = ?",
                    (self.user_name, self.user_password))
        user = cur.fetchone()
        if user:
            if 1 in user:
                return Incasator(self.user_name, self.user_password)
            else:
                return User(self.user_name, self.user_password)


class ATM(object):
    def start(self, user_name, user_password):
        val = Auth(user_name, user_password).validate()
        if val:
            val.menu()
            self.start(user_name, user_password)
        else:
            reg = int(input("User doesn't exist. Do you want to register?\n1. Yes\n2. No\n: "))
            if reg == 1:
                Auth.register()
            else:
                sys.exit()
            self.start(user_name, user_password)


username = input("Enter username: ")
password = input("Enter password: ")
DataBase.create_tables()
DataBase.insert_tables()
ATM().start(username, password)

con.close()
