from werkzeug.security import generate_password_hash, check_password_hash
from models import Session, User, Book, Note


class BookDB:
    def __init__(self):
        self.db = Session()

    def create_user(self, username, password):
        password_hash = generate_password_hash(password)
        user = User(username=username, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        return user

    def get_user(self, username):
        return self.db.query(User).filter(User.username == username).first()

    def check_password(self, user, password):
        return check_password_hash(user.password_hash, password)

    def list_books(self, user_id):
        return self.db.query(Book).filter(Book.user_id == user_id).all()

    def get_book(self, book_id, user_id):
        return self.db.query(Book).filter(Book.id == book_id, Book.user_id == user_id).first()

    def add_book(self, title, user_id, author="", status="Geplantes Buch"):
        book = Book(title=title, author=author, status=status, user_id=user_id)
        self.db.add(book)
        self.db.commit()

    def add_note(self, book_id, text):
        note = Note(book_id=book_id, text=text)
        self.db.add(note)
        self.db.commit()

    def update_status(self, book_id, status):
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book:
            book.status = status
            self.db.commit()