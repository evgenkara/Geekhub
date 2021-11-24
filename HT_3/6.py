"""
Створіть ф-цiю, яка буде отримувати рядки на зразок цього, яка оброблює наступні випадки:
-  якщо довжина рядка в діапазонi 30-50 -> прiнтує довжину, кiлькiсть букв та цифр
-  якщо довжина менше 30 -> прiнтує суму всiх чисел та окремо рядок без цифр (лише з буквами)
-  якщо довжина бульше 50 - > ваша фантазiя
"""

def longstr(string):
    letters = []
    nums = []
    for i in string:
        if i.isdigit():
            nums.append(int(i))
        else:
            letters.append(i)
    if len(string) in range(30, 51):
        return f"Length: {len(string)}\nLetters: {len(letters)}\nNumbers: {len(nums)}"
    elif len(string) < 30:
        new_str = "".join(letters)
        return f"Sum of numbers: {sum(nums)}\n{new_str}"
    elif len(string) > 50:
        num_only = "".join(map(str, nums))
        letter_only = "".join(letters)
        return f"Only numbers: {num_only}\nOnly letters: {letter_only}"

inp = input("Enter your string: ")
print(longstr(inp))