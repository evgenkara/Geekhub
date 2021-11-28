"""
Написати функцію, яка приймає на вхід список і підраховує кількість однакових елементів у ньому.
"""

def count(lis):
    result = {val: lis.count(val) for val in lis}
    return result

values = [1, 3, 3, 1, 1, 1, 1, "g"]
print(count(values))