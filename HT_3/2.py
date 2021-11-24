"""
Користувачем вводиться початковий і кінцевий рік. 
Створити цикл, який виведе всі високосні роки в цьому проміжку (границі включно).
"""

year_1 = int(input("Enter year 1: "))
year_2 = int(input("Enter year 2: "))
leap = []

for year in range(year_1, year_2 + 1):
    if year % 400 == 0:
        leap.append(year)
    elif year % 4 == 0 and year % 100 != 0:
        leap.append(year)

print(f"Leap years from {year_1} to {year_2}: {leap}")