"""
Видозмініть програму так, щоб метод __init__ мався в класі «геометричні фігури» та приймав кольор фігури при створенні
екземпляру, а методи __init__ підкласів доповнювали його та додавали початкові розміри.
"""


class Figure(object):
    def __init__(self, color="white"):
        self.color = color

    def change_color(self):
        new = input("Enter new color: ")
        self.color = new


class Oval(Figure):
    def __init__(self, color, radius):
        self.size = radius
        super(Oval, self).__init__(color)


class Square(Figure):
    def __init__(self, color, side):
        self.size = side
        super().__init__(color)


s = Square("yellow", 14)
print(s.color)
