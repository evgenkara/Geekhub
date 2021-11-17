"""
Write a script to print out a set containing all the colours from color_list_1 which are not present in color_list_2.
"""

color_list_1 = {color.strip().capitalize() for color in input("Enter 1st color set: ").split(",")}
color_list_2 = {color.strip().capitalize() for color in input("Enter 2nd color set: ").split(",")}
print(color_list_1.difference(color_list_2))