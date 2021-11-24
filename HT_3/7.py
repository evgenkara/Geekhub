"""
Ну і традиційно -> калькулятор :) повинна бути 1 ф-цiя яка б приймала 3 аргументи - один з яких операцiя, яку зробити!
"""

def calc(x, oper, y):
    x, y = int(x), int(y)
    if oper == "+":
        return x + y
    elif oper == "-":
        return x - y
    elif oper == "*":
        return x * y
    elif oper == "/":
        return x / y
    elif oper == "%":
        return x % y
    elif oper == "//":
        return x // y
    elif oper == "**":
        return x ** y
equation = input("Enter your equation: ").split()
print(calc(equation[0], equation[1], equation[2]))