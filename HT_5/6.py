"""
Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї функції.
P.S. Повинен вертатись генератор.
"""


def myrange(start, stop, step = 1):
    r = iter([start])
    if step > 0:
        while start < stop:
            yield start
            start += step
    if step < 0:
        while start > stop:
            yield start
            start += step

ran = myrange(15, 0, -5)
print(ran)
for i in ran:
    print(i)