# Projektdokumentation
Kleidungsempfehlung basierend auf Wetterdaten

## 1. Einleitung

Im Rahmen dieses Projekts wird eine Webanwendung entwickelt,
die auf Basis aktueller Wetterdaten eine passende
Kleidungsempfehlung für den Benutzer generiert.

Die Anwendung ruft Wetterdaten über eine externe API ab,
verarbeitet diese Daten und vergleicht sie mit
vordefinierten Regeln in einer SQL-Datenbank.

Anhand dieser Regeln wird eine geeignete Kleidung
empfohlen und im Webbrowser angezeigt.

## 2. Projektanforderungen
Ziel des Projekts ist die Entwicklung einer Anwendung,
die Wetterinformationen automatisch verarbeitet
und dem Benutzer eine passende Kleidungsempfehlung gibt.

Der Benutzer gibt eine Stadt, ein Datum und eine Uhrzeit ein und erhält eine
Empfehlung basierend auf Temperatur, Regen und Wind.

## 3. Projektteam

Das Projekt wird von vier Teammitgliedern umgesetzt.

| Rolle | Aufgabe | Name |
|------|------|------|
| Backend / API | Wetter API anbinden und Daten verarbeiten | Niklas |
| Datenbank | SQLite Datenbank und Regeln erstellen | Vahit |
| Frontend | Weboberfläche mit HTML und CSS | Theresa |
| Integration / Tests / Dokumentation | Komponenten verbinden und dokumentieren | Kseniia |


## 4. Verwendete Technologien

Für die Entwicklung der Anwendung werden folgende Technologien verwendet:

Frontend
- HTML
- CSS

Backend
- Webserver mit Python und Flask

Datenbank
-SQLite
API
- externe Wetter API (Open Meteo) zur Abfrage aktueller Wetterdaten

Versionskontrolle
- Git
- GitHub

## 5. Systemarchitektur

Die Anwendung besteht aus drei Hauptkomponenten:

Frontend  
Die Benutzeroberfläche wird mit HTML und CSS erstellt.
Der Benutzer gibt eine Stadt, ein Datum und eine Uhrzeit ein.

Backend  
Das Backend verarbeitet die Anfrage und ruft
Wetterdaten über eine externe API ab.

Datenbank  
Die Datenbank speichert Regeln für verschiedene
Wetterbedingungen sowie passende Kleidungsempfehlungen.

Der Ablauf der Anwendung ist wie folgt:

1. Benutzer gibt eine Stadt, Datum und Uhrzeit ein
2. Anfrage wird an das Backend gesendet
3. Backend ruft Wetterdaten über die API ab
4. Wetterdaten werden verarbeitet
5. Datenbank wird nach passenden Regeln durchsucht
6. Kleidungsempfehlung wird an das Frontend zurückgegeben
7. Ergebnis wird im Browser angezeigt

### 5.1 Use-Case-Diagramm

Das Use-Case-Diagramm zeigt die Interaktion zwischen dem Benutzer und dem System „Kleidungsempfehlung“.

- Der Benutzer gibt die notwendigen Informationen ein: Stadt, Datum und Uhrzeit.  
- Das System ruft automatisch die Wetterdaten über die Open Meteo API ab, verarbeitet diese Daten, sucht in der Datenbank nach passenden Regeln und generiert eine Kleidungsempfehlung.  
- Abschließend wird die Empfehlung dem Benutzer im Webbrowser angezeigt.

**Abbildung: Use-Case-Diagramm der Anwendung**  

![Use-Case-Diagramm](use_case_diagramm.png)

### 5.2 Activity-Diagramm

Das Activity-Diagramm zeigt den detaillierten Ablauf innerhalb des Systems:

- Start: Benutzer gibt Informationen ein  
- Entscheidung: Wetterdaten abrufen  
- Verarbeitung: Regeln prüfen  
- Generierung der Kleidungsempfehlung  
- Ende: Empfehlung anzeigen

Dieses Diagramm visualisiert die Schritte und Entscheidungen, die automatisch vom System durchgeführt werden, und zeigt die Logik hinter der Generierung der Empfehlungen.

**Abbildung: Activity-Diagramm der Anwendung**  

![Activity-Diagramm](activity_diagramm.png)

## 6. Datenbank
- DB Browser for SQLite: Zur visuellen Verwaltung und zum Testen der SQL-Befehle. 
- Das Projekt umfasst die Erstellung einer relationalen Datenbank zur automatisierten Kleidungsempfehlung basierend auf Wetterdaten. Das Ziel war es, eine Struktur zu schaffen, die nicht nur einfache Temperaturen berücksichtigt, sondern auch komplexe Szenarien wie Extremhitze, Regen und Schnee.
- Erstellung der Tabellen mit CREATE TABLE
- Vollständige Bestandsliste:
- SELECT k.id, k.name, k.kategorie, r.min_temp, r.max_temp, r.wetter_typ 
  FROM kleidung k
  LEFT JOIN wetter_regeln r ON k.id = r.kleidung_id;
  
- Datenintegrität: Verwendung von UNIQUE-Constraints und ON DELETE CASCADE-Regeln.
  
  .CREATE TABLE kleidung (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE, -- Hier ist der Constraint
    kategorie TEXT
   );
  
  .CREATE TABLE wetter_regeln (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ...
    kleidung_id INTEGER,
    FOREIGN KEY (kleidung_id) REFERENCES kleidung(id) ON DELETE CASCADE
   );

## 7. Backend und API

## 8. Frontend

## 9. Integration

## 10. Tests

## 11. Fehlerbehandlung

## 12. Installation

## 13. Fazit
