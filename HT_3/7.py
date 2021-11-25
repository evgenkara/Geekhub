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

num_1 = input("Enter 1st number: ").strip()
num_2 = input("Enter 2nd number: ").strip()
operation = input("Enter operation: ").strip()
print(calc(num_1, operation, num_2))
