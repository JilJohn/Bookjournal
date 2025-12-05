from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite:///books.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String)
    status = Column(String, default="planned")

    notes = relationship("Note", back_populates="book", cascade="all, delete")


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    book = relationship("Book", back_populates="notes")


Base.metadata.create_all(engine)


class BookDB:
    def __init__(self):
        self.db = Session()

    def list_books(self):
        return self.db.query(Book).all()

    def get_book(self, book_id):
        return self.db.query(Book).filter(Book.id == book_id).first()

    def add_book(self, title, author=""):
        book = Book(title=title, author=author)
        self.db.add(book)
        self.db.commit()

    def add_note(self, book_id, text):
        note = Note(book_id=book_id, text=text)
        self.db.add(note)
        self.db.commit()

    def update_status(self, book_id, status):
        book = self.get_book(book_id)
        if book:
            book.status = status
            self.db.commit()
# filepath: /Users/jiljohn/Bookjournal/db.py
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite:///books.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String)
    status = Column(String, default="planned")

    notes = relationship("Note", back_populates="book", cascade="all, delete")


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    book = relationship("Book", back_populates="notes")


Base.metadata.create_all(engine)


class BookDB:
    def __init__(self):
        self.db = Session()

    def list_books(self):
        return self.db.query(Book).all()

    def get_book(self, book_id):
        return self.db.query(Book).filter(Book.id == book_id).first()

    def add_book(self, title, author=""):
        book = Book(title=title, author=author)
        self.db.add(book)
        self.db.commit()

    def add_note(self, book_id, text):
        note = Note(book_id=book_id, text=text)
        self.db.add(note)
        self.db.commit()

    def update_status(self, book_id, status):
        book = self.get_book(book_id)
        if book:
            book.status = status
            self.db.commit()