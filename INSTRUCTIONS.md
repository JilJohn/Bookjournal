# Code Review Erklärung

Diese Flask-Applikation ist eine persönliche Bücherverwaltung mit Benutzerkonten.
User können sich registrieren, einloggen, Bücher anlegen, bearbeiten, löschen, Notizen hinzufügen und im Dashboard eine Status-Auswertung als Pie-Chart sehen.

Technologien: Flask (Webframework), SQLAlchemy (ORM & Datenbank), SQLite (Datenbank), Plotly (Visualisierung), Sessions für Login-Status



## Import
Alle benötigten Bibliotheken werden eingebunden.

secrets.token_urlsafe(32) → sicherer Session-Key
werkzeug.security → Passwort wird nie im Klartext gespeichert
plotly.graph_objects → interaktive Diagramme






## Datenbank Setup

ORM: Tabellen werden als Python-Klassen modelliert, Kein rohes SQL notwendig

engine = create_engine("sqlite:///books.db", echo=True)
Base = declarative_base()



## Datenbankmodelle

class User(Base):                                   #Ein User kann mehrere Bücher haben
    id, username, password_hash                     #Passwort nur als Hash
    books = relationship(...)

class Book(Base):
    title, author, status, user_id                  #Jedes Buch gehört genau einem user, Status z.B. „Geplantes Buc„Aktuelles Buch“, „Abgeschlossenes Buch“

class Note(Base):                                   #Ein Buch kann mehrere Notizen haben, Zeitstempel wird automatisch gesetzt
    text, created_at, book_id



cascade="all, delete" verhindert verwaiste Daten





Datenbank-Funktionen
Alle DB-Operationen sind ausgelagert → sehr gut für Wartbarkeit.

create_user() → User anlegen + Passwort hashen
get_book() → Sicherheitsrelevant: Buch nur vom eigenen User
update_book() → zentrale Update-Logik
add_note() → einfache Erweiterbark
"""



## Routen


if not session.get('user_id'):
    return redirect(url_for('login'))
