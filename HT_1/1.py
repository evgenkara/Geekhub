"""
Write a script which accepts a sequence of comma-separated numbers from user and generate a list and a tuple with those numbers.
"""

lis = [int(num) for num in input("Enter your numbers:").split(",")]
tup = tuple(lis)
print(f"List: {lis}")
print(f"Tuple: {tup}")