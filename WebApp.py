from flask import Flask, render_template, request, redirect, url_for
from book_app import BookJournalApp

app = Flask(__name__)
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
        if note:
            journal.add_note_to_book(book_id, note)
        status = request.form.get('status')
        if status:
            journal.update_book_status(book_id, status)
        return redirect(url_for('book_detail', book_id=book_id))

    return render_template('book.html', book=book)

if __name__ == "__main__":
    app.run(debug=True)
