"""
Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї функції.
P.S. Повинен вертатись генератор.
"""


def myrange(start, stop, step = 1):
    if step > 0:
        while start < stop:
            yield start
            start += step
    if step < 0:
        while start > stop:
            yield start
            start += step
    elif step == 0:
        raise ValueError

ran = myrange(15, 0, -1)
for i in ran:
    print(i)
