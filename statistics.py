from models import Session, Book
from sqlalchemy import func


class BookStatistics:
    def _init_(self):
        self.db = Session()

    def get_status_statistics(self, user_id):
        """
        Gibt die Anzahl der Bücher pro Status für einen User zurück.

        Returns:
            dict: {"Geplantes Buch": count, "Aktuelles Buch": count, "Abgeschlossenes Buch": count}
        """
        stats = self.db.query(
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

    def get_total_books(self, user_id):
        """
        Gibt die Gesamtanzahl der Bücher für einen User zurück.
        """
        return self.db.query(Book).filter(Book.user_id == user_id).count()