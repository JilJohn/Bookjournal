from typing import Callable
from typing import List

# Status-Farben 
STATUS_COLORS = {
    "read": "gray",         #read erhält Farbe grau
    "reading": "gray",      #reading erhält Farbe grau
    "planned": "gray"       #planned erhält Farbe grau
}

# Status-Anzeigen (Übersetzung)
STATUS_LABELS = {
    "read": "Gelesen",      #Anzeige der gelesenen Bücher
    "reading": "Lese ich",  #Anzeige der Bücher die ich gerade lese
    "planned": "Geplant"    #Anzeige der geplanten Bücher
}

class BookCard:
    """
    Logik einer einzelnen Buchkarte
    """

    def __init__(self, book, on_view_book, on_view, on_edit, on_delete, on_update_book):
        self.book = book
        self.on_view_book = on_view_book
        self.on_view = on_view
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_update_book = on_update_book

def handle_title_click(self):
    # Finde den Index der aktuellen Zeichen-Variante in der VARIANTS-Liste
    current_index = VARIANTS.index(self.current_variant)

    # Berechne den Index der nächsten Variante
    # Das % len(VARIANTS) sorgt dafür, dass wir nach dem letzten Element wieder vorne anfangen (zyklisch)
    next_index = (current_index + 1) % len(VARIANTS)

    # Setze die neue aktuelle Variante
    self.current_variant = VARIANTS[next_index]

    # Speichere die neue Variante auch im Buch-Objekt
    # So weiß das Buch, welche Zeichnungsvariante aktuell ist
    self.book.drawing_variant = self.current_variant


    # Aktionen (Buttons)
    def view(self):
        self.on_view()

    def edit(self):
        self.on_edit()

    def delete(self):
        confirm = input("Möchten Sie dieses Buch wirklich löschen? (ja/nein): ")
        if confirm.lower() == "ja":
            self.on_delete()

def get_display_data(self):
    """
    Gibt die wichtigsten Buchinfos zurück.
    """
    return {
        "title": self.book.title,
        "author": self.book.author,
        "genre": self.book.genre,
        "year": self.book.year,
        "has_notes": len(self.book.notes) > 0,
        "drawing_variant": self.current_variant
    }

