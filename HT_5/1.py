"""
Створіть функцію, всередині якої будуть записано список із п'яти користувачів (ім'я та пароль).
Функція повинна приймати три аргументи: два - обов'язкових (<username> та <password>) і третій - необов'язковий параметр <silent> (значення за замовчуванням - <False>).
Логіка наступна:
    -якщо введено коректну пару ім'я/пароль - вертається <True>;
    -якщо введено неправильну пару ім'я/пароль і <silent> == <True> - функція вертає <False>, інакше (<silent> == <False>) - породжується виключення LoginException
"""

class LoginException(Exception):
    pass

def validate(username, password, silent = False):
    users = [["user1", "1111"],["user2", "2222"], ["user3", "3333"], ["user4", "4444"], ["user5", "5555"]]
    data = [username, password]
    if data in users:
        return True
    elif data not in users and silent == True:
        return False
    else:
        raise LoginException()

print(validate("user1", "2222"))