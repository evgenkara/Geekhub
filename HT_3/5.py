"""
Користувач вводить змiннi "x" та "y" з довiльними цифровими значеннями;
Створiть просту умовну конструкцiю(звiсно вона повинна бути в тiлi ф-цiї), пiд час виконання якої буде перевiрятися рiвнiсть змiнних "x" та "y" 
і при нерiвностi змiнних "х" та "у" вiдповiдь повертали рiзницю чисел.
Повиннi опрацювати такi умови:
-  x > y;       вiдповiдь - х бiльше нiж у на z
-  x < y;       вiдповiдь - у бiльше нiж х на z
-  x == y.      вiдповiдь - х дорiвнює z
"""

def equals(x, y):
    if x > y:
        z = x - y
        res = f"{x} > {y} by {z}"
    elif x < y:
        z = y - x
        res = f"{x} < {y} by {z}"
    elif x == y:
        res = f"{x} = {y}"
    return res

num_1 = int(input("Enter 1st num: "))
num_2 = int(input("Enter 2nd num: "))
print(equals(num_1, num_2))