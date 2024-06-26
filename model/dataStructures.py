class TreeNode:
    def __init__(self, item):
        self.item = item
        self.left = None
        self.right = None

class LibraryTree:
    def __init__(self):
        self.root = None

    def insert(self, item):
        if self.root is None:
            self.root = TreeNode(item)
        else:
            self._insert(self.root, item)

    def _insert(self, node, item):
        if item.title < node.item.title:
            if node.left is None:
                node.left = TreeNode(item)
            else:
                self._insert(node.left, item)
        else:
            if node.right is None:
                node.right = TreeNode(item)
            else:
                self._insert(node.right, item)

    def search(self, title):
        return self._search(self.root, title)

    def _search(self, node, title):
        if node is None or node.item.title == title:
            return node
        if title < node.item.title:
            return self._search(node.left, title)
        return self._search(node.right, title)

    def delete(self, title):
        self.root, _ = self._delete(self.root, title)

    def _delete(self, node, title):
        if node is None:
            return node, None
        if title < node.item.title:
            node.left, deleted_node = self._delete(node.left, title)
        elif title > node.item.title:
            node.right, deleted_node = self._delete(node.right, title)
        else:
            deleted_node = node
            if node.left is None:
                return node.right, deleted_node
            elif node.right is None:
                return node.left, deleted_node

            temp = self._min_value_node(node.right)
            node.item = temp.item
            node.right, _ = self._delete(node.right, temp.item.title)
        return node, deleted_node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def in_order_traversal(self):
        items = []
        self._in_order_traversal(self.root, items)
        return items

    def _in_order_traversal(self, node, items):
        if node is not None:
            self._in_order_traversal(node.left, items)
            items.append(node.item)
            self._in_order_traversal(node.right, items)

    def search_by_title(self, title):
        return self._search_by_criteria(self.root, lambda item: title.lower() in item.title.lower())

    def search_by_category(self, category):
        return self._search_by_criteria(self.root, lambda item: category.lower() in item.category.lower())

    def search_by_language(self, language):
        return self._search_by_criteria(self.root, lambda item: language.lower() in item.language.lower())

    def search_by_year(self, year):
        return self._search_by_criteria(self.root, lambda item: year in item.year_published)

    def search_by_author(self, author):
        return self._search_by_criteria(self.root, lambda item: author.lower() in item.authors.lower())

    def _search_by_criteria(self, node, criteria):
        items = []
        self._search_by_criteria_helper(node, criteria, items)
        return items

    def _search_by_criteria_helper(self, node, criteria, items):
        if node is not None:
            self._search_by_criteria_helper(node.left, criteria, items)
            if criteria(node.item):
                items.append(node.item)
            self._search_by_criteria_helper(node.right, criteria, items)


class BorrowerNode:
    def __init__(self, borrower):
        self.borrower = borrower
        self.prev = None
        self.next = None

class BorrowerList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.next_account_number = 1

    def generate_account_number(self):
        if self.tail is not None:
            account_number = self.tail.borrower[0] + 1
        else:
            account_number = self.next_account_number

        self.next_account_number = account_number + 1  # Increment for next new account
        return account_number

    def add_borrower(self, borrower):
        new_node = BorrowerNode(borrower)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def find_borrower(self, username):
        current = self.head
        while current:
            if current.borrower[3] == username:
                return current.borrower
            current = current.next
        return None

    def update_borrower(self, updated_borrower):
        current = self.head
        while current:
            if current.borrower[0] == updated_borrower[0]:
                current.borrower = updated_borrower
                return True
            current = current.next
        return False

    def remove_borrower(self, username):
        current = self.head
        while current:
            if current.borrower[3] == username:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                return True
            current = current.next
        return False

    def display_all_borrowers(self):
        borrowers = []
        current = self.head
        while current:
            borrowers.append(current.borrower)
            current = current.next
        return borrowers
