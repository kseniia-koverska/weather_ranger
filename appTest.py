from flask import Flask, flash, render_template, request
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim # Import aus der Textdatei 
import requests
import sqlite3
import secrets

app = Flask(__name__, template_folder='frontend/Wetter/templates')
app.secret_key = secrets.token_hex(32)

# Initialisierung des Geolocators 
# "user_agent" sollte eindeutig sein, damit der Dienst stabil läuft
geolocator = Nominatim(user_agent="WeatherRanger_App_v1")

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

    return render_template(
        "index-test.html",
        datum_aktuell=datum_aktuell,
        uhrzeit_aktuell=uhrzeit_aktuell,
        stadtname=stadtname,
        api_response=api_response,
        result=result
        # 'staedte=staedte' wird nicht mehr benötigt!
    )