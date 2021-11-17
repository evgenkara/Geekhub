"""
Write a script to concatenate N strings.
"""

hexadec = [hex(int(num)).replace("0x", "") for num in input("Enter your numbers: ").split(",")]
print (hexadec)