"""
Написати функцію < square > , яка прийматиме один аргумент - сторону квадрата, 
і вертатиме 3 значення (кортеж): периметр квадрата, площа квадрата та його діагональ.
"""

import math

def square(side):
    perim = 4 * side
    area = side**2
    diag = round(side * math.sqrt(2), 2)
    return (perim, area, diag)

a = int(input("Enter side of a square: "))
print(square(a))