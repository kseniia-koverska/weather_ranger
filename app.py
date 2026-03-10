from flask import Flask, render_template, request
import requests
import sqlite3
import sys
app = Flask(__name__, template_folder='frontend/Wetter/templates')

# START SERVER:

# cd .\weather_app\weather_ranger\ (nur für Niklas)
# venv\Scripts\activate
# py app.py

# venv verlassen: deactivate

# START: ------------------------ API Logik --------------------------

# Test-URL für Berlin:
# url = 'https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,rain,snowfall,wind_speed_10m&timezone=Europe%2FBerlin&start_date=2026-03-03&end_date=2026-03-17'
# longitude, latitude for Berlin:
# lat = '52.52'
# long = '13.41'

def apiCall(latitude, longitude, date, time):
	url = 'https://api.open-meteo.com/v1/forecast?latitude=' + latitude + '&longitude=' + longitude + '&daily=uv_index_max&hourly=temperature_2m,rain,snowfall,wind_speed_10m&timezone=Europe%2FBerlin&start_date=' + date + '&end_date=' + date
	response = requests.get(url)
	hour_index = time 

	# Antwort als Array:
	api_reply = []
	
	# Überprüfen, ob die Anfrage erfolgreich war
	if response.status_code == 200:

		# Parse die JSON-antwort
		data = response.json()
		
		# Extrahieren der Temperatur für eine bestimmte "hourly" Stunde
		# Beispiel: für die Stunde 14:00 (2:00 PM)
		# Die "hourly" Daten sind in Stunden-Verzögerung, daher müssen wir die Stunde auf Stunden-Index in der Datenliste umrechnen
		hourly_data = data['hourly']
		
		temperature = hourly_data['temperature_2m'][hour_index]
		rain = hourly_data['rain'][hour_index]
		snowfall = hourly_data['snowfall'][hour_index]
		wind = hourly_data['wind_speed_10m'][hour_index]
		print("Datum:", date)
		print(f"Temperature at hour {hour_index}: {temperature}°C")
		print(f"Rain: {rain}mm, Snowfall: {snowfall}cm, Wind: {wind} km/h")

		api_reply.append({
						"Datum" : date,
						"Uhrzeit" : time, 
						"Temperatur" : hourly_data['temperature_2m'][hour_index],
						"Regen" : hourly_data['rain'][hour_index],
						"Schnee" : hourly_data['snowfall'][hour_index],
						"Wind" : hourly_data['wind_speed_10m'][hour_index]
						})
		
		return api_reply

	else:
		print(f"Fehler: Die Anfrage wurde nicht erfolgreich abgearbeitet. Statuscode: {response.status_code}")
		api_error = f"Fehler: Die Anfrage wurde nicht erfolgreich abgearbeitet. Statuscode: {response.status_code}"
		api_reply.append(api_error)
		return api_reply


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
	print("Python is used from:", sys.executable)

	api_response = ['Test']

	if request.method == "POST":
		print("--------------------TEST----------------")
		standort = request.form["standort"]
		datum = request.form["datum"]
		zeit = request.form["uhrzeit"]
		stunde = int(zeit[:2])
		form_submits.append((datum, zeit))

		conn = get_db()
		cursor = conn.cursor()

		print("Standort:", standort)
		print("Datum:", datum)

		# api_response = [datum, stunde]

		api_response = apiCall('52.52', '13.41', datum, stunde)

	return render_template("index.html", submits=form_submits, api_response=api_response)

if __name__ == "__main__":
	init_db() 
	app.run(debug=True)

