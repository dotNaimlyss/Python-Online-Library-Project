# item.py
class Item:
    def __init__(self, item_id, title, category, language, authors, year_published, due_date, isbn, item_type, audio_format):
        self.item_id = item_id
        self.title = title
        self.category = category
        self.language = language
        self.authors = authors
        self.year_published = year_published
        self.due_date = due_date
        self.type = item_type
        self.isbn = isbn
        self.audio_format = audio_format

    def __str__(self):
        return (f"{self.title}, {self.category}, {self.language}, {self.authors}, {self.year_published}, {self.type}, Due: {self.due_date}")

class Book(Item):
    def __init__(self, item_id, title, category, language, authors, year_published, due_date, isbn, item_type, audio_format):
        super().__init__(item_id, title, category, language, authors, year_published, due_date, isbn, item_type, audio_format)

    def __str__(self):
        return super().__str__() + f", {self.isbn}"

class Periodical(Item):
    def __init__(self, item_id, title, category, language, authors, year_published, due_date, isbn, item_type, audio_format):
        super().__init__(item_id, title, category, language, authors, year_published, due_date, isbn, item_type, audio_format)

class Magazine(Item):
    def __init__(self, item_id, title, category, language, authors, year_published, due_date, isbn, item_type, audio_format):
        super().__init__(item_id, title, category, language, authors, year_published, due_date, isbn, item_type, audio_format)

class AudioBook(Item):
    def __init__(self, item_id, title, category, language, authors, year_published, due_date, isbn, item_type, audio_format):
        super().__init__(item_id, title, category, language, authors, year_published, due_date, isbn, item_type, audio_format)

    def __str__(self):
        return super().__str__() + f", {self.isbn}, {self.audio_format}"
