"""
На основі попередньої функції створити наступний кусок кода:
   а) створити список із парами ім'я/пароль різноманітних видів (орієнтуйтесь по правилам своєї функції) - як валідні, так і ні;
   б) створити цикл, який пройдеться по цьому циклу і, користуючись валідатором, перевірить ці дані і надрукує для кожної пари значень відповідне повідомлення
"""

class LoginException(Exception):
    pass

def validate(username, password):
    if len(username) < 3:
        raise LoginException("Username is too short")
    elif len(username) > 50:
        raise LoginException("Username is too long")
    elif len(password) < 8:
        raise LoginException("Password is too short")
    elif  password.isalpha() == True:
        raise LoginException("Password must have at least 1 digit")
    elif not any(char.isupper() for char in username):
        raise LoginException("Username must contain at least 1 uppercase letter")

def check(username, password, exc = "OK"):
    try:
        validate(username, password)
        print(f"Name: {username}\nPassword: {password}\nStatus: {exc}\n-----")
    except LoginException as exc:
        print(f"Name: {username}\nPassword: {password}\nStatus: {exc}\n-----")

users = [["Us", "password1"], ["User2", "password2"], ["User3", "mypassword"], ["user4", "password4"]]
for data in users:
    check(data[0], data[1])