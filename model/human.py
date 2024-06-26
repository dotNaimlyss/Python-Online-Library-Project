# human.py
from item import Book, AudioBook, Magazine, Periodical
from datetime import datetime


class Human:
    def __init__(self, firstname, lastname, username, password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Borrower(Human):
    def __init__(self, borrower, conn):
        super().__init__(borrower[1], borrower[2], borrower[3], borrower[4])
        self.account_number = borrower[0]
        self.borrower = borrower
        self.conn = conn
        self.fine = borrower[5]

    def __getitem__(self, item):
        return self.borrower[item]

    def borrow_item(self, library_tree, borrowed_items):
        if borrowed_items.count_borrowed_items(self.borrower[0]) >= 8:
            print("You cannot borrow more than 8 items.")
            return
        if self.fine > 0:
            print("You have outstanding fines. Please clear them before borrowing new items.")
            return
        title = input("Enter title of the item to borrow: ").strip()
        node = library_tree.search(title)
        if node:
            borrowed_items.borrow_item(self.borrower[0], node.item.item_id)
            print(f"Item '{title}' borrowed successfully.")
        else:
            print(f"No item found with title '{title}'.")

    def return_item(self, borrowed_items):
        id = input("Enter ID of the item to return: ").strip()
        borrowed = borrowed_items.get_borrowed_items(self.borrower[0])
        if borrowed:
            borrowed_items.return_item(self.borrower[0], id)
            print(f"Item '{id}' returned successfully.")
        else:
            print(f"No item found with id '{id}'.")

    def pay_fine(self, borrowed_items):
        self.fine = 0.0
        self.clear_fine(self.borrower[0], borrowed_items)
        print(f"Now your fine is : ${self.fine}")

    def clear_fine(self, borrower_id, borrowed_items):
        borrowed_items_to_remove = []
        for i, (itm_id, borrow_date, due_date) in enumerate(borrowed_items.get_borrowed_items(self.borrower[0])):
            try:
                due_date = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                due_date = datetime.strptime(due_date, '%Y-%m-%d')
            if self.borrower[0] == borrower_id and datetime.now() > due_date:
                borrowed_items_to_remove.append(itm_id)
        for itm_id in borrowed_items_to_remove:
            borrowed_items.return_item(self.borrower[0], itm_id)

    def view_borrowed_items(self, borrowed_items):
        items = borrowed_items.get_borrowed_items(self.borrower[0])
        for item, borrow_date, due_date in items:
            print(f"Item ID: {item}, Borrowed on: {borrow_date}, Must be returned on: {due_date}")

    def view_fine(self, borrowed_items):
        self.fine = borrowed_items.calculate_fine(self.borrower[0])
        print(f"Your total fine is: ${self.fine:.2f}")

    def search_items(self, library_tree):
        print("\nSearch by:\n1. Title\n2. Category\n3. Language\n4. Year Published\n5. Author")
        choice = input("Enter your choice: ").strip()
        query = input("Enter the search query: ").strip()

        if choice == '1':
            results = library_tree.search_by_title(query)
        elif choice == '2':
            results = library_tree.search_by_category(query)
        elif choice == '3':
            results = library_tree.search_by_language(query)
        elif choice == '4':
            results = library_tree.search_by_year(query)
        elif choice == '5':
            results = library_tree.search_by_author(query)
        else:
            print("Invalid choice.")
            return

        if results:
            for item in results:
                print(item)
        else:
            print("No items found.")


class LibraryAdministrator(Human):
    def __init__(self, admin, conn):
        super().__init__(admin.firstname, admin.lastname, admin.username, admin.password)
        self.conn = conn

    def add_item(self, library_tree):
        item_id = input("Enter item ID: ").strip()
        title = input("Enter title: ").strip()
        category = input("Enter category: ").strip()
        language = input("Enter language: ").strip()
        authors = input("Enter authors: ").strip()
        year_published = input("Enter year published: ").strip()
        due_date = input("Enter due date: ").strip()
        isbn = input("Enter ISBN: ").strip()
        item_type = input("Enter item type (Book, AudioBook, Magazine, Periodical): ").strip()
        audio_format = None
        if item_type.lower() == "audiobook":
            audio_format = input("Enter audio format: ").strip()

        if item_type.lower() == "book":
            item = Book(item_id, title, category, language, authors, year_published, due_date, isbn, item_type,
                        audio_format)
        elif item_type.lower() == "audiobook":
            item = AudioBook(item_id, title, category, language, authors, year_published, due_date, isbn, item_type,
                             audio_format)
        elif item_type.lower() == "magazine":
            item = Magazine(item_id, title, category, language, authors, year_published, due_date, isbn, item_type,
                            audio_format)
        elif item_type.lower() == "periodical":
            item = Periodical(item_id, title, category, language, authors, year_published, due_date, isbn, item_type,
                              audio_format)
        else:
            print("Invalid item type.")
            return

        library_tree.insert(item)
        print("Item added successfully.")

    def remove_item(self, library_tree):
        title = input("Enter title of the item to remove: ").strip()
        node = library_tree.search(title)
        if node:
            library_tree.delete(node.item.title)
            print(f"Item '{title}' removed successfully.")
        else:
            print(f"No item found with title '{title}'.")

    def view_item_details(self, library_tree):
        title = input("Enter title of the item to view: ").strip()
        node = library_tree.search(title)
        if node:
            print(node.item)
        else:
            print(f"No item found with title '{title}'.")

    def view_all_items(self, library_tree, page_size=5):
        items = library_tree.in_order_traversal()
        total_pages = (len(items) + page_size - 1) // page_size

        for page in range(total_pages):
            print(f"\nPage {page + 1}/{total_pages}")
            for item in items[page * page_size:(page + 1) * page_size]:
                print(item)
            if page < total_pages - 1:
                cont = input("Enter 'n' to view next page or any other key to stop: ").strip().lower()
                if cont != 'n':
                    break

    def view_all_borrowers(self, borrower_list):
        borrowers = borrower_list.display_all_borrowers()
        for borrower in borrowers:
            print(f"Name: {borrower[1]} {borrower[2]}, Username: {borrower[3]}, Account Number: {borrower[0]}")

    def locate_borrowers_with_unpaid_fines(self, borrowed_items):
        unpaid_borrowers = set()
        for borrower_id, _, _, due_date in borrowed_items.borrowed_items:
            # Try to parse due_date considering it may contain both date and time
            try:
                due_date = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                due_date = datetime.strptime(due_date, '%Y-%m-%d')

            if datetime.now() > due_date:
                unpaid_borrowers.add(borrower_id)

        for borrower_id in unpaid_borrowers:
            print(f"Borrower ID: {borrower_id}")

    def list_borrowed_items_by_borrower(self, borrower_list, borrowed_items):
        for borrower in borrower_list.display_all_borrowers():
            borrower_id = borrower[0]
            print(f"\nBorrower: {borrower[1]} {borrower[2]} (ID: {borrower_id})")
            items = borrowed_items.get_borrowed_items(borrower_id)
            for item in items:
                print(f"  - ID: {item[0]}, Borrowed on: {item[1]}")

    def add_borrower(self, borrower_list):
        firstname = input("Enter borrower's first name: ").strip()
        lastname = input("Enter borrower's last name: ").strip()
        username = input("Enter borrower's username: ").strip()
        password = input("Enter borrower's password: ").strip()
        account_number = borrower_list.generate_account_number()
        fine = 0.0

        borrower = (account_number, firstname, lastname, username, password, fine)
        borrower_list.add_borrower(borrower)
        print("Borrower added successfully.")

    def update_borrower(self, borrower_list):
        username = input("Enter the username of the borrower to update: ").strip()
        borrower = borrower_list.find_borrower(username)
        if borrower:
            firstname = input(f"Enter new first name (current: {borrower[1]}): ").strip() or borrower[1]
            lastname = input(f"Enter new last name (current: {borrower[2]}): ").strip() or borrower[2]
            password = input(f"Enter new password (current: {borrower[4]}): ").strip() or borrower[4]

            updated_borrower = (borrower[0], firstname, lastname, username, password)
            borrower_list.update_borrower(updated_borrower)
            print("Borrower updated successfully.")
        else:
            print(f"No borrower found with username '{username}'.")

    def remove_borrower(self, borrower_list):
        username = input("Enter the username of the borrower to remove: ").strip()
        if borrower_list.remove_borrower(username):
            print("Borrower removed successfully.")
        else:
            print(f"No borrower found with username '{username}'.")

    def view_borrower(self, borrower_list):
        username = input("Enter the username of the borrower to view: ").strip()
        borrower = borrower_list.find_borrower(username)
        if borrower:
            print(f"Name: {borrower[1]} {borrower[2]}, Username: {borrower[3]}, Account Number: {borrower[0]}")
        else:
            print(f"No borrower found with username '{username}'.")
