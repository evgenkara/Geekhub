"""
Вводиться число. Якщо це число додатне, знайти його квадрат, якщо від'ємне, збільшити його на 100, 
якщо дорівнює 0, не змінювати.
 """

def do_smth(num):
    if num > 0:
        num **= 2
    elif num < 0:
        num += 100
    elif num == 0:
        pass
    return f"Result: {num}"

number = int(input("Enter your number: "))
print(do_smth(number))