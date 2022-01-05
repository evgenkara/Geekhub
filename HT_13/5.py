"""
Створіть за допомогою класів та продемонструйте свою реалізацію шкільної бібліотеки(включіть фантазію).
"""

import sys


class Lib(object):
    def __init__(self, *books):
        self.books = list(books)

    def show_books(self):
        print(f"List of available books: {self.books}")

    def add_book(self, book):
        self.books.append(book)
        print("Book added")

    def lend_book(self, book):
        if book in self.books:
            self.books.remove(book)
            print("Book borrowed")
        else:
            print("Can't find required book")


def start():
    lib = Lib("Basic math", "Stories", "A byte of Python")
    while True:
        choice = int(input("Enter Choice:\n1. Check available books\n2. Add book\n3. Borrow book\n4. Exit\n: "))
        if choice == 1:
            lib.show_books()
        elif choice == 2:
            book = input("Choose a book: ")
            lib.add_book(book.strip().capitalize())
        elif choice == 3:
            book = input("Choose a book: ")
            lib.lend_book(book.strip().capitalize())
        elif choice == 4:
            sys.exit()


start()
