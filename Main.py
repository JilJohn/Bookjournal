# Importieren der benötigten Bibliotheken
from flask import Flask, render_template, request, redirect, url_for, session, flash
import secrets                                                                                      # Für die sichere Erzeugung von zufälligen Strings, z.B. für die Flask-Session-Keys
import plotly.graph_objects as go                                                                   # Für interaktive Diagramme
from datetime import datetime                                                                       # Für Zeitstempel    
from pathlib import Path                                                                            # Für Dateipfade 
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash                           # Passwort-Hashing

# Flask App initialisieren
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)                                                          # Sicherer Schlüssel für Session-Daten

# ==========================
# Datenbank Setup
# ==========================
engine = create_engine(f"sqlite:///books.db", echo=True)                                            # SQLite Datenbank, die Datenbankdatei heisst books.db
Base = declarative_base()                                                                           # Basis für ORM Klassen, alle Tabellenklassen (User, Book, Note) erben von Base, Datenbankzeilen wie Python-Objekte behandeln

# ==========================
# Datenbankmodelle
# ==========================
class User(Base):
    __tablename__ = "users"                                                                         # Name der Tabelle in der Datenbank: "users"
    id = Column(Integer, primary_key=True)                                                          # Primärschlüssel: Eindeutige ID für jeden User              
    username = Column(String, unique=True, nullable=False)                                          # Benutzername, muss eindeutig sein 
    password_hash = Column(String, nullable=False)                                                  # Passwort-Hash     
    books = relationship("Book", back_populates="user", cascade="all, delete")                      # Beziehung zu Büchern, wenn User gelöscht wird, werden auch alle Bücher gelöscht        


class Book(Base):
    __tablename__ = "books"                                                                         # Name der Tabelle in der Datenbank: "books"
    id = Column(Integer, primary_key=True)                                                          # Primärschlüssel: Eindeutige ID für jedes Buch
    title = Column(String, nullable=False)                                                          # Titel des Buches
    author = Column(String)                                                                         # Autor des Buches
    status = Column(String, default="Geplantes Buch")                                               # Status des Buches
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)                               # ID des zugehörigen Users      

    notes = relationship("Note", back_populates="book", cascade="all, delete")                      # Beziehung zu Notizen, wenn Buch gelöscht wird, werden auch alle Notizen gelöscht
    user = relationship("User", back_populates="books")                                             # Beziehung: Ein Buch gehört genau einem User


class Note(Base):
    __tablename__ = "notes"                                                                         # Name der Tabelle in der Datenbank: "notes"    
    id = Column(Integer, primary_key=True)                                                          # Primärschlüssel: Eindeutige ID für jede Notiz
    book_id = Column(Integer, ForeignKey("books.id"))                                               # ID des zugehörigen Buches
    text = Column(String, nullable=False)                                                           # Text der Notiz
    created_at = Column(DateTime, default=datetime.utcnow)                                          # Erstellungsdatum der Notiz        

    book = relationship("Book", back_populates="notes")                                             # Beziehung: Eine Notiz gehört genau einem Buch


# Erstellen der Tabellen
Base.metadata.create_all(engine)                                                                    # Erstellt die Tabellen in der Datenbank
Session = sessionmaker(bind=engine)
db_session = Session()                                                                              # Erstellt eine konkrete Session-Instanz, über die wir Datenbankabfragen durchführen

# ==========================
# Datenbank-Funktionen
# ==========================
def create_user(username, password):
    """Neuen User erstellen mit Passwort-Hash"""
    password_hash = generate_password_hash(password)                                                # Passwort hashen
    user = User(username=username, password_hash=password_hash)                                     # User-Objekt erstellen
    db_session.add(user)                                                                            #fügt den neuen User der Session hinzu
    db_session.commit() 
    return user

def get_user(username):
    """User anhand des Usernames abrufen"""
    return db_session.query(User).filter(User.username == username).first()                         # Gibt den User zurück oder None, wenn nicht gefunden   

def check_password(user, password):
    """Passwort überprüfen"""
    return check_password_hash(user.password_hash, password)

def list_books(user_id):
    """Alle Bücher eines Users abrufen"""
    return db_session.query(Book).filter(Book.user_id == user_id).all()                             # Abrufen aller Bücher eines bestimmten Users

def get_book(book_id, user_id):
    """Ein bestimmtes Buch eines Users abrufen"""
    return db_session.query(Book).filter(Book.id == book_id, Book.user_id == user_id).first()       # Abrufen eines bestimmten Buches eines bestimmten Users

def add_new_book(title, user_id, author="", status="Geplantes Buch"):                   
    """Neues Buch hinzufügen"""
    book = Book(title=title, author=author, status=status, user_id=user_id)                          # Neues Buch-Objekt erstellen
    db_session.add(book)                                                                             # Fügt das neue Buch der Session hinzu
    db_session.commit()

def delete_book_ondb(book_id, user_id):
    """Buch löschen"""
    book = get_book(book_id, user_id)                                                               # Das Buch des aktuellen Users anhand der Buch-ID abrufen
    if book:
        db_session.delete(book)                                                                     # Löscht das Buch aus der Session
        db_session.commit()

def add_note(book_id, text):
    """Neue Notiz zu einem Buch hinzufügen"""
    note = Note(book_id=book_id, text=text)                                                         # Erstellt ein neues Notiz-Objekt
    db_session.add(note)                                                                            # Fügt die neue Notiz der Session hinzu
    db_session.commit()

def update_status(book_id, status):                  
    """Status eines Buches aktualisieren"""
    book = db_session.query(Book).filter(Book.id == book_id).first()                                # Das Buch anhand der Buch-ID abrufen       
    if book:
        book.status = status
        db_session.commit()

def update_book(book_id, title, author, status):
    """Titel, Autor und Status eines Buches aktualisieren"""
    book = db_session.query(Book).filter(Book.id == book_id).first()                                # Das Buch anhand der Buch-ID abrufen
    if book:
        book.title = title
        book.author = author
        book.status = status                                                                        # Aktualisiert Titel, Autor und Status des Buches
        db_session.commit()

# ==========================
# Statistikfunktionen
# ==========================
def get_status_statistics(user_id):             
    """
    Gibt die Anzahl der Bücher pro Status für einen User zurück.
    Rückgabe: dict {"Geplantes Buch": count, "Aktuelles Buch": count, "Abgeschlossenes Buch": count}
    """
    stats = db_session.query(                                               #Datenbankabfrage, die die Anzahl der Bücher pro Status zählt
        Book.status,                                                        #Buchstatus
        func.count(Book.id).label('count')                                  #Anzahl der Bücher
    ).filter(Book.user_id == user_id).group_by(Book.status).all()           #Gruppierung nach Status

    # Initialisiere alle Status mit 0
    result = {                                                              # Initialisiert ein Dictionary mit allen möglichen Buchstatus und setzt deren Werte auf 0
        "Geplantes Buch": 0,
        "Aktuelles Buch": 0,
        "Abgeschlossenes Buch": 0
    }

    # Fülle die tatsächlichen Werte ein
    for status, count in stats:                                            # Iteriert über die Ergebnisse der Datenbankabfrage
        if status in result:                                               # Prüft, ob der Status im Ergebnis-Dictionary vorhanden ist
            result[status] = count

    return result

def get_total_books(user_id):                                                   # Gesamtanzahl Bücher eines Users
    """Gesamtanzahl Bücher eines Users"""
    return db_session.query(Book).filter(Book.user_id == user_id).count()       # Zählt alle Bücher des Users

def create_status_pie_chart(user_id):                                           # Erstellen eines Plotly Pie Charts für Buchstatus
    """
    Erstellt ein Plotly Pie Chart für die Buchstatus-Verteilung.
    Rückgabe: HTML-Code für das Diagramm
    """
    stats = get_status_statistics(user_id)                                      # Holt die Status-Statistiken für den User  
    labels = [status for status, count in stats.items() if count > 0]           # Nur Status mit mehr als 0 Büchern anzeigen    
    values = [count for count in stats.values() if count > 0]                   # Nur Werte mit mehr als 0 Büchern anzeigen

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])                # Erstellen des Pie-Charts mit Plotly    
    fig.update_layout(title="Buchstatus Übersicht", height=400)                 # Layout anpassen

    return fig.to_html(full_html=False, include_plotlyjs='cdn')                 # Rückgabe des Diagramms als HTML-Code


# ==========================
# Flask-Routen
# ==========================
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registrierungsseite"""
    if request.method == 'POST':                                 # Prüft, ob das Formular abgeschickt wurde (POST-Anfrage)
        username = request.form.get('username')                  #Liest die Eingaben aus dem Formular aus
        password = request.form.get('password')

# Validierung: Sind alle Felder ausgefüllt?
        if not username or not password:
            flash('Bitte fülle alle Felder aus')                    # Fehlermeldung anzeigen
            return render_template('register.html')                 # Formular erneut anzeigen

        if get_user(username):                                      # Prüfen, ob der Username bereits existiert
            flash('Username bereits vergeben')                      # Fehlermeldung anzeigen
            return render_template('register.html')                 # Formular erneut anzeigen

        create_user(username, password)                             # Neuen User erstellen
        flash('Registrierung erfolgreich! Bitte melde dich an.')    # Erfolgsmeldung anzeigen
        return redirect(url_for('login'))                           # Nach der Registrierung zur Login-Seite weiterleiten

    return render_template('register.html')                         # Rendern der Registrierungsseite


@app.route('/login', methods=['GET', 'POST'])                        # Login-Seite
def login():
    """Login-Seite"""
    if request.method == 'POST':                                        # Prüft, ob das Formular abgeschickt wurde (POST-Anfrage)
        username = request.form.get('username')                         # Liest die Eingaben aus dem Formular aus
        password = request.form.get('password')                         # Liest die Eingaben aus dem Formular aus

        user = get_user(username)                                      # User anhand des Usernames abrufen
        if user and check_password(user, password):                    # Prüfen, ob der User existiert und das Passwort korrekt ist
            session['user_id'] = user.id                               # User-ID in der Session speichern
            session['username'] = user.username                        # Username in der Session speichern
            return redirect(url_for('index'))

        flash('Falscher Username oder Passwort')                      # Fehlermeldung anzeigen

    return render_template('login.html')


@app.route('/')
def index():
    """Startseite / Bücherübersicht"""
    books = []
    if session.get('user_id'):                                           # Prüfen, ob ein User eingeloggt ist
        books = list_books(session['user_id'])                           # Alle Bücher des eingeloggten Users abrufen
    return render_template('index.html', books=books, logged_in=session.get('user_id') is not None)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    """Detailansicht eines Buches"""
    if not session.get('user_id'):
        return redirect(url_for('login'))

    book = get_book(book_id, session['user_id'])                                 # Das Buch des aktuellen Users anhand der Buch-ID abrufen
    if not book:                                                                 # Prüfen, ob das Buch existiert
        return "Buch nicht gefunden", 404                                        # Fehler 404, falls das Buch nicht existiert oder nicht zum User gehört  

    if request.method == 'POST':                                                 # Verarbeitung des Formulars bei POST-Anfrage
        note = request.form.get('note')                                          # Neue Notiz aus dem Formular   
        if note:
            add_note(book_id, note)                                              # Neue Notiz zur Datenbank hinzufügen
        status = request.form.get('status')                                      # Neuer Status aus dem Formular
        if status:                                                               # Nur aktualisieren, wenn ein Status angegeben wurde
            update_status(book_id, status)
        return redirect(url_for('book_detail', book_id=book_id))                # Nach dem Hinzufügen der Notiz/Status-Update zurück zur Buchdetailseite

    return render_template('book.html', book=book)                              # Rendern der Buchdetailseite mit den Buchdaten


@app.route('/add_book', methods=['GET', 'POST'])                                # Buch hinzufügen
def add_book():
    """Buch hinzufügen"""   
    if not session.get('user_id'):                                              # Prüfen, ob ein User eingeloggt ist. Wenn nicht, zur Login-Seite weiterleiten.   
        return redirect(url_for('login'))                                       # Weiterleitung zur Login-Seite, wenn nicht eingeloggt

    if request.method == 'POST':                                                # Verarbeitung des Formulars bei POST-Anfrage
        title = request.form.get('title')                                       # Titel aus dem Formular
        author = request.form.get('author')                                     # Autor aus dem Formular
        status = request.form.get('status') or "planned"                        # Status aus dem Formular, Standardwert "Geplantes Buch"
        if title:
            add_new_book(title, session['user_id'], author, status)            # Neues Buch zur Datenbank hinzufügen        
        return redirect(url_for('index'))

    return render_template('add_book.html')                                     # Rendern der Seite zum Buch hinzufügen    


@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])                  # Buch bearbeiten
def edit_book(book_id):
    """Buch bearbeiten"""
    if not session.get('user_id'):                                                                # Prüfen, ob ein User eingeloggt ist. Wenn nicht, zur Login-Seite weiterleiten.                   
        return redirect(url_for('login'))                                                         # Weiterleitung zur Login-Seite, wenn nicht eingeloggt

 # Das Buch des aktuellen Users anhand der Buch-ID abrufen
    book = get_book(book_id, session['user_id'])
    if not book:
        return "Buch nicht gefunden", 404                                                        # 404 Fehler, wenn Buch nicht gefunden

 # Verarbeitung des Formulars bei POST-Anfrage
    if request.method == 'POST':
        title = request.form.get('title')                                                       # Neuer Titel aus dem Formular        
        author = request.form.get('author')                                                     # Neuer Autor aus dem Formular
        status = request.form.get('status')                                                     # Neuer Status aus dem Formular 
        if title:                                                                               # Nur aktualisieren, wenn ein Titel angegeben wurde
            update_book(book_id, title, author, status)                                         # Aktualisiert Titel, Autor und Status des Buches in der Datenbank
        return redirect(url_for('book_detail', book_id=book_id))

    return render_template('edit.html', book=book)                                               # Rendern der Editier-Seite mit den Buchdaten


@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    """Route zum Löschen eines Buches"""
    if not session.get('user_id'):                                                          # Prüfen, ob ein User eingeloggt ist. Wenn nicht, zur Login-Seite weiterleiten.
        return redirect(url_for('login'))

    delete_book_ondb(book_id, session['user_id'])                                           # Löscht das Buch aus der Datenbank, nur wenn es dem aktuellen User gehört
    return redirect(url_for('index'))                                                       # Nach dem Löschen zurück zur Startseite (Bücherübersicht)


@app.route('/logout')
def logout():
    """Logout und Session löschen"""
    session.clear()                                                                         #Löscht alle Session-Daten, d.h. User wird ausgeloggt
    return redirect(url_for('login'))                                                       # Nach dem Löschen zurück zur Startseite (Bücherübersicht)


@app.route('/dashboard')                                                                    # Dashboard - Seite
def dashboard():
    """Dashboard mit Pie-Chart zur Buchstatus-Übersicht"""

# Prüfen, ob der User eingeloggt ist
# session.get('user_id') liefert None zurück, wenn kein User eingeloggt ist
# In diesem Fall wird der Benutzer zur Login-Seite weitergeleitet

    if not session.get('user_id'):
        return redirect(url_for('login'))

    chart_html = create_status_pie_chart(session['user_id'])                                # Erstellen des Pie-Charts für den eingeloggten User
    return render_template('dashboard.html', username=session.get('username'), chart=chart_html)


# ==========================
# App starten
# ==========================
if __name__ == "__main__":
    app.run(debug=True, port=5002)
