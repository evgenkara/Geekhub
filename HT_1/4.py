"""
Write a script to concatenate N strings.
"""
n = int(input("Enter number of strings: "))
result = ""
for i in range(0, n):
    string = input(f"Enter string {i+1}: ")
    result += string
print(result)
