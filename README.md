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
