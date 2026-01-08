# Test your code:
# This is just an example. You should test a lot more than this.

from P1 import LibraryItem, Book, TextBook, Magazine

book = Book("Harry Potter", "B001", "J.K. Rowling")
book.set_pages_count(350)

textbook = TextBook("Physics", "T101", "Serway", "Science", 12)
textbook.set_pages_count(500)

mag = Magazine("Time", "M202", 45)

book.check_out()
textbook.check_out()

book.display_info()
print()
textbook.display_info()
print()
mag.display_info()