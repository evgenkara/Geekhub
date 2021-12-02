"""
Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї функції.
P.S. Повинен вертатись генератор.
"""

def myrange(start, stop = None, step = 1):
    if stop == None:
        stop = start; start = 0
    if step > 0:
        if start > stop:
            raise ValueError
        else:
            while start < stop:
                yield start
                start += step
    if step < 0:
        if start < stop:
            raise ValueError
        else:
            while start > stop:
                yield start
                start += step
    elif step == 0:
        raise ValueError

ran = myrange(30)
for i in ran:
    print(i)
