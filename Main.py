from flask import Flask, render_template, request, redirect, url_for, session, flash
import secrets
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

#Datenbankerstellen
# Get the directory where this script is located
engine = create_engine(f"sqlite:///books.db", echo=True)
Base = declarative_base()


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
    status = Column(String, default="Geplantes Buch")
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
Session= sessionmaker(bind=engine)
db_session = Session()

def create_user(username, password):
    password_hash = generate_password_hash(password)
    user = User(username=username, password_hash=password_hash)
    db_session.add(user)
    db_session.commit()
    return user

def get_user(username):
    return db_session.query(User).filter(User.username == username).first()

def check_password(user, password):
    return check_password_hash(user.password_hash, password)

def list_books(user_id):
    return db_session.query(Book).filter(Book.user_id == user_id).all()

def get_book(book_id, user_id):
    return db_session.query(Book).filter(Book.id == book_id, Book.user_id == user_id).first()

def add_new_book(title, user_id, author="", status="Geplantes Buch"):
    book = Book(title=title, author=author, status=status, user_id=user_id)
    db_session.add(book)
    db_session.commit()

def delete_book_ondb(book_id, user_id):
    book = db_session.query(Book).filter(Book.id == book_id, Book.user_id == user_id).first()
    if book:
        db_session.delete(book)
        db_session.commit()

def add_note(book_id, text):
    note = Note(book_id=book_id, text=text)
    db_session.add(note)
    db_session.commit()

def update_status(book_id, status):
    book = db_session.query(Book).filter(Book.id == book_id).first()
    if book:
        book.status = status
        db_session.commit()

def update_book(book_id, title, author, status):
    book = db_session.query(Book).filter(Book.id == book_id).first()
    if book:
        book.title = title
        book.author = author
        book.status = status
        db_session.commit()


def get_status_statistics(user_id):
    """
    Gibt die Anzahl der Bücher pro Status für einen User zurück.

    Returns:
        dict: {"Geplantes Buch": count, "Aktuelles Buch": count, "Abgeschlossenes Buch": count}
    """
    stats = db_session.query(
        Book.status,
        func.count(Book.id).label('count')
    ).filter(
        Book.user_id == user_id
    ).group_by(
        Book.status
    ).all()

    # Initialisiere alle Status mit 0
    result = {
        "Geplantes Buch": 0,
        "Aktuelles Buch": 0,
        "Abgeschlossenes Buch": 0
    }

    # Fülle die tatsächlichen Werte ein
    for status, count in stats:
        if status in result:
            result[status] = count

    return result

def get_total_books(user_id):
    """
    Gibt die Gesamtanzahl der Bücher für einen User zurück.
    """
    return db_session.query(Book).filter(Book.user_id == user_id).count()

def create_status_pie_chart(user_id):
    """
    Erstellt ein Plotly Pie Chart für die Buchstatus-Verteilung.

    Returns:
        str: HTML-Code für das Plotly Chart
    """
    stats = get_status_statistics(user_id)

    # Entferne Status mit 0 Büchern für eine sauberere Darstellung
    labels = [status for status, count in stats.items() if count > 0]
    values = [count for count in stats.values() if count > 0]

    # Erstelle das Pie Chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    fig.update_layout(
        title="Buchstatus Übersicht",
        height=400
    )

    # Konvertiere zu HTML
    return fig.to_html(full_html=False, include_plotlyjs='cdn')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Bitte fülle alle Felder aus')
            return render_template('register.html')

        if get_user(username):
            flash('Username bereits vergeben')
            return render_template('register.html')

        create_user(username, password)
        flash('Registrierung erfolgreich! Bitte melde dich an.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = get_user(username)
        if user and check_password(user, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))

        flash('Falscher Username oder Passwort')

    return render_template('login.html')

@app.route('/')
def index():
    books = []
    if session.get('user_id'):
        books = list_books(session['user_id'])
    return render_template('index.html', books=books, logged_in=session.get('user_id') is not None)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))

    book = get_book(book_id, session['user_id'])
    if not book:
        return "Buch nicht gefunden", 404

    if request.method == 'POST':
        note = request.form.get('note')
        if note:
            add_note(book_id, note)
        status = request.form.get('status')
        if status:
            update_status(book_id, status)
        return redirect(url_for('book_detail', book_id=book_id))

    return render_template('book.html', book=book)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        status = request.form.get('status') or "planned"
        if title:
            add_new_book(title, session['user_id'], author, status)
        return redirect(url_for('index'))

    return render_template('add_book.html')

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))

    book = get_book(book_id, session['user_id'])
    if not book:
        return "Buch nicht gefunden", 404

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        status = request.form.get('status')
        if title:
            update_book(book_id, title, author, status)
        return redirect(url_for('book_detail', book_id=book_id))

    return render_template('edit.html', book=book)

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))

    delete_book_ondb(book_id, session['user_id'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    chart_html = create_status_pie_chart(session['user_id'])

    return render_template('dashboard.html', username=session.get('username'), chart=chart_html)

if __name__ == "__main__":
    app.run(debug=True, port=5002)