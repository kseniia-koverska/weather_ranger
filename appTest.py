from flask import Flask, flash, render_template, request
from datetime import datetime, timedelta
<<<<<<< HEAD
from geopy.geocoders import Nominatim # Import aus der Textdatei 
import requests
import sqlite3
import secrets
=======

import requests
import sqlite3
import secrets
import json


from app import form_submits



# cd .\weather_app\weather_ranger\ (nur für Niklas)
# venv\Scripts\activate
# py app.py
>>>>>>> 54feb026f993f6deb96d1e3ad631a09d5cbbe6d5

app = Flask(__name__, template_folder='frontend/Wetter/templates')
app.secret_key = secrets.token_hex(32)

# Initialisierung des Geolocators 
# "user_agent" sollte eindeutig sein, damit der Dienst stabil läuft
geolocator = Nominatim(user_agent="WeatherRanger_App_v1")

<<<<<<< HEAD
# Deine bestehenden Funktionen (apiCall, db_empfehlung_items) bleiben gleich...

@app.route("/", methods=["GET","POST"])
def home():
    datum_aktuell = datetime.now().strftime("%Y-%m-%d")
    uhrzeit_aktuell = datetime.now().strftime("%H:%M")
    
    stadtname = ""
    api_response = []
    result = []

    if request.method == "POST":
        # Wir holen den Text aus dem neuen Eingabefeld
        stadt_eingabe = request.form.get("stadt_eingabe")
        datum = request.form.get("datum")
        zeit = request.form.get("uhrzeit")
        stunde = int(zeit[:2]) if zeit else 12

        try:
            # Dynamische Ortssuche mit geopy 
            location = geolocator.geocode(stadt_eingabe)
            
            if location:
                # Koordinaten extrahieren 
                lat = str(location.latitude)
                lon = str(location.longitude)
                stadtname = location.address # Zeigt den vollen Namen an
                
                # API mit den gefundenen Koordinaten aufrufen
                api_response = apiCall(lat, lon, datum, stunde)
                
                if api_response and api_response[0]["Temperatur"] is not None:
                    result = db_empfehlung_items(api_response[0]["Temperatur"])
            else:
                flash(f"Ort '{stadt_eingabe}' wurde nicht gefunden.", "error")
                
        except Exception as e:
            flash("Fehler bei der Ortssuche oder API.", "error")
=======

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
		#Für den Temperaturstest
		#result = db_empfehlung_items(-12)

	return render_template(
		"index-test.html",
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
>>>>>>> 54feb026f993f6deb96d1e3ad631a09d5cbbe6d5

    return render_template(
        "index-test.html",
        datum_aktuell=datum_aktuell,
        uhrzeit_aktuell=uhrzeit_aktuell,
        stadtname=stadtname,
        api_response=api_response,
        result=result
        # 'staedte=staedte' wird nicht mehr benötigt!
    )