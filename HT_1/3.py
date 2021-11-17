"""
Write a script to sum of the first n positive integers.
"""

n = int(input("Enter positive number: "))
sum = 0
if n >= 0:
    for i in range (0, n+1):
        sum += i
    print(f"Sum of the first {n} positive integers = {sum}")
else:
    print("Please enter POSITIVE number!")