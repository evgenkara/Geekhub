"""
Створіть клас в якому буде атребут який буде рахувати кількість створених екземплярів класів.
"""


class SomeClass(object):
    count = 0

    def __init__(self):
        self.__class__.count += 1


a = SomeClass()
c = SomeClass()
print(a.count)
