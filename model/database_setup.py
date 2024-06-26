import sqlite3
from datetime import datetime, timedelta
import random
from faker import Faker

# Initialize Faker
fake = Faker()

def setup_database():
    conn = sqlite3.connect('sola.db')
    c = conn.cursor()

    # Create table for library items
    c.execute('''CREATE TABLE IF NOT EXISTS library_items (
                 item_id TEXT PRIMARY KEY,
                 title TEXT,
                 category TEXT,
                 language TEXT,
                 authors TEXT,
                 year_published TEXT,
                 due_date TEXT,
                 isbn TEXT,
                 type TEXT,
                 audio_format TEXT
                 )''')

    # Create table for borrowers
    c.execute('''CREATE TABLE IF NOT EXISTS borrowers (
                 account_number INTEGER PRIMARY KEY,
                 firstname TEXT,
                 lastname TEXT,
                 username TEXT UNIQUE,
                 password TEXT,
                 fine REAL
                 )''')

    # Create table for borrowed items
    c.execute('''CREATE TABLE IF NOT EXISTS borrowed_items (
                 borrower_id INTEGER,
                 item_id TEXT,
                 borrow_date TEXT,
                 due_date TEXT,
                 FOREIGN KEY (borrower_id) REFERENCES borrowers (account_number),
                 FOREIGN KEY (item_id) REFERENCES library_items (item_id)
                 )''')

    conn.commit()
    conn.close()

def insert_dummy_data():
    conn = sqlite3.connect('sola.db')
    c = conn.cursor()

    # Helper functions
    def random_date(start, end):
        return start + timedelta(
            seconds=random.randint(0, int((end - start).total_seconds())))

    # Sample data
    titles_books = [
        "The Great Gatsby", "1984", "To Kill a Mockingbird", "The Catcher in the Rye",
        "The Lord of the Rings", "Pride and Prejudice", "The Hobbit", "Moby Dick",
        "War and Peace", "Great Expectations"
    ]

    titles_periodicals = [
        "Nature Journal", "Science Magazine", "The Lancet", "New England Journal of Medicine",
        "IEEE Transactions on Computers", "ACM Computing Surveys", "Journal of the ACM",
        "Cell", "The Astrophysical Journal", "Journal of Clinical Oncology"
    ]

    titles_magazines = [
        "National Geographic", "TIME", "The New Yorker", "Vogue",
        "Forbes", "People", "Sports Illustrated", "Popular Science",
        "The Economist", "Wired"
    ]

    titles_audiobooks = [
        "Becoming", "The Power of Habit", "Sapiens", "Educated",
        "Harry Potter and the Sorcerer's Stone", "The Subtle Art of Not Giving a F*ck",
        "Atomic Habits", "The Four Agreements", "Where the Crawdads Sing", "The Silent Patient"
    ]

    authors = [
        "F. Scott Fitzgerald", "George Orwell", "Harper Lee", "J.D. Salinger",
        "J.R.R. Tolkien", "Jane Austen", "Herman Melville", "Leo Tolstoy",
        "Charles Dickens", "Stephen King", "Margaret Atwood", "Ernest Hemingway"
    ]

    categories_books = ["Fiction", "Classics", "Historical Fiction", "Science Fiction", "Fantasy"]
    categories_periodicals = ["Science", "Medical", "Engineering", "Technology", "Biology"]
    categories_magazines = ["Education", "Lifestyle", "Business", "Technology", "Health"]
    categories_audiobooks = ["Biography", "Self-Help", "History", "Fiction", "Mystery"]

    languages = ["English", "Spanish", "French", "German", "Chinese"]
    audio_formats = ["MP3", "WAV", "AAC"]

    # Generate dummy data for library items
    library_items = []

    # Books
    for i in range(1, 26):
        item_id = f"book{i:03}"
        title = random.choice(titles_books)
        category = random.choice(categories_books)
        language = random.choice(languages)
        author = random.choice(authors)
        year_published = random.randint(1950, 2023)
        due_date = None
        isbn = f"978-3-{random.randint(1000000, 9999999)}"
        item_type = "book"
        audio_format = None

        library_items.append((item_id, title, category, language, author, year_published, due_date, isbn, item_type, audio_format))

    # Periodicals
    for i in range(1, 26):
        item_id = f"periodical{i:03}"
        title = random.choice(titles_periodicals)
        category = random.choice(categories_periodicals)
        language = random.choice(languages)
        author = random.choice(authors)
        year_published = random.randint(2000, 2023)
        due_date = None
        isbn = None
        item_type = "periodical"
        audio_format = None

        library_items.append((item_id, title, category, language, author, year_published, due_date, isbn, item_type, audio_format))

    # Magazines
    for i in range(1, 26):
        item_id = f"magazine{i:03}"
        title = random.choice(titles_magazines)
        category = random.choice(categories_magazines)
        language = random.choice(languages)
        author = random.choice(authors)
        year_published = random.randint(2000, 2023)
        due_date = None
        isbn = None
        item_type = "magazine"
        audio_format = None

        library_items.append((item_id, title, category, language, author, year_published, due_date, isbn, item_type, audio_format))

    # Audiobooks
    for i in range(1, 26):
        item_id = f"audiobook{i:03}"
        title = random.choice(titles_audiobooks)
        category = random.choice(categories_audiobooks)
        language = random.choice(languages)
        author = random.choice(authors)
        year_published = random.randint(2000, 2023)
        due_date = None
        isbn = f"978-3-{random.randint(1000000, 9999999)}"
        item_type = "audiobook"
        audio_format = random.choice(audio_formats)

        library_items.append((item_id, title, category, language, author, year_published, due_date, isbn, item_type, audio_format))

    # Insert the data into the library_items table
    c.executemany('''INSERT INTO library_items (item_id, title, category, language, authors, year_published, due_date, isbn, type, audio_format)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', library_items)
    conn.commit()

    # Generate and insert dummy data for borrowers
    borrowers = []
    for i in range(1, 21):
        account_number = i
        firstname = fake.first_name()
        lastname = fake.last_name()
        username = f"user{i}"
        password = "password123"
        fine = 0.0

        borrowers.append((account_number, firstname, lastname, username, password, fine))

    c.executemany('''INSERT INTO borrowers (account_number, firstname, lastname, username, password, fine )
                     VALUES (?, ?, ?, ?, ?, ?)''', borrowers)
    conn.commit()

    # Generate and insert dummy data for borrowed items
    borrowed_items = []
    for borrower in borrowers:
        borrower_id = borrower[0]
        num_borrowed_items = random.randint(1, 8)  # Each borrower has 1 to 8 borrowed items
        borrowed_item_ids = random.sample([item[0] for item in library_items],
                                          num_borrowed_items)  # Randomly select borrowed items

        for item_id in borrowed_item_ids:
            borrow_date = datetime.now() - timedelta(
                days=random.randint(1, 30))  # Random borrow date in the past 30 days
            due_date = borrow_date + timedelta(days=random.randint(1, 30))  # Random due date

            borrowed_items.append(
                (borrower_id, item_id, borrow_date.strftime("%Y-%m-%d"), due_date.strftime("%Y-%m-%d")))


    c.executemany('''INSERT INTO borrowed_items (borrower_id, item_id, borrow_date, due_date)
                     VALUES (?, ?, ?, ?)''', borrowed_items)
    conn.commit()

    # Close the database connection
    conn.close()

def load_data():
    conn = sqlite3.connect('sola.db')
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM library_items")
        library_items = c.fetchall()
        print("Library Items:")
        for item in library_items:
            print(item)

        c.execute("SELECT * FROM borrowers")
        borrowers = c.fetchall()
        print("\nBorrowers:")
        for borrower in borrowers:
            print(borrower)

        c.execute("SELECT * FROM borrowed_items")
        borrowed_items = c.fetchall()
        print("\nBorrowed Items:")
        for borrowed in borrowed_items:
            print(borrowed)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()
    insert_dummy_data()
    load_data()
