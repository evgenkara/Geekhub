"""
Написати функцію < fibonacci >, яка приймає один аргумент і виводить всі числа Фібоначчі, що не перевищують його.
"""

def fibonacci(num):
    values = []
    val_1, val_2 = 0, 1
    values.append(val_1)
    while val_2 < num:
        values.append(val_2)
        val_1, val_2 = val_2, val_1 + val_2
    print(values)
    return values

number = int(input("Enter positive number: "))
fibonacci(number)