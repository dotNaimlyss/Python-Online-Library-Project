# main.py
import sqlite3
import json
from item import Book, AudioBook, Magazine, Periodical
from dataStructures import LibraryTree, BorrowerList
from borroweditems import BorrowedItems
from human import Borrower, LibraryAdministrator, Human


def load_data(conn, library_tree, borrower_list, borrowed_items):
    cursor = conn.cursor()

    # Load library items into library_tree and borrowers into borrower_list
    cursor.execute("SELECT * FROM library_items")
    items = cursor.fetchall()
    for item in items:
        item_type = item[8].lower()
        if item_type == "book":
            library_tree.insert(Book(*item))
        elif item_type == "audiobook":
            library_tree.insert(AudioBook(*item))
        elif item_type == "periodical":
            library_tree.insert(Periodical(*item))
        elif item_type == "magazine":
            library_tree.insert(Magazine(*item))

    cursor.execute("SELECT * FROM borrowers")
    borrowers = cursor.fetchall()
    for borrower in borrowers:
        borrower_list.add_borrower(borrower)

    # Load borrowed items into borrowed_items
    cursor.execute("SELECT * FROM borrowed_items")
    borrowed_items_data = cursor.fetchall()
    for borrowed in borrowed_items_data:
        borrower_id = borrowed[0]
        item_id = borrowed[1]
        borrow_date = borrowed[2]
        due_date = borrowed[3]
        borrowed_items.borrow_item(borrower_id, item_id, borrow_date, due_date)

    conn.commit()


def save_data(conn, library_tree, borrower_list, borrowed_items):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM library_items")
    items = library_tree.in_order_traversal()
    for item in items:
        cursor.execute('''INSERT INTO library_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (item.item_id, item.title, item.category, item.language, item.authors,
                        item.year_published, item.due_date, item.isbn, item.type, item.audio_format))

    cursor.execute("DELETE FROM borrowers")
    borrowers = borrower_list.display_all_borrowers()
    for borrower in borrowers:
        cursor.execute("INSERT INTO borrowers VALUES (?, ?, ?, ?, ?, ?)",
                       (borrower[0], borrower[1], borrower[2], borrower[3], borrower[4], borrower[5]))

    cursor.execute("DELETE FROM borrowed_items")
    borrowed_items = borrowed_items.get_all_borrowed_items()
    for borrowed_item in borrowed_items:
        cursor.execute("INSERT INTO borrowed_items VALUES (?, ?, ?, ?)",
                       borrowed_item)

    conn.commit()


def main():
    conn = sqlite3.connect('sola.db')
    library_tree = LibraryTree()
    borrower_list = BorrowerList()
    borrowed_items = BorrowedItems()

    load_data(conn, library_tree, borrower_list, borrowed_items)

    while True:
        user_type = input("Are you a (1) Borrower or (2) Library Administrator? (enter 'q' to quit): ").strip().lower()
        if user_type == 'q':
            save_data(conn, library_tree, borrower_list, borrowed_items)
            break

        if user_type == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            borrower = borrower_list.find_borrower(username)

            if borrower and borrower[4] == password:
                borrower_obj = Borrower(borrower, conn)
                while True:
                    print("\n1. Borrow an item\n2. Return an item\n3. View borrowed items\n4. View fine\n5. Search "
                          "items\n6. Pay Fine\n7. Logout")
                    choice = input("Enter your choice: ").strip()
                    borrower_obj.fine = borrowed_items.calculate_fine(borrower[0])
                    if choice == '1':
                        borrower_obj.borrow_item(library_tree, borrowed_items)
                    elif choice == '2':
                        borrower_obj.return_item(borrowed_items)
                    elif choice == '3':
                        borrower_obj.view_borrowed_items(borrowed_items)
                    elif choice == '4':
                        borrower_obj.view_fine(borrowed_items)
                    elif choice == '5':
                        borrower_obj.search_items(library_tree)
                    elif choice == '6':
                        borrower_obj.pay_fine(borrowed_items)
                    elif choice == '7':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid username or password.")

        elif user_type == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            admin = Human("John", "Doe", username, "Admin123")

            if admin and admin.password == password:
                admin_obj = LibraryAdministrator(admin, conn)
                while True:
                    print(
                        "\n1. Add an item\n2. Remove an item\n3. View all items\n4. View all borrowers\n5. View item details\n6. Locate borrowers with unpaid fines\n7. List borrowed items by borrower\n8. Add a borrower\n9. Update a borrower\n10. Remove a borrower\n11. View a borrower\n12. Logout")
                    choice = input("Enter your choice: ").strip()
                    if choice == '1':
                        admin_obj.add_item(library_tree)
                    elif choice == '2':
                        admin_obj.remove_item(library_tree)
                    elif choice == '3':
                        admin_obj.view_all_items(library_tree)
                    elif choice == '4':
                        admin_obj.view_all_borrowers(borrower_list)
                    elif choice == '5':
                        admin_obj.view_item_details(library_tree)
                    elif choice == '6':
                        admin_obj.locate_borrowers_with_unpaid_fines(borrowed_items)
                    elif choice == '7':
                        admin_obj.list_borrowed_items_by_borrower(borrower_list, borrowed_items)
                    elif choice == '8':
                        admin_obj.add_borrower(borrower_list)
                    elif choice == '9':
                        admin_obj.update_borrower(borrower_list)
                    elif choice == '10':
                        admin_obj.remove_borrower(borrower_list)
                    elif choice == '11':
                        admin_obj.view_borrower(borrower_list)
                    elif choice == '12':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid username or password.")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
