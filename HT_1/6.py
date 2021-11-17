"""
Write a script to check whether a specified value is contained in a group of values.
"""

val = input("Enter your value: ").strip()
values = [value.strip() for value in input("Enter the group of values: ").split(",")]
print(val in values)