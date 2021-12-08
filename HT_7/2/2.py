def print_blocks(myfile, num):
    with open(myfile, "r") as file:
        old_file_position = file.tell()
        file.seek(0, 2)
        size = file.tell()
        if num * 3 <= size:
            file.seek(old_file_position)
            first = file.read(num)
            center = size // 2
            file.seek(center - num // 2)
            mid = file.read(num)
            file.seek(size - num)
            end = file.read(num)
            print([first, mid, end])
        else:
            print("Can't take more symbols than available")


print_blocks("test.txt", 3)
print_blocks("test2.txt", 4)
