from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import BookDB
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

journal = BookDB()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Bitte fülle alle Felder aus')
            return render_template('register.html')

        if journal.get_user(username):
            flash('Username bereits vergeben')
            return render_template('register.html')

        journal.create_user(username, password)
        flash('Registrierung erfolgreich! Bitte melde dich an.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = journal.get_user(username)
        if user and journal.check_password(user, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))

        flash('Falscher Username oder Passwort')

    return render_template('login.html')

@app.route('/')
def index():
    books = []
    if session.get('user_id'):
        books = journal.list_books(session['user_id'])
    return render_template('index.html', books=books, logged_in=session.get('user_id') is not None)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))

    book = journal.get_book(book_id, session['user_id'])
    if not book:
        return "Buch nicht gefunden", 404

    if request.method == 'POST':
        note = request.form.get('note')
        if note:
            journal.add_note(book_id, note)
        status = request.form.get('status')
        if status:
            journal.update_status(book_id, status)
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
            journal.add_book(title, session['user_id'], author, status)
        return redirect(url_for('index'))

    return render_template('add_book.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session.get('username'))

if __name__ == "__main__":
    app.run(debug=True, port=5002)