from sqlalchemy import text
from db_connection import engine


def buch_hinzufuegen(author_id, title, genre, isbn, pub_year, language, publisher):
    """Fügt ein neues Buch in die books-Tabelle ein (Create)."""
    query = text("""
        INSERT INTO books (authorID, title, genre, ISBN, pub_year, language, publisher)
        VALUES (:author_id, :title, :genre, :isbn, :pub_year, :language, :publisher)
    """)
    # engine.begin() übernimmt Commit/Rollback automatisch und schließt
    # die Verbindung am Ende des with-Blocks
    with engine.begin() as connection:
        connection.execute(query, {
            "author_id": author_id, "title": title, "genre": genre,
            "isbn": isbn, "pub_year": pub_year,
            "language": language, "publisher": publisher
        })
    print(f"Buch '{title}' erfolgreich hinzugefügt.")


def buch_suchen(suchbegriff):
    """Sucht Bücher, deren Titel den Suchbegriff enthält (Read)."""
    query = text("""
        SELECT title, genre, pub_year
        FROM books
        WHERE title LIKE :suchbegriff
    """)
    with engine.connect() as connection:
        ergebnis = connection.execute(query, {"suchbegriff": f"%{suchbegriff}%"})
        return ergebnis.fetchall()

def buch_zurueckgeben(book_id):
    """Trägt die Rückgabe eines Buches ein (Update): setzt return_date
    auf das heutige Datum und borrowed auf 0, für den aktuell offenen
    Loan (return_date IS NULL) zu dieser bookID."""
    query = text("""
        UPDATE loans
        SET return_date = CURDATE(), borrowed = 0
        WHERE bookID = :book_id AND return_date IS NULL
    """)
    with engine.begin() as connection:
        ergebnis = connection.execute(query, {"book_id": book_id})
        if ergebnis.rowcount == 0:
            print(f"Kein offener Loan für bookID {book_id} gefunden.")
            return False
        print(f"Buch mit bookID {book_id} als zurückgegeben markiert.")
        return True

def buch_ausleihen(book_id, borrower_id):
    """Trägt eine neue Ausleihe ein (Create): legt einen Loan-Eintrag an,
    aber nur, wenn das Buch aktuell nicht bereits verliehen ist."""
    
    # Schritt 1: Sicherheitsprüfung — gibt es schon einen offenen Loan zu diesem Buch?
    check_query = text("""
        SELECT loanID FROM loans
        WHERE bookID = :book_id AND return_date IS NULL
    """)
    with engine.connect() as connection:
        offener_loan = connection.execute(check_query, {"book_id": book_id}).fetchone()

    if offener_loan is not None:
        print(f"Buch mit bookID {book_id} ist bereits verliehen.")
        return False

    # Schritt 2: neuen Loan anlegen
    insert_query = text("""
        INSERT INTO loans (bookID, borrowerID, loan_date, borrowed)
        VALUES (:book_id, :borrower_id, CURDATE(), 1)
    """)
    with engine.begin() as connection:
        connection.execute(insert_query, {"book_id": book_id, "borrower_id": borrower_id})
    
    print(f"Buch mit bookID {book_id} erfolgreich an borrowerID {borrower_id} ausgeliehen.")
    return True

def buch_loeschen(book_id):
    """Entfernt ein Buch aus der books-Tabelle (Delete), aber nur wenn
    aktuell keine offene Ausleihe (return_date IS NULL) dazu existiert."""

    # Schritt 1: Sicherheitsprüfung — ist das Buch aktuell verliehen?
    check_query = text("""
        SELECT loanID FROM loans
        WHERE bookID = :book_id AND return_date IS NULL
    """)
    with engine.connect() as connection:
        offener_loan = connection.execute(check_query, {"book_id": book_id}).fetchone()

    if offener_loan is not None:
        print(f"Buch mit bookID {book_id} ist aktuell verliehen und kann nicht gelöscht werden.")
        return False

    # Schritt 2: Buch löschen
    delete_query = text("""
        DELETE FROM books WHERE bookID = :book_id
    """)
    with engine.begin() as connection:
        ergebnis = connection.execute(delete_query, {"book_id": book_id})
        if ergebnis.rowcount == 0:
            print(f"Kein Buch mit bookID {book_id} gefunden.")
            return False

    print(f"Buch mit bookID {book_id} erfolgreich gelöscht.")
    return True

def alle_buecher():
    """Gibt alle Bücher als Liste von (bookID, title) zurück, für Auswahllisten."""
    query = text("SELECT bookID, title FROM books ORDER BY title")
    with engine.connect() as connection:
        return connection.execute(query).fetchall()

def alle_ausleiher():
    """Gibt alle Ausleiher als Liste von (borrowerID, first_name, last_name) zurück."""
    query = text("SELECT borrowerID, first_name, last_name FROM borrowers ORDER BY last_name")
    with engine.connect() as connection:
        return connection.execute(query).fetchall()

def alle_buecher_detailliert():
    """Gibt alle Bücher mit Genre, Autor und Ausleihstatus zurück, für das Bücherregal."""
    query = text("""
        SELECT b.bookID, b.title, b.genre, a.first_name, a.last_name,
               CASE WHEN l.loanID IS NOT NULL THEN 1 ELSE 0 END AS verliehen
        FROM books b
        LEFT JOIN authors a ON b.authorID = a.authorID
        LEFT JOIN loans l ON b.bookID = l.bookID AND l.return_date IS NULL
        ORDER BY b.title
    """)
    with engine.connect() as connection:
        return connection.execute(query).fetchall() 

def ausleihen_pro_ausleiher(borrower_id):
    """Gibt alle aktuell offenen Ausleihen eines Ausleihers zurück (Read)."""
    query = text("""
        SELECT b.title, l.loan_date
        FROM loans l
        JOIN books b ON l.bookID = b.bookID
        WHERE l.borrowerID = :borrower_id AND l.return_date IS NULL
        ORDER BY l.loan_date
    """)
    with engine.connect() as connection:
        return connection.execute(query, {"borrower_id": borrower_id}).fetchall()


def kontakt_aktualisieren(borrower_id, email, telephone):
    """Aktualisiert E-Mail und Telefonnummer eines Ausleihers (Update)."""
    query = text("""
        UPDATE borrowers
        SET email = :email, telephone = :telephone
        WHERE borrowerID = :borrower_id
    """)
    with engine.begin() as connection:
        ergebnis = connection.execute(query, {"email": email, "telephone": telephone, "borrower_id": borrower_id})
        if ergebnis.rowcount == 0:
            print(f"Kein Ausleiher mit borrowerID {borrower_id} gefunden.")
            return False
        print(f"Kontaktdaten für borrowerID {borrower_id} aktualisiert.")
        return True


def abgeschlossene_ausleihen():
    """Gibt alle bereits zurückgegebenen Ausleihen zurück, zur Auswahl fürs Löschen (Read)."""
    query = text("""
        SELECT l.loanID, b.title, br.first_name, br.last_name, l.loan_date, l.return_date
        FROM loans l
        JOIN books b ON l.bookID = b.bookID
        JOIN borrowers br ON l.borrowerID = br.borrowerID
        WHERE l.return_date IS NOT NULL
        ORDER BY l.return_date DESC
    """)
    with engine.connect() as connection:
        return connection.execute(query).fetchall()


def ausleihe_loeschen(loan_id):
    """Löscht einen abgeschlossenen Ausleihe-Eintrag (Delete), nur wenn er bereits
    zurückgegeben wurde (return_date IS NOT NULL) — schützt laufende Ausleihen."""
    query = text("""
        DELETE FROM loans WHERE loanID = :loan_id AND return_date IS NOT NULL
    """)
    with engine.begin() as connection:
        ergebnis = connection.execute(query, {"loan_id": loan_id})
        if ergebnis.rowcount == 0:
            print(f"Kein abgeschlossener Loan mit loanID {loan_id} gefunden.")
            return False
        print(f"Ausleihe-Eintrag {loan_id} erfolgreich gelöscht.")
        return True  
def alle_ausleihen_uebersicht():
    """Gibt alle Ausleihen (offen und abgeschlossen) mit Buchtitel, Ausleihername
    und Status zurück — Grundlage für die Übersichtstabelle."""
    query = text("""
        SELECT b.title AS Buch, CONCAT(br.first_name, ' ', br.last_name) AS Ausleiher,
               l.loan_date AS Ausgeliehen_am, l.return_date AS Zurueckgegeben_am,
               CASE WHEN l.return_date IS NULL THEN 'Offen' ELSE 'Abgeschlossen' END AS Status
        FROM loans l
        JOIN books b ON l.bookID = b.bookID
        JOIN borrowers br ON l.borrowerID = br.borrowerID
        ORDER BY l.loan_date DESC
    """)
    with engine.connect() as connection:
        return connection.execute(query).fetchall()


def alle_autoren():
    """Gibt alle Autoren als Liste von (authorID, first_name, last_name) zurück, für Auswahllisten."""
    query = text("SELECT authorID, first_name, last_name FROM authors ORDER BY last_name")
    with engine.connect() as connection:
        return connection.execute(query).fetchall()


def ausleiher_hinzufuegen(first_name, last_name, email, telephone):
    """Fügt einen neuen Ausleiher in die borrowers-Tabelle ein (Create)."""
    query = text("""
        INSERT INTO borrowers (first_name, last_name, email, telephone)
        VALUES (:first_name, :last_name, :email, :telephone)
    """)
    with engine.begin() as connection:
        connection.execute(query, {
            "first_name": first_name, "last_name": last_name,
            "email": email, "telephone": telephone
        })
    print(f"Ausleiher '{first_name} {last_name}' erfolgreich hinzugefügt.")
     
# Testaufrufe: laufen nur bei direktem Start dieser Datei,
# nicht beim späteren Import in die App
if __name__ == "__main__":
    buch_hinzufuegen(1, "Doctor Sleep", "Horror", "9783453270092", 2013, "ger", "Heyne")
    print(buch_suchen("Harry Potter"))
    buch_zurueckgeben(8)  # Dune (bookID 8) als Test
    buch_ausleihen(8, 5)  # bookID 8 an borrowerID 5 ausleihen
    buch_loeschen(16)  # sollte erfolgreich löschen
    buch_loeschen(8)   # sollte abbrechen, da verliehen