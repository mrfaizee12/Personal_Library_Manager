import streamlit as st
import json
import os

# File to store library data
LIBRARY_FILE = "library.txt"

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

# Initialize library
library = load_library()

# Dark Mode Toggle
dark_mode = st.sidebar.checkbox('🌓 Dark Mode', value=False)

# Dynamic CSS based on mode
if dark_mode:
    css = """
    <style>
        .stApp {
            background-color: #121212;
            color: white;
        }
        [data-testid="stSidebar"] {
            background-color: #242424 !important;
        }
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        [data-testid="stSidebar"] .stSelectbox div[aria-selected="true"] {
            background-color: #64b5f6 !important;
            color: #121212 !important;
            font-weight: bold;
        }
        label, .stTextInput label, .stNumberInput label, .stRadio label, .stSelectbox label {
            color: #64b5f6 !important;
        }
        .stButton button {
            background-color: #ff7e5f !important;
            color: white !important;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        .stButton button:hover {
            background-color: #e76f51 !important;
        }
    </style>
    """
else:
    css = """
    <style>
        .stApp {
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            color: black;
        }
        [data-testid="stSidebar"] {
            background-color: white !important;
            color: black !important;
        }
        .stButton button {
            background-color: #ff7e5f !important;
            color: white !important;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        .stButton button:hover {
            background-color: #e76f51 !important;
        }
    </style>
    """

st.markdown(css, unsafe_allow_html=True)

# App Title
st.markdown("<h1 style='text-align: center;'>📚 Personal Library Manager</h1>", unsafe_allow_html=True)

# Navigation Menu
menu = ["📖 Add Book", "❌ Remove Book", "🔍 Search Book", "📚 Display All Books", "📊 Statistics", "🚪 Exit"]
choice = st.sidebar.selectbox("Select an option", menu)

# Add a Book
if choice == "📖 Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Enter Book Title")
    author = st.text_input("Enter Author")
    year = st.number_input("Enter Publication Year", min_value=0, step=1)
    genre = st.text_input("Enter Genre")
    read_status = st.radio("Have you read this book?", ("Yes", "No"))
    
    if st.button("Add Book"):
        book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": True if read_status == "Yes" else False
        }
        library.append(book)
        save_library(library)
        st.success(f"📘 '{title}' added successfully!")

# Remove a Book
elif choice == "❌ Remove Book":
    st.subheader("🗑 Remove a Book")
    book_titles = [book["title"] for book in library]
    book_to_remove = st.selectbox("Select a book to remove", book_titles) if book_titles else None
    
    if st.button("Remove Book") and book_to_remove:
        library = [book for book in library if book["title"] != book_to_remove]
        save_library(library)
        st.success(f"📕 '{book_to_remove}' removed successfully!")

# Search for a Book
elif choice == "🔍 Search Book":
    st.subheader("🔎 Search for a Book")
    search_option = st.radio("Search by:", ("Title", "Author"))
    search_query = st.text_input("Enter search query")
    
    if st.button("Search"):
        results = [book for book in library if search_query.lower() in book[search_option.lower()].lower()]
        if results:
            for book in results:
                st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("No matching books found!")

# Display All Books
elif choice == "📚 Display All Books":
    st.subheader("📘 Your Library")
    if library:
        for book in library:
            st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.warning("Library is empty!")

# Display Statistics
elif choice == "📊 Statistics":
    st.subheader("📈 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0

    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"📖 **Books Read:** {read_books} ({percentage_read:.2f}%)")

# Exit
elif choice == "🚪 Exit":
    st.subheader("👋 Exiting...")
    st.warning("Close the app window to exit.")
