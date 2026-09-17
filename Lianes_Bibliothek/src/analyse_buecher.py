import pandas as pd
import matplotlib.pyplot as plt

# CSV-Datei laden: erzeugt eine "Tabelle" (DataFrame) aus den Buchdaten
books_df = pd.read_csv('data/books.csv')

# Die ersten Zeilen anzeigen, um zu prüfen, ob das Laden geklappt hat
print("Erste Zeilen der Buch-Tabelle:")
print(books_df.head())

# Anzahl der Bücher pro Genre zählen
genre_counts = books_df['genre'].value_counts()
print("\nAnzahl Bücher pro Genre:")
print(genre_counts)

# Balkendiagramm erstellen und als Bild speichern
genre_counts.plot(kind='bar')
plt.title('Bücher pro Genre')
plt.xlabel('Genre')
plt.ylabel('Anzahl')
plt.tight_layout()
plt.savefig('reports/genre_verteilung.png')
print("\nDiagramm gespeichert unter reports/genre_verteilung.png")