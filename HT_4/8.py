"""
Написати функцію, яка буде реалізувати логіку циклічного зсуву елементів в списку. Тобто, функція приймає два аргументи: список і величину зсуву 
(якщо ця величина додатня - пересуваємо з кінця на початок, якщо від'ємна - навпаки - пересуваємо елементи з початку списку в його кінець).
"""

def move(lis, shift):
    if shift >= 0:
        for i in range(shift):
            lis.insert(0, lis.pop())
    elif shift < 0:
        for i in range(abs(shift)):
            lis.append(lis.pop(0))
    return lis

values = [1, 2, 3, 4, 5]
print(move(values, shift = -2))