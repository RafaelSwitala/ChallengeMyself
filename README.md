# ChallengeMyself

## Projektbeschreibung
ChallengeMyself ist eine Web-App zur persönlichen Ziel- und Aufgabenverfolgung.  
Benutzer können **verschiedene Challenges** (z. B. Lernen, Laufen, Rauchen reduzieren) erstellen und ihre Fortschritte verfolgen.

- Jede Challenge kann Sessions/Einträge mit Datum, Dauer, Menge etc. enthalten.  
- Ziele/Target-Werte für Challenges sind definierbar.  
- Backend speichert Daten lokal in JSON-Dateien.  
- Frontend visualisiert und verwaltet die Daten, inklusive interaktiver Plots mit Plotly.

---

## Technologien & Versionen

### Backend
- Python 3.14.0  
- Flask (REST-API)  
- flask-cors (für Cross-Origin Requests)  
- Pandas, NumPy, Plotly  
- Backend-Abhängigkeiten siehe `backend/requirements.txt`  

### Frontend
- React 19.2.3  
- React-Bootstrap 2.10.10  
- Bootstrap 5.3.8  
- React-Scripts 5.0.1  
- Node.js & npm (aktuelle LTS-Versionen)  
- `react-plotly.js` & `plotly.js` für interaktive Diagramme  

### Betriebssystem & IDE
- Windows 11  
- Visual Studio Code mit Python-Erweiterung  

---

## Backend Setup

### Virtuelle Umgebung erstellen
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt




| Technologie     | Version                |
| --------------- | ---------------------- |
| Python          | 3.14.0                 |
| Flask           | siehe requirements.txt |
| React           | 19.2.3                 |
| React-Bootstrap | 2.10.10                |
| Bootstrap       | 5.3.8                  |
| Node.js         | aktuelle LTS           |
| npm             | aktuelle LTS           |
| react-scripts   | 5.0.1                  |



| Activity    | Was wird getrackt                      | Beispiel-Ziel                |
| ----------- | -------------------------------------- | ---------------------------- |
| Laufen      | Datum, km, Dauer, Pausen               | 5 km pro Tag                 |
| Radfahren   | Datum, km, Dauer, Pausen               | 50 km pro Woche              |
| Lesen       | Datum, Minuten gelesen, Seiten         | 1000 Seiten pro Monat        |
| Lernen      | Datum, Minuten                         | 100 Stunden pro Monat        |
| Liegestütze | Datum, Anzahl, Sets                    | Wöchentlich 10 mehr          |
| Rauchen     | Datum, Zigaretten                      | 2 Zigaretten weniger pro Tag |
| Schlaf      | Datum, Stunden                         | 8 Stunden Schlaf pro Nacht   |
| Wasser      | Datum, ml                              | 2 Liter pro Tag              |
| Ernährung   | Datum, Mahlzeiten, Kalorien (optional) | 2000 kcal pro Tag            |
| Meditation  | Datum, Minuten                         | 10 Minuten täglich           |



### Backend starten
cd backend
python app.py

### Frontend starten
cd frontend
npm install
npm start

### Interaktive Plots
Das Backend erzeugt Plotly-kompatibles JSON, das im Frontend über react-plotly.js interaktiv angezeigt wird.

Benutzer können:

Beliebige Felder per Checkbox auswählen (z. B. distanz_km, dauer_min, schritte_anzahl)

Nach Intensität filtern (gemuetlich, stark etc.)

---

## Beispiele: Backend testen mit cURL & Plot-URLs

### 1. Neue Challenge erstellen
```bash
curl -X POST http://localhost:5000/challenges \
-H "Content-Type: application/json" \
-d '{
  "name": "Wandermarathon",
  "activity": "Spazieren"
}'

---

{
  "name": "Wandermarathon",
  "activity_type": "Spazieren",
  "goal": null,
  "sessions": []
}

---

curl -X POST http://localhost:5000/challenges/Wandermarathon/sessions \
-H "Content-Type: application/json" \
-d '{
  "date": "2026-01-01",
  "time": "09:00",
  "values": {
    "distanz_km": 10,
    "dauer_min": 150,
    "schritte_anzahl": 16000,
    "intensitaet": "gemuetlich"
  }
}'

---

curl -X POST http://localhost:5000/challenges/Wandermarathon/goal \
-H "Content-Type: application/json" \
-d '{
  "description": "Wandermarathon im Wald nächsten Sommer",
  "target": "",
  "period": "4 mal in der Woche"
}'


## Logging & Fehlerbehandlung
Das Backend verwendet ein zentrales, konfigurierbares Logging-System, um Fehler, Warnungen und Debug-Informationen ausschließlich in Logdateien zu schreiben (keine Console-Ausgabe).

### 1. Logging-Konfiguration
LOG_ENABLED = True          # Logging an / aus
LOG_LEVEL = "DEBUG"        # DEBUG | INFO | WARNING | ERROR
LOG_DIR = "logs"           # Log-Verzeichnis
LOG_FILE = "app.log"       # Logdatei

- Logging kann vollständig deaktiviert werden (LOG_ENABLED = False)
- Log-Level steuert die Detailtiefe der Einträge
- Logs werden rotierend gespeichert (max. ~2 MB pro Datei, 5 Backups)

### 2. Log-Dateien
Bei aktiviertem Logging werden Logdateien automatisch erzeugt unter:
backend/logs/app.log

Hinweis: Die Flask-Konsole bleibt bewusst ruhig – alle Logs gehen ausschließlich in die Datei.

### 3. Fehlerbehandlung (Backend)
- Validierungsfehler (Client-Fehler, 4xx)
- Beispiele: Fehlende Pflichtfelder, Ungültige Activity, Nicht existierende Challenge
- HTTP-Statuscodes:
- 400 Bad Request
- 404 Not Found
- Diese Fehler werden als WARNING geloggt.

- Laufzeitfehler (Server-Fehler, 5xx)
- Unerwartete Fehler im Backend (z. B. Parsing-, IO- oder Pandas-Fehler) werden abgefangen.
- Beispiele: Ungültiges Datum, Falscher Datentyp in values, Schreibfehler beim Speichern einer JSON-Datei
- 500 Internal Server Error
- Diese Fehler werden als ERROR inklusive Stacktrace in der Logdatei gespeichert.
