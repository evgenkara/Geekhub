"""
Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
   - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
   - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну цифру;
   - щось своє :)
Якщо якийсь із параментів не відповідає вимогам - породити виключення із відповідним текстом.
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
        raise LoginException("Password must contain at least 1 number")
    elif not any(char.isupper() for char in username):
        raise LoginException("Username must contain at least 1 uppercase letter")

validate("user1", "passwordnumber1")