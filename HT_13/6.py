"""
Створіть клас в якому буде атребут який буде рахувати кількість створених екземплярів класів.
"""


class SomeClass(object):
    count = 0

    def __init__(self):
        type(self).count += 1


a = SomeClass()
c = SomeClass()
print(a.count)
