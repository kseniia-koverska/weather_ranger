from flask import Flask, flash, render_template, request
from datetime import datetime
import requests
import sqlite3
import secrets
import json

from app import form_submits

# cd .\weather_app\weather_ranger\ (nur für Niklas)
# venv\Scripts\activate
# py app.py

app = Flask(__name__, template_folder='frontend/Wetter/templates')
app.secret_key = secrets.token_hex(32)

staedte = [
	{"name": "Berlin", "Latitude": 52.5200, "Longitude": 13.4050},
	{"name": "Hamburg", "Latitude": 53.5511, "Longitude": 9.9937},
	{"name": "München", "Latitude": 48.1351, "Longitude": 11.5820},
	{"name": "Köln", "Latitude": 50.9375, "Longitude": 6.9603},
	{"name": "Frankfurt am Main", "Latitude": 50.1109, "Longitude": 8.6821},
	{"name": "Stuttgart", "Latitude": 48.7758, "Longitude": 9.1829},
	{"name": "Düsseldorf", "Latitude": 51.2277, "Longitude": 6.7735},
	{"name": "Dortmund", "Latitude": 51.5136, "Longitude": 7.4653},
	{"name": "Essen", "Latitude": 51.4556, "Longitude": 7.0116},
	{"name": "Leipzig", "Latitude": 51.3397, "Longitude": 12.3731}
]

def apiCall(latitude, longitude, date, time):
	url = 'https://api.open-meteo.com/v1/forecast?latitude=' + latitude + '&longitude=' + longitude + '&daily=uv_index_max&hourly=temperature_2m,rain,snowfall,wind_speed_10m&timezone=Europe%2FBerlin&start_date=' + date + '&end_date=' + date
	api_reply = []
	try:
		response = requests.get(url)
		hour_index = time

		# Parse die JSON-antwort
		data = response.json()

		# Extrahieren der Temperatur für eine bestimmte "hourly" Stunde
		# Beispiel: für die Stunde 14:00 (2:00 PM)
		# Die "hourly" Daten sind in Stunden-Verzögerung, daher müssen wir die Stunde auf Stunden-Index in der Datenliste umrechnen
		hourly_data = data['hourly']

		api_reply.append({
					"Datum" : date,
					"Uhrzeit" : time,
					"Temperatur" : hourly_data['temperature_2m'][hour_index],
					"Regen" : hourly_data['rain'][hour_index],
					"Schnee" : hourly_data['snowfall'][hour_index],
					"Wind" : hourly_data['wind_speed_10m'][hour_index]
					})

	except:
		flash("Wetterdaten konnten nicht geladen werden", "error")
		api_reply.append({"Temperatur": None})
	return api_reply


DB_NAME = "wetter.db"


def db_empfehlung_items(temperature):
	result = []
	try:
		if temperature is not None:
			conn = sqlite3.connect(DB_NAME)
			cursor = conn.cursor()

			sql_stmt = """
						SELECT 
							GROUP_CONCAT(k.name, ', ') AS Kleidungsstück, 
							k.kategorie AS Kategorie, 
							w.wetter_typ AS Wetterzustand
						FROM 
							kleidung k
						JOIN 
							wetter_regeln w ON k.id = w.kleidung_id
						WHERE 
							 (
								w.min_temp <= ?
								AND w.max_temp >= ?
							)
						GROUP BY 
							Kategorie;
						"""

			cursor.execute(sql_stmt, (temperature, temperature))
			kleidungsteile = cursor.fetchall()

			for i, item in enumerate(kleidungsteile):
					result.append({
						"name" : item[0],
						"kategorie" : item[1],
						"wetter_typ" : item[2],
					})

			conn.close()
	except:
		flash("Datenbankverbindung fehlgeschlagen", "error")
	return result

@app.route("/", methods=["GET","POST"])
def home():
	datum_aktuell = datetime.now().strftime("%Y-%m-%d")
	uhrzeit_aktuell = datetime.now().strftime("%H:%M")
	form_submits = []
	stadtname = ""
	api_response = []
	result = []
	
	if request.method == "POST":
		standort = json.loads(request.form["standort"])
		stadtname = standort["name"]
		datum = request.form["datum"]
		zeit = request.form["uhrzeit"]
		stunde = int(zeit[:2])
		form_submits.append((datum, zeit))

		api_response = apiCall(str(standort["Latitude"]), str(standort["Longitude"]), datum, stunde)

		#result = db_empfehlung_items(api_response[0]["Temperatur"])
		#Für den Temperaturstest
		result = db_empfehlung_items(-12)

	return render_template("index-test.html", submits=form_submits, datum_aktuell=datum_aktuell, uhrzeit_aktuell=uhrzeit_aktuell, stadtname=stadtname, api_response=api_response, result=result, staedte=staedte)

if __name__ == "__main__":
	app.run(debug=True)

