"""
Name: Your Name
Date: 2025
Project: Library Inventory & Borrowing System (Mini Project - Unit 2)
"""

# ------------------------------
# Global Data Storage
# ------------------------------
books = {}          # bookID → book details
borrowed = {}       # student → bookID


# ------------------------------
# Task 2: Add Book
# ------------------------------
def add_book():
    print("\n--- Add New Book ---")
    book_id = input("Enter Book ID: ").strip()
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    copies = int(input("Enter No. of Copies: "))

    books[book_id] = {
        "title": title,
        "author": author,
        "copies": copies
    }

    print(f"\nBook '{title}' added successfully!\n")


# ------------------------------
# Task 3A: View All Books
# ------------------------------
def view_books():
    print("\n------ Library Books ------")
    print("ID\tTitle\t\tAuthor\t\tCopies")
    print("---------------------------------------------")

    for b_id, info in books.items():
        print(f"{b_id}\t{info['title']}\t{info['author']}\t{info['copies']}")

    print()


# ------------------------------
# Task 3B: Search Functions
# ------------------------------
def search_by_id(book_id):
    return books.get(book_id, None)

def search_by_title(title_substring):
    result = []
    for book_id, info in books.items():
        if title_substring.lower() in info['title'].lower():
            result.append((book_id, info))
    return result


def search_book():
    print("\n--- Search Book ---")
    print("1. Search by Book ID")
    print("2. Search by Title (substring)")
    choice = input("Choose option: ")

    if choice == "1":
        book_id = input("Enter Book ID: ").strip()
        result = search_by_id(book_id)

        if result:
            print("\nBook Found:")
            print(result)
        else:
            print("\nBook NOT Found!")

    elif choice == "2":
        title = input("Enter part of title: ")
        results = search_by_title(title)

        if results:
            print("\nMatching Books:")
            for r in results:
                print(r)
        else:
            print("\nNo matching books found.")

    print()


# ------------------------------
# Task 4: Borrow Book
# ------------------------------
def borrow_book():
    print("\n--- Borrow Book ---")
    student = input("Enter Student Name: ")
    book_id = input("Enter Book ID: ")

    if book_id not in books:
        print("Book does not exist!\n")
        return

    if books[book_id]["copies"] > 0:
        borrowed[student] = book_id
        books[book_id]["copies"] -= 1
        print(f"\nBook borrowed successfully by {student}\n")
    else:
        print("\nNo copies available!\n")


# ------------------------------
# Task 5: Return Book
# ------------------------------
def return_book():
    print("\n--- Return Book ---")
    student = input("Enter Student Name: ")
    book_id = input("Enter Book ID: ")

    if student in borrowed and borrowed[student] == book_id:
        books[book_id]["copies"] += 1
        borrowed.pop(student)
        print("\nBook returned successfully!\n")
    else:
        print("\nInvalid return attempt!\n")

    # List comprehension to show borrowed list
    borrowed_list = [f"{stu} -> {bk}" for stu, bk in borrowed.items()]
    print("Borrowed List:", borrowed_list, "\n")


# ------------------------------
# Menu + Loop (Task 1 & 6)
# ------------------------------
def menu():
    while True:
        print("\n============ Library Management System ============")
        print("1. Add Book")
        print("2. View Books")
        print("3. Search Book")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Exit")
        print("===================================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            borrow_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            print("Exiting the program... Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")


# Run Program
menu()
