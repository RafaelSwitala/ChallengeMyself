# ChallengeMyself

Eine Python-basierte Webanwendung zur Verfolgung persönlicher Ziele, Aktivitäten und Fortschritts. Überwache deine Fitness-Routinen, Lernziele und Gesundheitskennzahlen mit interaktiven, responsive Visualisierungen.

---

## Funktionen

- **Challenge-Verwaltung**: Erstelle und verwalte mehrere persönliche Challenges (z.B. "Marathon-Training", "Python lernen", "Alkoholkonsum reduzieren")
- **Flexible Datenerfassung**: Jede Challenge kann verschiedene Metriken verfolgen (Distanz, Dauer, Anzahl, Intensität, Wetter, etc.)
- **Ziel-Verfolgung**: Definiere Ziele für jede Challenge, um dich zu motivieren
- **Interaktive Visualisierungen**: Sehe deine Daten mit mehreren Diagrammtypen (Liniendiagramme, Balkendiagramme, Kategoriehäufigkeit)
- **Erweiterte Charting**:
  - Mische Diagrammtypen in einer Ansicht (Linie + Balken gleichzeitig)
  - Duale Y-Achsen für unterschiedliche Skalen
  - Datumsbereichs-Filterung
  - Dynamische Achsen-Skalierungskontrollen
- **Lokale Speicherung**: Alle Daten werden persistent als leicht lesbare JSON-Dateien gespeichert (keine Datenbank notwendig)

---

## Technologie-Stack

### Backend (Python)
- **Python 3.12** - Kernsprache
- **Flask** - REST API Server und HTML-Rendering
- **Pandas** - Datenverarbeitung und -manipulation
- **Plotly** - Interaktive Visualisierungen (Python Backend)
- **Dataclasses** - Saubere Datenmodellierung
- **Logging** - Anwendungs-Logging und Debugging

### Frontend (Minimalistischer Ansatz)
- **React** - UI-Komponentenbibliothek
- **Bootstrap 5** - Responsive Styling
- **Plotly.js** - Interaktives Diagramm-Rendering
- **Fetch API** - Kommunikation mit Backend

### Datenspeicherung
- **JSON-Dateien** - Lokale Dateisystem-Persistierung in `backend/data/`

---

## Schnellstart

### Voraussetzungen

- **Python 3.12** - [Python herunterladen](https://www.python.org/downloads/)
- **Node.js LTS** - [Node.js herunterladen](https://nodejs.org/) (für React Frontend)

### Installation

#### Methode 1: Automatisierte Installation (Empfohlen - Windows)

```powershell
# Zum Projektverzeichnis navigieren
cd c:\Users\<Benutzername>\Desktop\PProjekte\ChallengeMyself

# Installationsskript ausführen
.\install.ps1
```

Das Skript führt automatisch aus:
1. Python-Version überprüfen
2. Virtuelle Umgebung erstellen
3. Python-Abhängigkeiten installieren
4. Node.js-Pakete installieren

#### Methode 2: Manuelle Installation

**Backend-Setup:**
```powershell
# Virtuelle Umgebung erstellen
python -m venv backend\venv

# Virtuelle Umgebung aktivieren
backend\venv\Scripts\activate

# Python-Pakete installieren
pip install -r backend\requirements.txt
```

**Frontend-Setup:**
```powershell
# Node.js-Pakete installieren
cd frontend
npm install
cd ..
```

### Anwendung ausführen

#### Option 1: Schnellstart (Empfohlen)
```powershell
.\start.ps1 # ---------------------------------------------------------------------------------------------------- Hier starten
```

Das macht automatisch:
1. Aktiviert Python-Virtualumgebung
2. Startet Flask-Backend auf `http://localhost:5000`
3. Startet React-Frontend auf `http://localhost:3000`
4. Öffnet die App im Standard-Browser

#### Option 2: Manueller Start

**Terminal 1 - Backend:**
```powershell
backend\venv\Scripts\activate
python backend\app.py
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm start
cd ..
```

Die Anwendung ist erreichbar unter `http://localhost:5000`.

---

## Projektstruktur

```
ChallengeMyself/
├── start.ps1                        # Schnellstart-Automatisierung
├── install.ps1                      # Automatisierte Installation
├── README.md                        # Diese Dokumentation
│
├── backend/                         # Python Flask Backend
│   ├── app.py                       # Flask REST API Server
│   ├── config.py                    # Konfiguration
│   ├── requirements.txt             # Python-Abhängigkeiten
│   ├── models/                      # Datenmodelle
│   ├── storage/                     # JSON-Persistierung
│   ├── utils/                       # Hilfsfunktionen
│   ├── templates/                   # HTML-Vorlagen
│   ├── static/                      # CSS-Dateien
│   ├── data/                        # JSON-Datendateien
│   └── logs/                        # Anwendungs-Logs
│
└── frontend/                        # React Frontend
    ├── package.json
    └── src/                         # React-Komponenten
```

---

## Wichtigste Python-Konzepte

Dieses Projekt demonstriert folgende Python-Konzepte:

### 1. **Fehlerbehandlung (Fehlerbehandlung)**
- `try-except-else-finally` Blöcke im gesamten Backend
- Exception-Logging mit Tracebacks

### 2. **Logging (Protokollierung)**
- Benutzerdefiniertes Logging-Setup in `backend/utils/logger.py`
- DEBUG, INFO, WARNING, ERROR Logging-Level

### 3. **Funktionen (Funktionen)**
- Reine Funktionen mit Type Hints
- Rückgabewert-Dokumentation
- Beispiele: `filter_by_date_range()`, `calculate_hidden_fields()`

### 4. **Klassen & Instanziierung (Klassen)**
- Dataclass-Verwendung: `Challenge`, `Session`, `Goal`, `Field`
- Instanzmethoden und Klassenvariablen
- Beispiele in `backend/models/*.py`

### 5. **Bibliotheks-Importe (Bibliotheken)**
- Flask - REST API
- Pandas - Datenverarbeitung
- Plotly - Visualisierung
- JSON - Datenpersistierung

---

## Unterstützte Aktivitäten

| Kategorie | Aktivitäten |
|-----------|-----------|
| **Sport** | Laufen, Radfahren, Spazieren, Schwimmen, Workout |
| **Lernen** | Lesen, Studieren |
| **Gesundheit** | Wasser, Alkohol, Stimmung, Stress |
| **Spezial** | Ereignisse |

---

## API-Endpunkte

### Challenges
- `GET /challenges` - Alle Challenges auflisten
- `POST /challenges` - Neue Challenge erstellen
- `GET /challenges/<name>` - Challenge-Details abrufen

### Sessions
- `POST /challenges/<name>/sessions` - Neue Session hinzufügen

### Ziele
- `POST /challenges/<name>/goal` - Ziel setzen
- `POST /challenges/<name>/goal?delete=true` - Ziel löschen

### Visualisierung
- `GET /challenges/<name>/plot?fields=...&date_from=...&date_to=...` - Diagrammdaten abrufen

### Aktivitäten
- `GET /activities` - Alle Aktivitäten auflisten
- `GET /activities/<name>` - Aktivitätsfelder abrufen

---

## Fehlerbehandlung

**Python nicht gefunden**: Installiere Python 3.12 oder füge es zum system PATH hinzu

**Port 5000 in Verwendung**: Ändere `PORT` in `backend/config.py`

**Diagramme laden nicht**: Browsercache leeren, `backend/logs/app.log` überprüfen

**npm nicht gefunden**: Installiere Node.js LTS

---

## Lizenz

Bildungsprojekt für "Projekt: Einführung in die Programmierung mit Python"

---

**Version:** 1.0 (Python Plotly Backend)  
**Python:** 3.12  
**Status:** Produktionsbereit
