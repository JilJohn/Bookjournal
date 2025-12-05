from flask import Flask, render_template, request, redirect, url_for, session
from db import BookDB
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

journal = BookDB()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['user'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/')
def index():
    books = journal.list_books()
    return render_template('index.html', books=books)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    book = journal.get_book(book_id)
    if not book:
        return "Buch nicht gefunden", 404

    if request.method == 'POST':
        note = request.form.get('note')
        if note:
            journal.add_note_to_book(book_id, note)
        status = request.form.get('status')
        if status:
            journal.update_book_status(book_id, status)
        return redirect(url_for('book_detail', book_id=book_id))

    return render_template('book.html', book=book)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        status = request.form.get('status') or "planned"
        if title:
            journal.add_book(title, author, status)
        return redirect(url_for('index'))

    return render_template('add_book.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if not session.get('user'):
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session.get('user'))

if __name__ == "__main__":
    app.run(debug=True, port=5002)

