# 🎯 ChallengeMyself

Eine Webanwendung zur persönlichen Ziel- und Aufgabenverfolgung. Verfolge deine Fortschritte bei verschiedenen Aktivitäten und visualisiere deine Erfolge mit interaktiven Diagrammen.

---

## Features

- **Challenge-Verwaltung**: Erstelle und verwalte verschiedene Challenges (z.B. "Fit für den Sommer", "Laufen", "Lernen")
- **Flexible Datenerfassung**: Jede Challenge kann unterschiedliche Daten erfassen (km, Minuten, Anzahl, etc.)
- **Zieltracking**: Definiere Ziele und Zeiträume für jede Challenge
- **Interaktive Visualisierungen**: Visualisiere deine Sessions mit Liniendiagrammen und Säulendiagrammen
- **Intensitäts-Filter**: Filtere deine Daten nach Intensität (gemütlich, mittel, stark)
- **Lokal gespeichert**: Alle Daten werden lokal im JSON-Format gespeichert

---

## Technologie-Stack

### Backend (Python)
- **Python 3.14+** – Hauptprogrammiersprache
- **Flask** – Web-Framework für HTML-Rendering & API
- **Pandas** – Datenverarbeitung und Diagramm-Erstellung
- **Plotly** – Interaktive Diagramme

### Frontend (Minimal)
- **Jinja2-Templates** – HTML vom Backend generiert
- **Bootstrap 5** – Responsive UI
- **Plotly.js** – Interaktive Charts im Browser

### Datenspeicherung
- **JSON-Dateien** – Lokal im `backend/data/`

---

## Schnellstart

### 1️⃣ Voraussetzungen
- Python 3.10+
- Node.js & npm (LTS)

### 2️⃣ Installation

```powershell
# Backend-Umgebung
python -m venv backend/venv
backend\venv\Scripts\activate
pip install -r backend/requirements.txt

# Frontend-Abhängigkeiten
cd frontend
npm install
cd ..
```

### 3️⃣ Anwendung starten

**Einfach mit einem Befehl:**
```powershell
.\start.ps1
```

Die App öffnet sich automatisch unter: `http://localhost:5000`

Warte ~5 Sekunden beim ersten Start!

---

## Projektstruktur

```
ChallengeMyself/
├── start.ps1                    # Start-Script (alles mit einem Befehl!)
├── README.md                    # Diese Dokumentation
├── backend/
│   ├── app.py                   # Flask-Hauptanwendung
│   ├── config.py                # Konfiguration
│   ├── requirements.txt          # Python-Dependencies
│   ├── templates/               # HTML-Templates (vom Backend generiert)
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── challenge_detail.html
│   │   └── plot.html
│   ├── data/                    # JSON-Speicherung
│   ├── models/                  # Python-Datenmodelle
│   ├── storage/                 # Persistierungs-Logik
│   └── utils/                   # Hilfsfunktionen
├── frontend/
│   ├── package.json
│   └── src/
│       └── App.js               # React-Einstiegspunkt
└── venv/                        # (wird erstellt)
```

---

## Unterstützte Activities

| Kategorie | Activities |
|-----------|-----------|
| **Sport** | Laufen, Radfahren, Spazieren, Schwimmen, Workout, Liegestütze |
| **Lernen** | Lesen, Lernen |
| **Schlaf** | Schlaf |
| **Medien** | Bildschirmzeit |
| **Konsum** | Wasser, Alkohol, Rauchen |
| **Wohlbefinden** | Stimmung, Stress |

---

## Verwendungsbeispiel

### 1. Challenge erstellen
- Name: "Marathon vorbereitung"
- Activity: "Laufen"

### 2. Ziel setzen
- "5 km pro Tag"
- Zielwert: 5
- Zeitraum: täglich

### 3. Sessions hinzufügen
- Datum: Heute
- Uhrzeit: 18:30
- Distanz: 5.2 km
- Dauer: 45 Minuten
- Intensität: mittel

### 4. Visualisieren
- Wähle "Distanz (km)" & "Dauer (min)"
- Filter nach Intensität
- Wechsle Chart-Typ (Linie / Säule)

---

## Architektur

### Backend als Haupt-Interface
- **HTML-Rendering mit Jinja2**: Alle Seiten werden vom Python-Backend generiert
- **Formular-Management**: Challenge-Erstellung, Goals, Sessions – alles in Python
- **Business-Logic in Python**: Datenverarbeitung, Persistierung, Visualisierung

### Minimal Viable React
- React wird nur für **Plotly-Visualisierungen** verwendet
- Keine komplexe State-Management, keine React-Router
- Navigation erfolgt über HTML-Links

### Datenfluss
```
Browser → Flask (HTML-Templates) → Benutzer füllt Form
User-Input → Backend (POST-Form) → JSON-Speicherung
Visualisierung → Plotly-API → React rendert Chart
```

**Warum?** Python bietet bessere Datenverarbeitung (Pandas), Persistierung und simplere Business-Logic als React.

---

## FAQ

**F: Wo sind meine Daten?**
A: In `backend/data/` als `.json`-Dateien (keine Cloud!)

**F: Kann ich Challenges löschen?**
A: Aktuell nur manuell: Lösche die `.json`-Datei in `backend/data/`

**F: Warum Python überall?**
A: Bessere Datenverarbeitung, lokale Speicherung, einfachere Business-Logic

**F: Warum noch React?**
A: Plotly-Visualisierungen brauchen JavaScript

---

## Troubleshooting

**Port bereits in Verwendung:**
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**venv-Probleme:**
```powershell
backend\venv\Scripts\activate
pip install -r backend/requirements.txt
```

**npm-Fehler:**
```powershell
cd frontend
rm -r node_modules package-lock.json
npm install
```

**PS1-Script wird nicht ausgeführt:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## JSON-Format

Jede Challenge wird als `.json` gespeichert:

```json
{
  "name": "Laufen",
  "activity_type": "Laufen",
  "goal": {
    "description": "5 km täglich",
    "target": 5.0,
    "period": "täglich"
  },
  "sessions": [
    {
      "date": "2026-02-02",
      "time": "18:30",
      "values": {
        "distanz_km": 5.2,
        "dauer_min": 45,
        "intensitaet": "mittel"
      }
    }
  ]
}
```

---

## Roadmap

- ✅ Challenges verwalten
- ✅ Sessions erfassen
- ✅ Ziele setzen
- ✅ Visualisierungen
- ✅ Backend als Haupt-Interface
- 🔄 Sessions löschen/bearbeiten
- 🔄 Datenbankunterstützung
- 🔄 Export-Funktionen
- 🔄 Mobile-App

---

**Happy Tracking!**
