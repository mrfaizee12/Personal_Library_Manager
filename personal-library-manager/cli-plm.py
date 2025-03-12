import json
import os
import time
from colorama import Fore, Style, init

# Initialize Colorama for colorful text
init(autoreset=True)

LIBRARY_FILE = "library.json"

# Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Initialize Library
library = load_library()

# Cool Loading Effect
def loading_effect(msg="Processing"):
    print(Fore.CYAN + msg, end="", flush=True)
    for _ in range(3):
        time.sleep(0.5)
        print(Fore.CYAN + ".", end="", flush=True)
    print("\n")

# Display Main Menu
def display_menu():
    print(Fore.MAGENTA + Style.BRIGHT + "\n📚 WELCOME TO YOUR PERSONAL LIBRARY MANAGER 📚\n")
    print(Fore.YELLOW + "1️⃣ ➕ Add a Book")
    print(Fore.YELLOW + "2️⃣ ❌ Remove a Book")
    print(Fore.YELLOW + "3️⃣ 🔍 Search for a Book")
    print(Fore.YELLOW + "4️⃣ 📖 Display All Books")
    print(Fore.YELLOW + "5️⃣ 📊 View Statistics")
    print(Fore.YELLOW + "6️⃣ 🚪 Exit")

# Add a Book
def add_book():
    print(Fore.GREEN + "\n📖 ADD A NEW BOOK 📖")
    title = input(Fore.CYAN + "Enter Book Title: ")
    author = input(Fore.CYAN + "Enter Author Name: ")
    year = input(Fore.CYAN + "Enter Publication Year: ")
    genre = input(Fore.CYAN + "Enter Genre: ")
    read_status = input(Fore.CYAN + "Have you read this book? (yes/no): ").strip().lower()

    book = {
        "title": title,
        "author": author,
        "year": int(year),
        "genre": genre,
        "read": True if read_status == "yes" else False
    }

    library.append(book)
    save_library(library)
    loading_effect("Saving Book")
    print(Fore.GREEN + f"✅ '{title}' has been added successfully!\n")

# Remove a Book
def remove_book():
    print(Fore.RED + "\n🗑 REMOVE A BOOK 🗑")
    title = input(Fore.CYAN + "Enter the book title to remove: ")

    global library
    new_library = [book for book in library if book["title"].lower() != title.lower()]

    if len(new_library) < len(library):
        library = new_library
        save_library(library)
        loading_effect("Removing Book")
        print(Fore.RED + f"❌ '{title}' has been removed successfully!\n")
    else:
        print(Fore.YELLOW + "⚠️ Book not found in the library!\n")

# Search for a Book
def search_book():
    print(Fore.BLUE + "\n🔎 SEARCH FOR A BOOK 🔎")
    search_type = input(Fore.CYAN + "Search by Title (T) or Author (A)? ").strip().lower()
    query = input(Fore.CYAN + "Enter search query: ").strip().lower()

    results = [book for book in library if query in book["title"].lower() or query in book["author"].lower()]

    if results:
        print(Fore.GREEN + "\n📚 Matching Books:")
        for book in results:
            status = "✅ Read" if book["read"] else "❌ Unread"
            print(Fore.YELLOW + f"📖 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        print(Fore.RED + "⚠️ No matching books found!\n")

# Display All Books
def display_books():
    print(Fore.BLUE + "\n📚 YOUR LIBRARY COLLECTION 📚")
    if library:
        for i, book in enumerate(library, 1):
            status = "✅ Read" if book["read"] else "❌ Unread"
            print(Fore.YELLOW + f"{i}. 📖 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        print(Fore.RED + "⚠️ Your library is empty!\n")

# Display Statistics
def display_statistics():
    print(Fore.CYAN + "\n📊 LIBRARY STATISTICS 📊")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0

    print(Fore.GREEN + f"📚 Total Books: {total_books}")
    print(Fore.GREEN + f"✅ Books Read: {read_books} ({percentage_read:.2f}%)")

# Main Loop
while True:
    display_menu()
    choice = input(Fore.CYAN + "Enter your choice (1-6): ").strip()

    if choice == "1":
        add_book()
    elif choice == "2":
        remove_book()
    elif choice == "3":
        search_book()
    elif choice == "4":
        display_books()
    elif choice == "5":
        display_statistics()
    elif choice == "6":
        loading_effect("Saving and Exiting")
        print(Fore.MAGENTA + "📖 Library saved successfully. Goodbye! 🚀")
        break
    else:
        print(Fore.RED + "⚠️ Invalid choice! Please enter a valid option.\n")
