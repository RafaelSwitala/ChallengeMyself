# ChallengeMyself

## Projektbeschreibung
ChallengeMyself ist eine Web-App zur persönlichen Ziel- und Aufgabenverfolgung.  
Benutzer können **verschiedene Challenges** (z. B. Lernen, Laufen, Rauchen reduzieren) erstellen und ihre Fortschritte verfolgen.  

- Jede Challenge kann Sessions/Einträge mit Datum, Dauer, Menge etc. enthalten.  
- Ziele/Target-Werte für Challenges sind definierbar.  
- Backend speichert Daten lokal in JSON-Dateien.  
- Frontend visualisiert und verwaltet die Daten.  

---

## Technologien & Versionen

### Backend
- Python 3.14.0
- Flask (REST-API)
- flask-cors (für Cross-Origin Requests)
- Python-Bibliotheken siehe `backend/requirements.txt`

### Frontend
- React 19.2.3
- React-Bootstrap 2.10.10
- Bootstrap 5.3.8
- React-Scripts 5.0.1
- Node.js & npm (aktuelle LTS-Versionen)
- Optional: `concurrently` für gleichzeitiges Starten von Backend & Frontend

### Betriebssystem & IDE
- Windows 11
- Visual Studio Code mit Python-Erweiterung

---

## Backend Setup

### Virtuelle Umgebung erstellen
```powershell
python -m venv venv



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
