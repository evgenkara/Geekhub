"""
Написати функцiю season, яка приймає один аргумент — номер мiсяця (вiд 1 до 12), 
яка буде повертати пору року, якiй цей мiсяць належить (зима, весна, лiто або осiнь)
"""

def season(month):
    if month in range(1,3) or month == 12:
        return "Winter"
    elif month in range(3, 6):
        return "Spring"
    elif month in range(6, 9):
        return "Summer"
    elif month in range(9,12):
        return "Autumn"
    else:
        return "Wrong input"

inp = int(input("Enter month(1-12): "))
print(season(inp))