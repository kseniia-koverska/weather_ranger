# Flask importieren
# Flask = Webserver
# request = Zugriff auf Daten aus dem Browser (z.B. Formular)
# render_template = HTML-Datei anzeigen
from flask import Flask, request, render_template

# SQLite Bibliothek für Datenbankzugriff
import sqlite3

# Flask App erstellen (Webserver starten)
app = Flask(__name__)


# Funktion um Verbindung zur SQLite-Datenbank herzustellen
def get_db():
    # Verbindung zur Datei "database.db"
    conn = sqlite3.connect("wetter.db")
    return conn


# Route für die Startseite "/"
# Diese Seite kann sowohl GET (Seite laden) als auch POST (Formular senden)
@app.route("/", methods=["GET", "POST"])
def index():

    # Prüfen ob der Browser ein Formular gesendet hat
    if request.method == "POST":

        # DATENQUELLE: HTML Input Feld
        # Der Browser sendet den Inhalt des Formularfelds "name"
        # <input name="name">
        name = request.form["name"]

        # Verbindung zur Datenbank herstellen
        conn = get_db()
        cursor = conn.cursor()

        # DATENZIEL: SQLite Datenbank
        # Der Name wird in die Tabelle "users" gespeichert
        cursor.execute(
            "INSERT INTO users (name) VALUES (?)",
            (name,)
        )

        # Änderungen speichern
        conn.commit()

        # Verbindung schließen
        conn.close()


    # Jetzt Daten aus der Datenbank lesen
    conn = get_db()
    cursor = conn.cursor()

    # DATENQUELLE: SQLite Datenbank
    # Alle Namen aus der Tabelle abrufen
    cursor.execute("SELECT * FROM kleidung")

    users = cursor.fetchall()

    # Verbindung schließen
    conn.close()


    # DATENZIEL: HTML Template
    # Die Daten werden an index.html gesendet
    # Dort können sie mit Jinja angezeigt werden
    return render_template("index.html", kleidung=kleidung)


# Webserver starten
app.run(debug=True)