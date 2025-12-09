from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase

# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "books.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    books = relationship("Book", back_populates="user", cascade="all, delete")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String)
    status = Column(String, default="planned")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    notes = relationship("Note", back_populates="book", cascade="all, delete")
    user = relationship("User", back_populates="books")


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    book = relationship("Book", back_populates="notes")


Base.metadata.create_all(engine)