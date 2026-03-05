import requests

# URL Berlin => Temperatur, Schnee, Regen, Wind

url = 'https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=uv_index_max&hourly=temperature_2m,rain,snowfall,wind_speed_10m&timezone=Europe%2FBerlin&utm_source=chatgpt.com'

# Senden der GET-Anfrage
response = requests.get(url)

# Überprüfen, ob die Anfrage erfolgreich war
if response.status_code == 200:
    # Parse die JSON-antwort
    data = response.json()
    
    # Extrahieren der Temperatur für eine bestimmte "hourly" Stunde
    # Beispiel: für die Stunde 14:00 (2:00 PM)
    # Die "hourly" Daten sind in Stunden-Verzögerung, daher müssen wir die Stunde auf Stunden-Index in der Datenliste umrechnen
    hourly_data = data['hourly']
    hour_index = 10  # Stunde 14:00 (2:00 PM)
    temperature = hourly_data['temperature_2m'][hour_index]
    rain = hourly_data['rain'][hour_index]
    snowfall = hourly_data['snowfall'][hour_index]
    wind = hourly_data['wind_speed_10m'][hour_index]
    
    print(f"Temperature at hour {hour_index}: {temperature}°C")
    print(f"Rain: {rain}mm, Snowfall: {snowfall}cm, Wind: {wind} km/h")

else:
    print(f"Fehler: Die Anfrage wurde nicht erfolgreich abgearbeitet. Statuscode: {response.status_code}")