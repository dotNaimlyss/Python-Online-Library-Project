from datetime import datetime, timedelta

class BorrowedItems:
    def __init__(self):
        self.borrowed_items = []

    def borrow_item(self, borrower_id, item_id, borrow_date=None, due_date=None):
        if not borrow_date:
            borrow_date = datetime.now().strftime('%Y-%m-%d')
        if not due_date:
            due_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        self.borrowed_items.append((borrower_id, str(item_id), borrow_date, due_date))

    def return_item(self, borrower_id, item_id):
        for i, (b_id, itm_id, borrow_date, due_date) in enumerate(self.borrowed_items):
            if b_id == borrower_id and itm_id == item_id:
                self.borrowed_items.pop(i)
                print(f"Item '{item_id}' returned on {datetime.now().strftime('%Y-%m-%d')}")
                return
        print("Item not found in borrowed items.")

    def get_borrowed_items(self, borrower_id):
        return [(itm_id, borrow_date, due_date) for b_id, itm_id, borrow_date, due_date in self.borrowed_items if b_id == borrower_id]

    def count_borrowed_items(self, borrower_id):
        return sum(1 for b_id, itm_id, borrow_date, due_date in self.borrowed_items if b_id == borrower_id)

    def get_all_borrowed_items(self):
        return self.borrowed_items

    def calculate_fine(self, borrower_id):
        total_fine = 0
        for b_id, itm_id, borrow_date, due_date in self.borrowed_items:
            if b_id == borrower_id:
                try:
                    due_date = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    due_date = datetime.strptime(due_date, '%Y-%m-%d')
                if datetime.now() > due_date:
                    days_overdue = (datetime.now() - due_date).days
                    total_fine += days_overdue * 0.5  # Assuming $0.50 fine per day
        return total_fine

