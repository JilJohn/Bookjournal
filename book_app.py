class BookJournalApp:
    def __init__(self):
        self.books = []
        ...
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@dataclass
class Note:
    id: str
    text: str
    date: str

@dataclass
class Book:
    id: str
    title: str
    author: str
    genre: str
    year: int
    status: str
    date_added: str
    date_finished: Optional[str] = None
    notes: List[Note] = field(default_factory=list)
    cover_image: Optional[str] = None

class BookJournalApp:
    def __init__(self):
        self.books = [
            Book("1", "Der grosse Gatsby", "F. Scott Fitzgerald", "Klassiker", 1925, "read",
                 "2024-01-15", "2024-02-01", cover_image="gatsby.jpg"),
            Book("2", "1984", "George Orwell", "Dystopie", 1949, "reading",
                 "2024-02-10", cover_image="1984.jpg"),
            Book("3", "Sapiens", "Yuval Noah Harari", "Sachbuch", 2011, "planned",
                 "2024-03-01", cover_image="sapiens.jpg"),
        ]
        self.selected_book_id = None

    def get_book(self, book_id): return next((b for b in self.books if b.id == book_id), None)
    def list_books(self, status=None): return [b for b in self.books if b.status == status] if status else self.books
    def update_book_status(self, book_id, status):
        book = self.get_book(book_id)
        if not book: return False
        book.status = status
        book.date_finished = now() if status=="read" else None
        return True
    def add_note_to_book(self, book_id, text):
        book = self.get_book(book_id)
        if not book: return None
        note = Note(str(uuid.uuid4()), text, now())
        book.notes.append(note)
        return note
    def list_notes(self, book_id):
        book = self.get_book(book_id)
        return book.notes if book else []
