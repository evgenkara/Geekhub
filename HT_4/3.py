"""
Написати функцию < is_prime >, яка прийматиме 1 аргумент - число від 0 до 1000, і яка вертатиме True, 
якщо це число просте, і False - якщо ні.
"""

def is_prime(num):
    if num < 2:
        return False
    elif num == 2:
        return True
    for n in range(2, num):
        if num % n == 0:
            return False
    return True

number = int(input("Enter positive number: "))
print(is_prime(number))