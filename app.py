from flask import Flask, render_template, request
import sqlite3
import sys
app = Flask(__name__, template_folder='frontend/Wetter/templates')

# START SERVER:

# cd .\weather_app\weather_ranger\ (nur für Niklas)
# venv\Scripts\activate
# py app.py

# venv verlassen: deactivate

# START: ------------------------ API Logik --------------------------

lat = '52.52'

long = '13.41'

url = 'https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=uv_index_max&hourly=temperature_2m,rain,snowfall,wind_speed_10m&timezone=Europe%2FBerlin&utm_source=chatgpt.com'

url_glued = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=#' + long + '&daily=uv_index_max&hourly=temperature_2m,rain,snowfall,wind_speed_10m&timezone=Europe%2FBerlin&utm_source=chatgpt.com'



"""
Berlin: Latitude: 52.5200°, Longitude: 13.4050°

Hamburg: Latitude: 53.5511°, Longitude: 9.9937°

München: Latitude: 48.1351°, Longitude: 11.5820°

Köln: Latitude: 50.9375°, Longitude: 6.9603°

Frankfurt am Main: Latitude: 50.1109°, Longitude: 8.6821°

Stuttgart: Latitude: 48.7758°, Longitude: 9.1829°

Düsseldorf: Latitude: 51.2277°, Longitude: 6.7735°

Dortmund: Latitude: 51.5136°, Longitude: 7.4653°

Essen: Latitude: 51.4556°, Longitude: 7.0116°

Leipzig: Latitude: 51.3397°, Longitude: 12.3731°
"""


# END:    ------------------------ API Logik -------------------------


# --------------------- DATENBANK INTEGRATION ------------------------

# Name Testdatenbank
DB_NAME = "test_wetter.db"

# Test-Datenbank erstellen + Tabelle anlegen
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wetter (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stadt TEXT,
        temperatur INTEGER
    )
    """)

    cursor.execute(
        "INSERT INTO wetter (stadt, temperatur) VALUES (?, ?)",
        ("Berlin", 20)   # Beispiel: Stadt Berlin, 20°C
    )

    conn.commit()
    conn.close()


# Datenbank Verbindung
def get_db():
    return sqlite3.connect(DB_NAME)

form_submits = []

@app.route("/", methods=["GET","POST"])
def home():
	print("Python используется из:", sys.executable)
	if request.method == "POST":
		standort = request.form["standort"]
		datum = request.form["datum"]
		zeit = request.form["uhrzeit"]
		
		form_submits.append((datum, zeit))

		conn = get_db()
		cursor = conn.cursor()

		print("Standort:", standort)
		print("Datum:", datum)

	return render_template("index.html", submits=form_submits)

if __name__ == "__main__":
	init_db() 
	app.run(debug=True)

