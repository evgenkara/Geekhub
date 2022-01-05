"""
Створити клас Person, в якому буде присутнім метод __init__ який буде приймати * аргументів, які зберігатиме в
відповідні змінні. Методи, які повинні бути в класі Person - show_age, print_name, show_all_information.
   - Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть атребут profession.
"""


class Person(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def show_age(self):
        try:
            print(f"{self.name} is {self.age} years old")
        except AttributeError:
            print("Person age is not defined")

    def print_name(self):
        try:
            print(f"Hello! My name is {self.name}")
        except AttributeError:
            print("Person name is not defined")

    def show_all_info(self):
        for key in self.__dict__.keys():
            print(f"{key}: {self.__dict__[key]}")


person1 = Person(name="Sasha", age=20, city="Cherkassy")
person1.profession = "Clown"
person1.show_all_info()

person2 = Person(name="Vasya", age=35)
person2.profession = "Builder"
person2.show_age()

