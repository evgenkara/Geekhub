"""
Написати скрипт, який конкатенує всі елементи в списку і виведе їх на екран.
"""

values = [1, 2, 'test', 10, 'foo']
result = "".join(map(str, values))
print(result)