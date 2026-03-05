# API Documentation

# Installation

`pip install requests` (wird benötigt um Anfragen an API zu schicken)

Open Meteo:

Link zur Dokumentation: https://www.meteomatics.com/en/api/getting-started/?gl=1_1sbx4dh__up_MQ.._gs*MQ..&gclid=EAIaIQobChMIzs3A46GGkwMVnP15BB1IPxRKEAAYASAAEgIvw_D_BwE

username / password: (wird nicht benötigt)

Beispiel Wetterdaten Anfrage für Berlin:

https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=uv_index_max&hourly=temperature_2m,rain,snowfall,wind_speed_10m&timezone=Europe%2FBerlin&utm_source=chatgpt.com

Parameter:

`latitude`(Längengrad)

`longitude`(Breitengrad)

`hourly`(für stündliche Angaben)

`timezone`(wichtig: Zeitzone, sollte mit angegeben werden)

`start_date`/ `end_date`(im Format YYYY-MM-DD, für den selben Tag gleicher Wert für beide Parameter)

`temperature_2m` (Temperature, 2m über Boden)

`rain`  (Niederschlag in mm)

`snowfall` (Schneefall in cm)

`wind_speed_10m` (Windgeschwindigkeit 10m über Boden)


# Backend

## Server starten + Flask installieren

```
pip install flask
python server.py
```

im Browser: http://127.0.0.1:5000

## Ordnerstruktur

```
projekt/
│
├── server.py
└── templates/
    └── index.html
```

## Datenfluss

```
Browser (HTML Formular)
        │
        │  POST request
        ▼
Flask Backend (server.py)
        │
        │  INSERT
        ▼
SQLite Datenbank
        │
        │  SELECT
        ▼
Flask Backend
        │
        │  render_template()
        ▼
HTML Seite zeigt Daten
```

## Backend-Logic (server.py)





Frontend Beispiel:









