"""
Створiть 3 рiзних функцiї (на ваш вибiр). Кожна з цих функцiй повинна повертати якийсь результат. 
Також створiть четверу ф-цiю, яка в тiлi викликає 3 попереднi, обробляє повернутий ними результат та також повертає результат. 
Таким чином ми будемо викликати 1 функцiю, а вона в своєму тiлi ще 3
"""

def sum(a, b):
    return a + b

def dif(a , b):
    return a - b

def mult(a, b):
    return a * b

def res(a, b):
    return sum(a, b) + dif(a, b) + mult(a, b)

inp_1 = int(input("Enter 1st int: "))
inp_2 = int(input("Enter 2nd int: "))
print(res(inp_1, inp_2))