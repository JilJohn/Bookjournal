from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "geheim123"  # Für Sessions

# Beispiel-Benutzer
users = {
    "jil": "pass123",
    "max": "12345"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Falscher Benutzername oder Passwort"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)




from flask import Flask, render_template, request, redirect, url_for
from book_app import BookJournalApp

app = Flask(__name__)
journal = BookJournalApp()

# Startseite: Liste aller Bücher
@app.route('/')
def index():
    books = journal.list_books()
    return render_template('index.html', books=books)

# Detailseite für ein Buch
@app.route('/book/<book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    book = journal.get_book(book_id)
    if not book:
        return "Buch nicht gefunden", 404

    if request.method == 'POST':
        note_text = request.form.get('note')
        if note_text:
            journal.add_note_to_book(book_id, note_text)
        status = request.form.get('status')
        if status:
            journal.update_book_status(book_id, status)
        return redirect(url_for('book_detail', book_id=book_id))

    return render_template('book.html', book=book)

