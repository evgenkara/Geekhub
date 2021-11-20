"""
Написати скрипт, який залишить в словнику тільки пари із унікальними значеннями (дублікати значень - видалити). Словник для
роботи захардкодити свій.
"""

dict_1 = {1 : "a", 2 : "b", 3 : "a", 4 : "d", 5 : "b"}
result = {}
for key, val in dict_1.items():
    if val not in result.values():
        result[key] = val

print(result)