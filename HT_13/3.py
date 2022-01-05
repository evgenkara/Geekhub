"""
Напишіть програму, де клас «геометричні фігури» (figure) містить властивість color з початковим значенням white і метод
для зміни кольору фігури, а його підкласи «овал» (oval) і «квадрат» (square) містять методи __init__ для завдання
початкових розмірів об'єктів при їх створенні.
"""


class Figure(object):
    color = "white"

    def change_color(self):
        new = input("Enter new color: ")
        self.color = new


class Oval(Figure):
    def __init__(self, radius):
        self.size = radius


class Square(Figure):
    def __init__(self, side):
        self.size = side
