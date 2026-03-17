from flask import Flask, render_template, request
import requests
import sqlite3
import sys
app = Flask(__name__, template_folder='frontend/Wetter/templates')

# START SERVER:



# venv verlassen: deactivate

# START: ------------------------ API Logik --------------------------

# Test-URL für Berlin:
# url = 'https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,rain,snowfall,wind_speed_10m&timezone=Europe%2FBerlin&start_date=2026-03-03&end_date=2026-03-17'
# longitude, latitude for Berlin:
# lat = '52.52'
# long = '13.41'

def apiCall(latitude, longitude, date, time):
	url = 'https://api.open-meteo.com/v1/forecast?latitude=' + latitude + '&longitude=' + longitude + '&daily=uv_index_max&hourly=temperature_2m,rain,snowfall,wind_speed_10m&past_days=7&timezone=Europe%2FBerlin&start_date=' + date + '&end_date=' + date
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
DB_NAME = "wetter.db"

# Funktion für DB-Suche (Kleidungsempfehlung im bestimmten Temp. Bereich):

def db_empfehlung_items(min_t, max_t, kategorie):
	conn = sqlite3.connect(DB_NAME)
	cursor = conn.cursor()

	empfehlung_items = []

	sql_stmt = """
				SELECT 
					k.name AS Kleidungsstück, 
					k.kategorie AS Kategorie, 
					w.min_temp AS Min_Temperatur, 
					w.max_temp AS Max_Temperatur,
					w.wetter_typ AS Wetterzustand
				FROM 
					kleidung k
				JOIN 
					wetter_regeln w ON k.id = w.kleidung_id
				WHERE 
					k.kategorie = ?
					AND (
						w.min_temp <= ?
						AND w.max_temp >= ?
					)
				ORDER BY 
					k.name;
				"""

	cursor.execute(sql_stmt, (kategorie, max_t, min_t))
	kleidungsteile = cursor.fetchall()

	for i, item in enumerate(kleidungsteile):
			empfehlung_items.append(item[0])
	
	conn.close()

	return empfehlung_items


# Test-Datenbank erstellen + Tabelle anlegen
def init_db():
	try:
		conn = sqlite3.connect(DB_NAME)
		cursor = conn.cursor()
		
		print("Succesfully connected to", DB_NAME)


		# Test welche Tabellen gibt es?

		#cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
		#tables = cursor.fetchall()
		#print("Tabellen:")
		#for table in tables:
		#	print(table)


		# Test SQL-Statement (Temp: 0 - 5 Grad, Kategorie "Oberteil")

		cursor.execute("""
						SELECT 
							k.name AS Kleidungsstück, 
							k.kategorie AS Kategorie, 
							w.min_temp AS Min_Temperatur, 
							w.max_temp AS Max_Temperatur,
							w.wetter_typ AS Wetterzustand
						FROM 
							kleidung k
						JOIN 
							wetter_regeln w ON k.id = w.kleidung_id
						WHERE 
							k.kategorie = 'Oberteil' 
							AND (
								
								w.min_temp <= 5 AND w.max_temp >= 0
							)
						ORDER BY 
							k.name;
						""")
		
		kleidungsteile = cursor.fetchall()


		#print("Tabelleninhalt:", tables_content)
		print("Kleidung bei 0°C bis 5°C:")

		for i, item in enumerate(kleidungsteile):
			print(item[0])
		
		print("Daten aus db_empfehlung_items Funktion:")
		empfehlung = db_empfehlung_items(10, 15, 'Oberteil')
		print(empfehlung)




	except sqlite3.Error as e:
		print("SQLite Fehler:", e)

	finally:
		if conn:
			conn.close()


# Datenbank Verbindung
def get_db():
    return sqlite3.connect(DB_NAME)

# ------------- API FRONTEND/BACKEND ------------------------

form_submits = []


@app.route("/", methods=["GET","POST"])
def home():
	print("Python is used from:", sys.executable)

	api_response = []
	empfehlung_oberteil = ''
	empfehlung_accessoire = ''
	empfehlung_hose = ''
	empfehlung_schuhe = ''
	empfehlung_sonnenbrille = False
	
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

		temperature = api_response[0]["Temperatur"]
		# Testtemperatur
		temperature = -12

		kleidungs_kategorien = ['Oberteile', 'Hose', 'Accessoire', 'Schuhe']
		temp_intervalle = []

		# To Do: Vereinfachung IF-Block mit einer Funktion
		def empfehlung_frontend(temp_intervals, kategorien):
			pass


		if -20 <= temperature < -15:
			empfehlung_oberteil = db_empfehlung_items(-20, -15, 'Oberteil')
			empfehlung_accessoire = db_empfehlung_items(-20, -15, 'Accessoire')
			empfehlung_hose = db_empfehlung_items(-20, -15, 'Hose')
			empfehlung_schuhe = db_empfehlung_items(-20, -15, 'Schuhe')
			empfehlung_sonnenbrille = False
		
		elif -15 <= temperature < -10:
			empfehlung_oberteil = db_empfehlung_items(-15, -10, 'Oberteil')
			empfehlung_accessoire = db_empfehlung_items(-15, -10, 'Accessoire')
			empfehlung_hose = db_empfehlung_items(-15, -10, 'Hose')
			empfehlung_schuhe = db_empfehlung_items(-15, -10, 'Schuhe')
			empfehlung_sonnenbrille = False
		
		elif -10 <= temperature < -5:
			empfehlung_oberteil = db_empfehlung_items(-10, -5, 'Oberteil')
			empfehlung_accessoire = db_empfehlung_items(-10, -5, 'Accessoire')
			empfehlung_hose = db_empfehlung_items(-10, -5, 'Hose')
			empfehlung_schuhe = db_empfehlung_items(-10, -5, 'Schuhe')
			empfehlung_sonnenbrille = False
		
		elif -5 <= temperature < 0:
			empfehlung_oberteil = db_empfehlung_items(-5, 0, 'Oberteil')
			empfehlung_accessoire = db_empfehlung_items(-5, 0, 'Accessoire')
			empfehlung_hose = db_empfehlung_items(-5, 0, 'Hose')
			empfehlung_schuhe = db_empfehlung_items(-5, 0, 'Schuhe')
			empfehlung_sonnenbrille = False
		
		elif 0 <= temperature < 10:
			empfehlung_oberteil = db_empfehlung_items(0, 10, 'Oberteil')
			empfehlung_accessoire = db_empfehlung_items(0, 10, 'Accessoire')
			empfehlung_hose = db_empfehlung_items(0, 10, 'Hose')
			empfehlung_schuhe = db_empfehlung_items(0, 10, 'Schuhe')
			empfehlung_sonnenbrille = False
		
		elif 10 <= temperature <= 15:
			empfehlung_oberteil = db_empfehlung_items(10, 15, 'Oberteil')
			empfehlung_accessoire = db_empfehlung_items(10, 15, 'Accessoire')
			empfehlung_hose = db_empfehlung_items(10, 15, 'Hose')
			empfehlung_schuhe = db_empfehlung_items(10, 15, 'Schuhe')
			empfehlung_sonnenbrille = False
		
		elif 15 < temperature < 20:
			empfehlung_oberteil = db_empfehlung_items(15, 20, 'Oberteil')
			empfehlung_accessoire = db_empfehlung_items(15, 20, 'Accessoire')
			empfehlung_hose = db_empfehlung_items(15, 20, 'Hose')
			empfehlung_schuhe = db_empfehlung_items(15, 20, 'Schuhe')
			empfehlung_sonnenbrille = False
		
		elif temperature >= 20:
			empfehlung_oberteil = db_empfehlung_items(20, 100, 'Oberteil')
			empfehlung_accessoire = db_empfehlung_items(20, 100, 'Accessoire')
			empfehlung_hose = db_empfehlung_items(20, 100, 'Hose')
			empfehlung_schuhe = db_empfehlung_items(20, 100, 'Schuhe')
			empfehlung_sonnenbrille = True
		


	return render_template("index.html", submits=form_submits, api_response=api_response, empfehlung_oberteil=empfehlung_oberteil, empfehlung_hose=empfehlung_hose, empfehlung_schuhe=empfehlung_schuhe, empfehlung_accessoire=empfehlung_accessoire)

if __name__ == "__main__":
	init_db()
	app.run(debug=True)

