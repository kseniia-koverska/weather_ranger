from flask import Flask, flash, render_template, request
from datetime import datetime, timedelta

import requests
import sqlite3
import secrets
import json


#from app import form_submits



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
		daily_data = data['daily']

		api_reply.append({
					"Datum" : date,
					"Uhrzeit" : time,
					"Temperatur" : hourly_data['temperature_2m'][hour_index],
					"Regen" : hourly_data['rain'][hour_index],
					"Schnee" : hourly_data['snowfall'][hour_index],
					"Wind" : hourly_data['wind_speed_10m'][hour_index],
					"UV" : daily_data['uv_index_max'][0]
					})

	except:
		flash("Wetterdaten konnten nicht geladen werden", "error")
		api_reply.append({"Temperatur": None})
	return api_reply


DB_NAME = "anderung.db"


def db_empfehlung_items(temperature):
	result = []
	try:
		if temperature is not None:
			conn = sqlite3.connect(DB_NAME)
			cursor = conn.cursor()

			sql_stmt = """
						SELECT 
							GROUP_CONCAT(DISTINCT k.name) AS Kleidungsstück, 
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

			#Testing:
			global kleider_test
			kleider_test = kleidungsteile

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

# Testing:
result = db_empfehlung_items(10.9)
print("Test with 10.9°:", result)
print("SQL Statement -> DB, min_temp <= 10.9, max_temp >= 10.9:", kleider_test)

@app.template_filter("date_de")
def date_de(value):
    return datetime.strptime(value, "%Y-%m-%d").strftime("%d.%m.%Y")

@app.route("/", methods=["GET","POST"])
def home():



	# Variablen für Empfehlungen bezogen auf Regen, Sonne, Schnee:

	rain_kleidung = False
	snow_kleidung = False
	sunglasses = False
	rains = 0.0
	uv_index = 0.00
	url = ''


	datum_aktuell = datetime.now().strftime("%Y-%m-%d")
	now = datetime.now()
	uhrzeit_aktuell = datetime.now().strftime("%H:%M")
	min_date = (now - timedelta(days=7)).strftime("%Y-%m-%d")
	max_date = (now + timedelta(days=7)).strftime("%Y-%m-%d")
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

		result = db_empfehlung_items(api_response[0]["Temperatur"])

		#Zum Testen, künstliche Werte erstellen:
		#Temperatur: -20 (veränderbar)
		#result = db_empfehlung_items(30)
		#Testwert für Schnee
		#api_response[0]["Schnee"] = 3.00
		#Testwert für Regen
		#api_response[0]["Regen"] = 3.00

	return render_template(
		"index.html",
		submits=form_submits,
		datum_aktuell=datum_aktuell,
		min_date=min_date,
		max_date=max_date,
		uhrzeit_aktuell=uhrzeit_aktuell,
		stadtname=stadtname,
		api_response=api_response,
		result=result,
		staedte=staedte
	)
if __name__ == "__main__":
	app.run(debug=True)