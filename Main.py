import os
from flask import Flask, render_template, request, redirect, url_for, session
from book_app import BookJournalApp

# wähle templates-Ordner (case-insensitive)
base_dir = os.path.dirname(__file__)
if os.path.isdir(os.path.join(base_dir, "templates")):
    template_folder = "templates"
elif os.path.isdir(os.path.join(base_dir, "Templates")):
    template_folder = "Templates"
else:
    template_folder = "templates"

app = Flask(__name__, template_folder=template_folder, static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

journal = BookJournalApp()

@app.route('/')
def index():
    books = journal.list_books()
    return render_template('index.html', books=books)

@app.route('/book/<book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    book = journal.get_book(book_id)
    if not book:
        return "Buch nicht gefunden", 404

    if request.method == 'POST':
        note = request.form.get('note')
        if note and hasattr(journal, "add_note_to_book"):
            journal.add_note_to_book(book_id, note)
        status = request.form.get('status')
        if status and hasattr(journal, "update_book_status"):
            journal.update_book_status(book_id, status)
        return redirect(url_for('book_detail', book_id=book_id))

    return render_template('book.html', book=book)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        status = request.form.get('status')
        if title and hasattr(journal, "add_book"):
            try:
                # best-effort Aufruf: (title, author, status) oder (title, author)
                journal.add_book(title, author, status)
            except TypeError:
                try:
                    journal.add_book(title, author)
                except Exception:
                    pass
        return redirect(url_for('index'))

    books = journal.list_books()
    return render_template('add_book.html', books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['user'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

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
