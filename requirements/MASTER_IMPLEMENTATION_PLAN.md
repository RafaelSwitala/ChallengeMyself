# ChallengeMyself - Umfassender Implementierungsplan

**Datum**: März 2026
**Status**: Planungsphase
**Ziel**: Vollständige Restaurierung der Anwendung mit Best Practices und modernen Design Patterns

---

## 📋 INHALTSVERZEICHNIS

1. [Executive Summary](#executive-summary)
2. [Architektur-Übersicht](#architektur-übersicht)
3. [Backend - Python/Flask](#backend---pythonflask)
4. [Frontend - React](#frontend---react)
5. [Kernkonzepte: Activities, Goals, Fields](#kernkonzepte-activities-goals-fields)
6. [Best Practices & Design Patterns](#best-practices--design-patterns)
7. [Implementierungsreihenfolge](#implementierungsreihenfolge)
8. [Code-Standards](#code-standards)

---

## Executive Summary

### Projektvisioning

Die Anwendung **ChallengeMyself** ist ein **persönliches Goal-Tracking und Activity-Management System**, das Benutzer dabei hilft:
- Persönliche Herausforderungen zu definieren (Joggen, Lernen, Gesundheit, etc.)
- Aktivitäten mit flexiblen, aktivitätsspezifischen Metriken zu erfassen
- Intelligente Ziele zu setzen und Fortschritt zu verfolgen
- Datenvisualisierungen zu nutzen zur Analyse und Motivation

### Neues Scope (aus Requirements)

Das System wird erweitert von **22 auf 40+ Aktivitäten** mit:
- **12 verschiedene Goal-Typen** (nicht nur "Ziel X pro Periode")
- **85+ vordefinierte Fields** mit standardisierter Benennung
- Bessere Feldorganisation für Wiederverwendbarkeit
- Strikte Typsicherheit (auch im Python Backend)
- Effiziente Datenberechnung (Durchschnitte, Streak, etc.)

### Key Decisions

✅ **Backend**: Python + Flask (REST API)
✅ **Frontend**: React ohne TypeScript (wie gewünscht)
✅ **Datenspeicherung**: JSON Files (lokal im `data/` Ordner)
✅ **OOP-Ansatz**: Klassen, Interfaces/Dataclasses, Enums
✅ **Design Patterns**: Registry, Factory, Builder, Strategy
✅ **Wiederverwendbarer Code**: Maximale Modularität
✅ **Best Practices**: Type Hints (Python), Clean Code, Separation of Concerns

---

## Architektur-Übersicht

### Gesamter Datenfluss

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend                            │
│  (3000) - Komponenten: App, ChallengeDetail, Stats, Forms   │
└────────────┬────────────────────────────────────────────────┘
             │ HTTP/JSON (CORS enabled)
             │
┌────────────▼────────────────────────────────────────────────┐
│               Flask REST API Backend (5000)                  │
├──────────────────────────────────────────────────────────────┤
│  ┌─ Routes Layer                                             │
│  │  ├─ /challenges (CRUD)                                   │
│  │  ├─ /activities (Registry + Field Definitions)           │
│  │  ├─ /goals (Create/Calculate Progress)                   │
│  │  └─ /plot (Advanced Filtering & Visualization)           │
│  │                                                            │
│  ├─ Service/Domain Logic Layer                              │
│  │  ├─ ActivityRegistry (Factory Pattern)                   │
│  │  ├─ GoalProgressCalculator (Strategy Pattern)            │
│  │  ├─ FieldValidator                                        │
│  │  └─ DataAggregator (avg, streak, velocity)               │
│  │                                                            │
│  ├─ Models Layer (OOP)                                      │
│  │  ├─ Activity (dataclass)                                  │
│  │  ├─ Challenge (dataclass)                                 │
│  │  ├─ Session (dataclass)                                   │
│  │  ├─ Goal (dataclass)                                      │
│  │  ├─ Field (dataclass)                                     │
│  │  └─ Enums (ActivityType, GoalType, FieldType, etc.)      │
│  │                                                            │
│  └─ Storage Layer                                            │
│     └─ JSON FileStorage (load, save, list)                  │
│        └─ data/*.json (Challenge Persistierung)             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Separating Concerns - 3-Schicht-Architektur

**Schicht 1: Web Layer (Routes/API)**
- HTTP Request/Response Handling
- CORS Management
- Error Handling & Status Codes
- Smart Response Routing (HTML vs JSON)

**Schicht 2: Business Logic Layer (Services/Domains)**
- Activity Registry & Definitions
- Goal Calculations & Evaluation
- Data Validation & Transformation
- Filtering & Aggregation Logic

**Schicht 3: Data Layer (Models & Storage)**
- Data Models (dataclasses)
- Type Definitions (Enums)
- JSON File Persistence
- Data Serialization

---

## Backend - Python/Flask

### 1. Zielstrukturen & Ordnerorganisation

```
backend/
├── app.py                              # Haupteinstiegspunkt, Routes
├── config.py                           # Globale Konfiguration
├── requirements.txt                    # Dependencies
│
├── models/                             # 🔹 Data Models Layer
│   ├── __init__.py
│   ├── activity.py                    # Activity (dataclass)
│   ├── challenge.py                   # Challenge (dataclass)
│   ├── session.py                     # Session (dataclass)
│   ├── goal.py                        # Goal (dataclass)
│   ├── field.py                       # Field (dataclass)
│   ├── enums.py                       # Alle Enums (ActivityType, GoalType, etc.)
│   └── types.py                       # Custom Type Aliases & TypedDicts
│
├── domains/                            # 🔹 Business Logic / Services Layer
│   ├── __init__.py
│   │
│   ├── activities/
│   │   ├── __init__.py
│   │   ├── registry.py                # ActivityRegistry (Factory Pattern)
│   │   ├── definitions.py             # Activity Definitions (alle 40+ Aktivitäten)
│   │   └── field_mappings.py          # Field Config für jede Aktivität
│   │
│   ├── goals/
│   │   ├── __init__.py
│   │   ├── calculator.py              # GoalProgressCalculator (Strategy Pattern)
│   │   ├── strategies.py              # 12 Goal-Type Strategien
│   │   ├── validator.py               # Goal-Validierung
│   │   └── evaluator.py               # Goal Status Evaluation
│   │
│   ├── fields/
│   │   ├── __init__.py
│   │   ├── definitions.py             # Alle 85+ Field-Definitionen (zentral)
│   │   ├── validator.py               # Field Value Validation
│   │   ├── calculator.py              # Hidden Field Calculation (avg, streak, etc.)
│   │   └── aggregator.py              # Data Aggregation (sum, average, etc.)
│   │
│   └── data/
│       ├── __init__.py
│       ├── filterer.py                # Data Filtering Logic
│       └── transformer.py             # Data Transformation (JSON ↔ Model)
│
├── storage/                            # 🔹 Persistence Layer
│   ├── __init__.py
│   ├── json_storage.py                # JSON File Operations (CRUD)
│   ├── serializer.py                  # Serialization (Model → JSON)
│   └── deserializer.py                # Deserialization (JSON → Model)
│
├── api/                                # 🔹 Web Layer / Routes
│   ├── __init__.py
│   ├── routes.py                      # API Route Definitions (@app.route)
│   ├── handlers.py                    # Route Handler Functions
│   ├── middleware.py                  # CORS, Error Handling
│   └── responses.py                   # Response Formatters
│
├── utils/                              # 🔹 Utility Functions
│   ├── __init__.py
│   ├── logger.py                      # Logging Setup
│   ├── date_utils.py                  # Date/Time Utilities
│   ├── validators.py                  # General Validators
│   └── text_normalizer.py             # Text Processing
│
├── data/                               # 🔹 Persistent Data
│   └── *.json                         # Challenge JSON Files
│
├── logs/                               # 🔹 Runtime Logs
│   └── app.log
│
└── venv/                               # Virtual Environment
```

### 2. Modelle - Dataclass Pattern (Python)

```python
# models/enums.py
from enum import Enum

class ActivityType(Enum):
    """40+ Aktivitätstypen"""
    JOGGING = "Joggen"
    CYCLING = "Radfahren"
    WALKING = "Spazieren"
    SWIMMING = "Schwimmen"
    WORKOUT = "Workout"
    SLEEPING = "Schlaf"
    READING = "Lesen"
    LEARNING = "Lernen"
    EATING = "Ernährung"
    # ... 30+ weitere

class GoalType(Enum):
    """12 Goal-Typen"""
    MORE_THAN = "a"           # Mehr als X
    LESS_THAN = "b"           # Weniger als X
    AVOID = "c"               # Ganz vermeiden
    FREQUENCY_EXACT = "d"     # Genau X-mal pro Periode
    FREQUENCY_MIN = "e"       # Mindestens X-mal
    FREQUENCY_MAX = "f"       # Maximal X-mal
    STREAK = "g"              # X Tage in Folge
    INCREASE_DAILY = "h"      # Täglich X mehr bis Y
    DECREASE_DAILY = "i"      # Täglich X weniger bis Y
    AVERAGE_ABOVE = "j"       # Durchschnitt über X
    AVERAGE_BELOW = "k"       # Durchschnitt unter X
    CONDITIONAL = "l"         # X erreichen unter Bedingung Y

class GoalPeriod(Enum):
    """Zeiträume für Goals"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    DATE_RANGE = "date_range"

class FieldType(Enum):
    """Feldtypen"""
    NUMBER = "number"
    INTEGER = "integer"
    ENUM = "enum"
    TEXT = "text"
    DATE = "date"
    BOOLEAN = "boolean"

class ChartType(Enum):
    """Diagrammtypen"""
    LINE = "line"
    BAR = "bar"
    BOTH = "both"
    ENUM_BAR = "enum_bar"
    NONE = "none"
    VALUE = "value"

# models/field.py
from dataclasses import dataclass
from typing import Optional, List, Any
from enum import Enum

@dataclass
class Field:
    """Field Definition - standardisierte Feldvorlage"""
    key: str                                    # z.B. "distance_km"
    label: str                                  # z.B. "Distanz"
    unit: Optional[str] = None                  # z.B. "km", "min", "%"
    field_type: FieldType = FieldType.NUMBER   # Datentyp
    chart_type: ChartType = ChartType.LINE     # Visualisierungstyp
    required: bool = False                      # Pflichtfeld?
    hidden: bool = False                        # Berechnetes Feld (unsichtbar)?
    options: Optional[List[str]] = None        # Enum-Optionen
    description: Optional[str] = None           # Dokumentation
    min_value: Optional[float] = None          # Validation: Minimum
    max_value: Optional[float] = None          # Validation: Maximum
    calculator: Optional[str] = None           # Funktionsreferenz für Hidden Fields

    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """Validiert einen Wert gegen dieses Field"""
        # Typ-Validierung
        # Range-Validierung (min/max)
        # Enum-Validierung
        return True, None

# models/session.py
from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime

@dataclass
class Session:
    """Eine einzelne Erfassung einer Aktivität"""
    date: str                               # ISO 8601: YYYY-MM-DD
    time: str                               # HH:MM
    values: Dict[str, Any]                  # {field_key: value, ...}

    def get_timestamp(self) -> datetime:
        return datetime.fromisoformat(f"{self.date}T{self.time}:00")

# models/goal.py
from dataclasses import dataclass, field as dc_field
from datetime import datetime

@dataclass
class Goal:
    """Ein Ziel für eine Challenge"""
    description: str                       # z.B. "100 km pro Monat joggen"
    variable_reference: str                # Feld zum Tracken: z.B. "distance_km"
    goal_type: GoalType                    # Zieltyp (a-l)
    target: float                          # Zielwert
    period: GoalPeriod                     # Zeitraum
    secondary_target: Optional[float] = None    # Für conditional goals
    secondary_reference: Optional[str] = None   # Für conditional goals
    created_at: datetime = dc_field(default_factory=datetime.now)
    updated_at: datetime = dc_field(default_factory=datetime.now)

    def is_type(self, goal_type: GoalType) -> bool:
        return self.goal_type == goal_type

# models/challenge.py
from dataclasses import dataclass, field as dc_field
from typing import List, Optional

@dataclass
class Challenge:
    """Eine persönliche Challenge mit Sessions und Goal"""
    name: str                              # Eindeutig
    activity_type: ActivityType            # Aktivitätstyp
    sessions: List[Session] = dc_field(default_factory=list)
    goal: Optional[Goal] = None
    created_at: datetime = dc_field(default_factory=datetime.now)
    updated_at: datetime = dc_field(default_factory=datetime.now)

    def add_session(self, session: Session) -> None:
        self.sessions.append(session)
        self.updated_at = datetime.now()

    def get_sessions_for_date_range(self, date_from: str, date_to: str) -> List[Session]:
        # Filtert Sessions nach Datumsbereich
        pass

# models/activity.py
from dataclasses import dataclass
from typing import List

@dataclass
class Activity:
    """Eine Aktivitätsdefinition mit ihren Feldern"""
    type: ActivityType
    fields: List[Field]     # Alle verfügbaren Felder

    def get_required_fields(self) -> List[Field]:
        return [f for f in self.fields if f.required]

    def get_trackable_fields(self) -> List[Field]:
        return [f for f in self.fields if not f.hidden]

    def get_chart_fields(self) -> List[Field]:
        return [f for f in self.fields if f.chart_type != ChartType.NONE]
```

### 3. Registry Pattern - Activity Management

```python
# domains/activities/registry.py
from typing import Dict, Optional
from models import Activity, ActivityType, Field
from .definitions import ACTIVITY_DEFINITIONS
from .field_mappings import ACTIVITY_FIELD_MAPPINGS

class ActivityRegistry:
    """Factory Pattern: Zentrale Registry für alle Aktivitäten"""

    _instance = None  # Singleton
    _activities: Dict[ActivityType, Activity] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """Initialisiert alle Aktivitäten aus Definitionen"""
        for activity_type in ActivityType:
            field_keys = ACTIVITY_FIELD_MAPPINGS.get(activity_type, [])
            fields = [self._get_field(key) for key in field_keys]
            self._activities[activity_type] = Activity(type=activity_type, fields=fields)

    def get_activity(self, activity_type: ActivityType) -> Optional[Activity]:
        """Gibt eine Aktivität zurück"""
        return self._activities.get(activity_type)

    def get_all_activities(self) -> Dict[ActivityType, Activity]:
        """Gibt alle Aktivitäten zurück"""
        return self._activities.copy()

    def get_field(self, activity_type: ActivityType, field_key: str) -> Optional[Field]:
        """Liegt ein bestimmtes Feld in einer Aktivität"""
        activity = self.get_activity(activity_type)
        if not activity:
            return None
        return next((f for f in activity.fields if f.key == field_key), None)

    def _get_field(self, field_key: str) -> Field:
        """Lädt ein Field aus der zentralen Feldefinition"""
        from domains.fields.definitions import FIELD_DEFINITIONS
        return FIELD_DEFINITIONS[field_key]

# domains/activities/field_mappings.py
from models import ActivityType

ACTIVITY_FIELD_MAPPINGS: Dict[ActivityType, List[str]] = {
    ActivityType.JOGGING: [
        "notes",                    # 1
        "distance",                 # 2
        "average_distance",         # 3 (hidden)
        "duration",                 # 6
        "average_duration",         # 7 (hidden)
        "velocity",                 # 8 (hidden - calculated)
        "average_velocity",         # 9 (hidden)
        "movement_intensity",       # 12
        "route_type",               # 13
        "weather",                  # 14
        "energy_level",             # 51
        "average_energy_level",     # 52 (hidden)
    ],
    ActivityType.CYCLING: [
        "notes",
        "distance",
        "average_distance",
        "duration",
        "average_duration",
        "velocity",
        "average_velocity",
        "altitude",
        "movement_intensity",
        "route_type",
        "weather",
        # ...
    ],
    # ... weitere Aktivitäten
}
```

### 4. Field Definitions - Zentrale Feldverwaltung

```python
# domains/fields/definitions.py
from models import Field, FieldType, ChartType
from typing import Dict

FIELD_DEFINITIONS: Dict[str, Field] = {
    # UNIVERSELLE FELDER
    "notes": Field(
        key="notes",
        label="Notizen",
        field_type=FieldType.TEXT,
        chart_type=ChartType.NONE,
        required=False,
        hidden=False,
    ),

    # DISTANZ-FELDER
    "distance": Field(
        key="distance",
        label="Distanz",
        unit="km",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.BOTH,
        required=True,
        hidden=False,
        min_value=0,
    ),
    "average_distance": Field(
        key="average_distance",
        label="Durchschnittliche Distanz",
        unit="km",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        required=False,
        hidden=True,  # 🔹 BERECHNET AUTOMATISCH!
        calculator="calculate_average",  # Funktionsreferenz
    ),

    # INTENSITÄT (ENUM)
    "movement_intensity": Field(
        key="movement_intensity",
        label="Intensität",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["sehr leicht", "leicht", "mittel", "intensiv", "sehr intensiv"],
    ),

    # STIMMUNG (1-10 Scale)
    "mood_value": Field(
        key="mood_value",
        label="Stimmung",
        unit="0-10",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.LINE,
        required=True,
        hidden=False,
        min_value=0,
        max_value=10,
    ),

    # ... weitere 80+ Felder
}

# Hilfsklasse für Feld-Zugriff
class FieldManager:
    """Zentrale Verwaltung aller Feldoperationen"""

    @staticmethod
    def get_field(field_key: str) -> Optional[Field]:
        return FIELD_DEFINITIONS.get(field_key)

    @staticmethod
    def get_all_fields() -> Dict[str, Field]:
        return FIELD_DEFINITIONS.copy()

    @staticmethod
    def get_required_fields() -> List[Field]:
        return [f for f in FIELD_DEFINITIONS.values() if f.required]

    @staticmethod
    def validate_field_value(field_key: str, value: Any) -> tuple[bool, Optional[str]]:
        """Validiert einen Wert gegen sein Field"""
        field = FIELD_DEFINITIONS.get(field_key)
        if not field:
            return False, f"Field '{field_key}' existiert nicht"

        if field.field_type == FieldType.NUMBER:
            if not isinstance(value, (int, float)):
                return False, f"{field.label} muss eine Zahl sein"
            if field.min_value and value < field.min_value:
                return False, f"{field.label} muss mindestens {field.min_value} sein"
            if field.max_value and value > field.max_value:
                return False, f"{field.label} darf maximal {field.max_value} sein"

        elif field.field_type == FieldType.ENUM:
            if value not in field.options:
                return False, f"{field.label} muss eine der folgenden Optionen sein: {', '.join(field.options)}"

        return True, None
```

### 5. Goal Progress Calculator - Strategy Pattern

```python
# domains/goals/calculator.py
from abc import ABC, abstractmethod
from models import Goal, GoalType, GoalPeriod, Session
from typing import List, Dict, Any

class GoalStrategy(ABC):
    """Basisklasse für alle Goal-Berechnungsstrategien"""

    @abstractmethod
    def calculate(
        self,
        sessions: List[Session],
        goal: Goal,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """Berechnet Goal-Progress"""
        pass

# STRATEGIEN FÜR ALLE 12 GOAL-TYPEN

class MoreThanStrategy(GoalStrategy):
    """Ziel: Mehr als X"""

    def calculate(self, sessions: List[Session], goal: Goal, **kwargs) -> Dict[str, Any]:
        # Filter Sessions nach Datumsbereich + Periode
        # Sum values von variable_reference
        # Vergleiche mit target

        total = sum(s.values[goal.variable_reference] for s in sessions
                   if goal.variable_reference in s.values)

        return {
            "value": total,
            "target": goal.target,
            "status": "completed" if total >= goal.target else "in_progress",
            "percentage": min(100, int((total / goal.target) * 100)),
        }

class FrequencyExactStrategy(GoalStrategy):
    """Ziel: Genau X-mal pro Periode"""

    def calculate(self, sessions: List[Session], goal: Goal, **kwargs) -> Dict[str, Any]:
        # Zähle Sessions pro Periode
        # Vergleiche mit target
        pass

class StreakStrategy(GoalStrategy):
    """Ziel: X Tage in Folge Goal erreicht"""

    def calculate(self, sessions: List[Session], goal: Goal, **kwargs) -> Dict[str, Any]:
        # Berechne aktuelle Streak
        # Vergleiche mit target
        pass

class AverageAboveStrategy(GoalStrategy):
    """Ziel: Durchschnitt über X"""

    def calculate(self, sessions: List[Session], goal: Goal, **kwargs) -> Dict[str, Any]:
        values = [s.values[goal.variable_reference] for s in sessions
                 if goal.variable_reference in s.values]

        if not values:
            return {"value": 0, "target": goal.target, "status": "no_data"}

        average = sum(values) / len(values)

        return {
            "value": average,
            "target": goal.target,
            "status": "completed" if average >= goal.target else "in_progress",
        }

# ... weitere Strategien (LessThan, Avoid, FrequencyMin, etc.)

class GoalProgressCalculator:
    """Hauptklasse zum Berechnen von Goal-Progress"""

    _strategies: Dict[GoalType, GoalStrategy] = {
        GoalType.MORE_THAN: MoreThanStrategy(),
        GoalType.LESS_THAN: LessThanStrategy(),
        GoalType.FREQUENCY_EXACT: FrequencyExactStrategy(),
        GoalType.STREAK: StreakStrategy(),
        GoalType.AVERAGE_ABOVE: AverageAboveStrategy(),
        GoalType.AVERAGE_BELOW: AverageBelowStrategy(),
        # ... weitere
    }

    @staticmethod
    def calculate_progress(
        sessions: List[Session],
        goal: Goal,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """Berechnet Goal-Progress mit der richtigen Strategie"""

        if goal.goal_type not in GoalProgressCalculator._strategies:
            raise ValueError(f"Unbekannter Goal-Typ: {goal.goal_type}")

        strategy = GoalProgressCalculator._strategies[goal.goal_type]
        result = strategy.calculate(sessions, goal, date_from=date_from, date_to=date_to)

        return {
            **result,
            "goal_type": goal.goal_type.value,
            "period": goal.period.value,
            "unit": FieldManager.get_field(goal.variable_reference)?.unit or "",
        }
```

### 6. Routes - REST API Layer

```python
# api/routes.py
from flask import Blueprint, request, jsonify
from api.handlers import (
    challenges_handler,
    activities_handler,
    goals_handler,
)

# Blueprint für bessere Organisierung
api_bp = Blueprint('api', __name__, url_prefix='/api')

# CHALLENGES
@api_bp.route('/challenges', methods=['GET'])
def get_challenges():
    return challenges_handler.list_challenges()

@api_bp.route('/challenges', methods=['POST'])
def create_challenge():
    return challenges_handler.create_challenge(request.get_json())

@api_bp.route('/challenges/<name>', methods=['GET'])
def get_challenge(name):
    return challenges_handler.get_challenge(name)

@api_bp.route('/challenges/<name>/sessions', methods=['POST'])
def add_session(name):
    return challenges_handler.add_session(name, request.get_json())

# GOALS
@api_bp.route('/challenges/<name>/goal', methods=['POST'])
def set_goal(name):
    data = request.get_json()
    if data.get('delete'):
        return goals_handler.delete_goal(name)
    return goals_handler.set_goal(name, data)

@api_bp.route('/challenges/<name>/goal/progress', methods=['GET'])
def get_goal_progress(name):
    return goals_handler.get_goal_progress(name)

# ACTIVITIES & FIELDS
@api_bp.route('/activities', methods=['GET'])
def list_activities():
    return activities_handler.list_activities()

@api_bp.route('/activities/<activity_name>', methods=['GET'])
def get_activity_fields(activity_name):
    return activities_handler.get_activity_fields(activity_name)

# app.py
from flask import Flask
from api.routes import api_bp
from api.middleware import setup_cors, handle_errors

app = Flask(__name__)
setup_cors(app)
app.register_blueprint(api_bp)
setup_error_handlers(app)

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000, threaded=True)
```

---

## Frontend - React

### 1. Zielstrukturen & Ordnerorganisation

```
frontend/src/
├── App.js                              # Root Component
├── App.css
├── index.js                            # Entry Point
│
├── pages/                              # 🔹 Page-Level Komponenten (Routes)
│   ├── ChallengesPage.js              # /challenges - Liste & Erstellung
│   ├── ChallengeDetailPage.js         # /challenge/:name - Details
│   ├── ChallengeStatsPage.js          # /challenge/:name/stats - Analytics
│   └── styles/
│       ├── ChallengesPage.css
│       ├── ChallengeDetailPage.css
│       └── ChallengeStatsPage.css
│
├── components/                         # 🔹 Wiederverwendbare Komponenten
│   ├── Challenge/
│   │   ├── ChallengeCard.js           # Challenge-Übersicht (Mini)
│   │   ├── ChallengeHeader.js         # Challenge-Info Header
│   │   ├── ChallengeActions.js        # Delete, Rename Buttons
│   │   └── styles.css
│   │
│   ├── Session/
│   │   ├── SessionForm.js             # Session-Eingabeformular
│   │   ├── SessionList.js             # Sessions-Tabelle
│   │   ├── SessionRow.js              # Einzelne Session-Zeile
│   │   └── styles.css
│   │
│   ├── Goal/
│   │   ├── GoalForm.js                # Goal-Erstellungsformular
│   │   ├── GoalDisplay.js             # Goal-Info mit Progress
│   │   ├── GoalProgressBar.js         # Progress-Anzeige
│   │   └── styles.css
│   │
│   ├── Chart/
│   │   ├── ChartPlot.js               # Plotly-Diagramm
│   │   ├── ChartFilters.js            # Filter-Optionen
│   │   ├── ChartSettings.js           # Chart-Konfiguration
│   │   └── styles.css
│   │
│   ├── Form/
│   │   ├── FormField.js               # Reusable Form Field
│   │   ├── TextInput.js               # Text Input
│   │   ├── NumberInput.js             # Number Input
│   │   ├── EnumSelect.js              # Enum Dropdown
│   │   ├── DatePicker.js              # Date Input
│   │   └── styles.css
│   │
│   ├── UI/
│   │   ├── Button.js                  # Reusable Button
│   │   ├── Alert.js                   # Alert/Message
│   │   ├── Loading.js                 # Loading Spinner
│   │   ├── Modal.js                   # Modal Dialog
│   │   └── styles.css
│   │
│   └── Layout/
│       ├── Header.js                  # Top Navigation
│       ├── Sidebar.js                 # Optional Navigation
│       └── styles.css
│
├── hooks/                              # 🔹 Custom React Hooks
│   ├── useChallenge.js                # Challenge-Daten & Operations
│   ├── useGoalProgress.js             # Goal-Berechnung & Tracking
│   ├── useActivities.js               # Activities laden & cachen
│   ├── useFetch.js                    # Generic Fetch Hook
│   ├── useLocalStorage.js             # LocalStorage Persistence
│   └── useDebounce.js                 # Debounce Hook
│
├── services/                           # 🔹 API & Business Logic
│   ├── api/
│   │   ├── challengeApi.js            # Challenge API Calls
│   │   ├── activityApi.js             # Activity API Calls
│   │   ├── goalApi.js                 # Goal API Calls
│   │   ├── chartApi.js                # Chart/Plot API Calls
│   │   └── client.js                  # HTTP Client (Fetch Wrapper)
│   │
│   ├── formatters/
│   │   ├── dateFormatter.js           # Date/Time Formatting
│   │   ├── numberFormatter.js         # Number Formatting
│   │   └── dataFormatter.js           # Data Transformation
│   │
│   └── constants/
│       ├── api.js                     # API URLs & Endpoints
│       ├── goalTypes.js               # Goal-Type Konstanten
│       ├── activityTypes.js           # Activity-Type Konstanten
│       └── chartConfig.js             # Chart Default Config
│
├── context/                            # 🔹 Context API (State Management)
│   ├── ActivitiesContext.js           # Globale Activities + Caching
│   ├── ToastContext.js                # Toast Notifications
│   └── AppContext.js                  # App-Level State
│
├── utils/                              # 🔹 Utility Functions
│   ├── validation.js                  # Field Validation
│   ├── helpers.js                     # General Helpers
│   ├── errors.js                      # Error Handling
│   └── filters.js                     # Data Filtering
│
├── styles/                             # 🔹 Global Styles
│   ├── global.css                     # Global Styles
│   ├── variables.css                  # CSS Variables (Colors, Sizes)
│   ├── responsive.css                 # Responsive Design
│   └── themes.css                     # Dark/Light Theme
│
└── index.js                            # App Entry Point
```

### 2. Component Patterns - React Hooks

```jsx
// pages/ChallengeDetailPage.js
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useChallenge, useGoalProgress } from '../hooks';
import SessionForm from '../components/Session/SessionForm';
import SessionList from '../components/Session/SessionList';
import GoalDisplay from '../components/Goal/GoalDisplay';

export default function ChallengeDetailPage() {
  const { name } = useParams();
  const decodedName = decodeURIComponent(name);

  // 🔹 Custom Hooks für Daten & Logik
  const { challenge, loading, error, addSession, deleteChallenge } = useChallenge(decodedName);
  const { goalProgress } = useGoalProgress(decodedName);

  const [showSessionForm, setShowSessionForm] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  // Session-Handler
  const handleAddSession = async (sessionData) => {
    try {
      await addSession(sessionData);
      setSuccessMessage('Session erfolgreich hinzugefügt');
      setShowSessionForm(false);
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      console.error('Error:', err);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!challenge) return <div>Challenge nicht gefunden</div>;

  return (
    <div className="challenge-detail-page">
      <header className="challenge-header">
        <h1>{challenge.name}</h1>
        <p>Aktivität: {challenge.activity_type}</p>
      </header>

      {successMessage && <Alert type="success">{successMessage}</Alert>}

      <section className="goal-section">
        {challenge.goal ? (
          <GoalDisplay goal={challenge.goal} progress={goalProgress} />
        ) : (
          <div>Kein Ziel gesetzt</div>
        )}
      </section>

      <section className="session-section">
        <h2>Sessions</h2>
        {showSessionForm ? (
          <SessionForm
            activityType={challenge.activity_type}
            onSubmit={handleAddSession}
            onCancel={() => setShowSessionForm(false)}
          />
        ) : (
          <button onClick={() => setShowSessionForm(true)}>
            + Neue Session
          </button>
        )}
        <SessionList sessions={challenge.sessions} />
      </section>
    </div>
  );
}

// hooks/useChallenge.js - Custom Hook for Daten + Operationen
import { useState, useEffect, useCallback } from 'react';
import { challengeApi } from '../services/api';

export function useChallenge(challengeName) {
  const [challenge, setChallenge] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Lade Challenge beim Mount
  useEffect(() => {
    async function loadChallenge() {
      try {
        setLoading(true);
        const data = await challengeApi.getChallenge(challengeName);
        setChallenge(data);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadChallenge();
  }, [challengeName]);

  // Callback für Session-Adding
  const addSession = useCallback(async (sessionData) => {
    const response = await challengeApi.addSession(challengeName, sessionData);
    setChallenge(response.challenge);
    return response;
  }, [challengeName]);

  const deleteChallenge = useCallback(async () => {
    await challengeApi.deleteChallenge(challengeName);
    return true;
  }, [challengeName]);

  return { challenge, loading, error, addSession, deleteChallenge };
}

// components/Form/FormField.js - Reusable Form Field Component
import { TextInput, NumberInput, EnumSelect, DatePicker } from './';

export default function FormField({ field, value, onChange, error }) {
  const handleChange = (newValue) => {
    onChange(field.key, newValue);
  };

  // 🔹 Render je nach Field-Typ
  if (field.field_type === 'enum') {
    return (
      <div className="form-field">
        <label>{field.label}</label>
        <EnumSelect
          value={value}
          options={field.options}
          onChange={handleChange}
        />
        {error && <span className="error">{error}</span>}
      </div>
    );
  }

  if (field.field_type === 'number') {
    return (
      <div className="form-field">
        <label>{field.label} {field.unit && `(${field.unit})`}</label>
        <NumberInput
          value={value}
          min={field.min_value}
          max={field.max_value}
          onChange={handleChange}
        />
        {error && <span className="error">{error}</span>}
      </div>
    );
  }

  if (field.field_type === 'date') {
    return <DatePicker value={value} onChange={handleChange} />;
  }

  // default: text
  return (
    <div className="form-field">
      <label>{field.label}</label>
      <TextInput value={value} onChange={handleChange} />
      {error && <span className="error">{error}</span>}
    </div>
  );
}

// services/api/client.js - HTTP Fetch Wrapper
const API_BASE_URL = 'http://localhost:5000/api';

class ApiClient {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;

    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'API Error');
    }

    return response.json();
  }

  get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export const apiClient = new ApiClient();

// services/api/challengeApi.js
import { apiClient } from './client';

export const challengeApi = {
  listChallenges: () => apiClient.get('/challenges'),
  getChallenge: (name) => apiClient.get(`/challenges/${encodeURIComponent(name)}`),
  createChallenge: (name, activityType) =>
    apiClient.post('/challenges', { name, activity_type: activityType }),
  addSession: (challengeName, sessionData) =>
    apiClient.post(`/challenges/${encodeURIComponent(challengeName)}/sessions`, sessionData),
  deleteChallenge: (name) =>
    apiClient.post(`/challenges/${encodeURIComponent(name)}?delete=true`, {}),
};
```

### 3. State Management mit Context API

```jsx
// context/ActivitiesContext.js - Globaler Activities Cache
import { createContext, useState, useEffect, ReactNode } from 'react';
import { activityApi } from '../services/api';

export const ActivitiesContext = createContext();

export function ActivitiesProvider({ children }) {
  const [activities, setActivities] = useState({});
  const [loading, setLoading] = useState(false);

  // Lade Activities einmalig beim App-Start
  useEffect(() => {
    async function loadActivities() {
      try {
        setLoading(true);
        const data = await activityApi.listActivities();
        setActivities(data);
      } catch (err) {
        console.error('Failed to load activities:', err);
      } finally {
        setLoading(false);
      }
    }

    loadActivities();
  }, []);

  // Helper zum Abrufen einer Aktivität + Felder
  const getActivityFields = async (activityType) => {
    if (activities[activityType]) {
      return activities[activityType];
    }

    try {
      const fields = await activityApi.getActivityFields(activityType);
      setActivities(prev => ({
        ...prev,
        [activityType]: fields
      }));
      return fields;
    } catch (err) {
      console.error('Failed to load activity fields:', err);
      return [];
    }
  };

  return (
    <ActivitiesContext.Provider value={{ activities, loading, getActivityFields }}>
      {children}
    </ActivitiesContext.Provider>
  );
}

// hooks/useActivities.js - Hook zum Zugriff auf Context
import { useContext } from 'react';
import { ActivitiesContext } from '../context/ActivitiesContext';

export function useActivities() {
  const context = useContext(ActivitiesContext);
  if (!context) {
    throw new Error('useActivities muss innerhalb ActivitiesProvider verwendet werden');
  }
  return context;
}
```

---

## Kernkonzepte: Activities, Goals, Fields

### 1. Activities - Aktivitätsdefinition

**Was ist eine Activity?**
- Eine Aktivität (z.B. "Joggen", "Lesen", "Stimmung") definiert, welche Felder verfolgbar sind
- Jede Aktivität hat einen Typ (Enum) und ein Set von Feldern
- Eine Challenge ist immer an eine Aktivität gebunden

**Implementierungs-Strategie:**

```
Backend (Python):
  - ActivityType Enum mit 40+ Werten
  - Activity Dataclass mit Feldern
  - ActivityRegistry (Singleton Factory)
  - ACTIVITY_FIELD_MAPPINGS (zentrale Zuordnung)

Frontend (React):
  - useActivities Hook (Context)
  - Activities laden einmalig beim Start
  - Aktivitätsfeld-Selekt bei Challenge-Erstellung
  - Dynamische Fieldlisten-Rendering
```

**Orchestrierung:**

```python
# Backend: Activity definieren
class ActivityRegistry:
    JOGGING = Activity(
        type=ActivityType.JOGGING,
        fields=[
            FIELD_DEFINITIONS["distance"],
            FIELD_DEFINITIONS["duration"],
            FIELD_DEFINITIONS["movement_intensity"],
            # ...
        ]
    )

# API Endpoint: GET /activities
# Response: { "activities": ["Joggen", "Radfahren", ...] }

# API Endpoint: GET /activities/Joggen
# Response: { "fields": [{...}, {...}, ...] }
```

### 2. Fields - Flexible Feldverwaltung

**Was ist ein Field?**
- Ein Field ist eine einzelne Metrik/Property einer Session (z.B. "distance_km", "mood_value")
- Zentral definiert in `FIELD_DEFINITIONS` (85+ Felder)
- Jedes Activity hat eine Subset dieser Felder
- Fields können berechnete Hidden Fields sein

**Implementierungs-Strategie:**

```
Zentrale Field-Registry:
  - Alle 85+ Felder in FIELD_DEFINITIONS
  - Keine Redundanz
  - Einfach zu erweitern

Hidden Fields (Berechnung):
  - average_distance = sum(distance) / count
  - velocity = distance / duration
  - average_velocity = sum(velocity) / count
  - consecutive_days (für Streak-Goals)

Validierung:
  - Type-Validierung (number, enum, text)
  - Range-Validierung (min/max)
  - Enum-Validierung (erlaubte Werte)
```

**Backend Implementierung:**

```python
# domains/fields/definitions.py - ZENTRAL!
FIELD_DEFINITIONS = {
    "distance": Field(...),
    "average_distance": Field(..., hidden=True, calculator="calculate_average"),
    "mood_value": Field(...),
    # ... 85 mehr
}

# domains/fields/calculator.py
class FieldCalculator:
    @staticmethod
    def calculate_hidden_field(field: Field, sessions: List[Session]) -> Any:
        if field.calculator == "calculate_average":
            return FieldCalculator.calculate_average(sessions, field.key)
        elif field.calculator == "calculate_velocity":
            return FieldCalculator.calculate_velocity(sessions, field.key)
        # ...

    @staticmethod
    def calculate_average(sessions: List[Session], field_key: str) -> float:
        values = [s.values[field_key] for s in sessions if field_key in s.values]
        return sum(values) / len(values) if values else 0
```

**Frontend Implementierung:**

```jsx
// components/Session/SessionForm.js
function SessionForm({ activityType, onSubmit }) {
  const { getActivityFields } = useActivities();
  const [fields, setFields] = useState([]);
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});

  // Lade Felder der Aktivität
  useEffect(() => {
    async function loadFields() {
      const activityFields = await getActivityFields(activityType);
      // Filter Hidden Fields raus
      const displayFields = activityFields.filter(f => !f.hidden);
      setFields(displayFields);
    }
    loadFields();
  }, [activityType]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validiere Required Fields
    const newErrors = {};
    fields.forEach(field => {
      if (field.required && !formData[field.key]) {
        newErrors[field.key] = 'Pflichtfeld';
      }
    });

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    onSubmit({
      date: formData.date,
      time: formData.time,
      values: formData
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      {fields.map(field => (
        <FormField
          key={field.key}
          field={field}
          value={formData[field.key] || ''}
          onChange={(key, val) => setFormData({...formData, [key]: val})}
          error={errors[field.key]}
        />
      ))}
      <button type="submit">Session speichern</button>
    </form>
  );
}
```

### 3. Goals - Flexible Zieltypen

**Was ist ein Goal?**
- Ein Goal ist eine Zielsetzung für eine Challenge (z.B. "100 km pro Monat joggen")
- 12 verschiedene Zieltypen A-L (More than, Less than, Frequency, Streak, Average, etc.)
- Wird an eine Variable gebunden (z.B. "distance_km", "mood_value")
- Hat einen Zeitraum (daily, weekly, monthly, yearly, date_range)

**Implementierungs-Strategie:**

```
Strategy Pattern - eine Klasse pro Goal-Typ:

  a) MoreThanStrategy: current >= target
  b) LessThanStrategy: current <= target
  c) AvoidStrategy: current == 0
  d) FrequencyExactStrategy: count == target
  e) FrequencyMinStrategy: count >= target
  f) FrequencyMaxStrategy: count <= target
  g) StreakStrategy: consecutive_days >= target
  h) IncreaseDailyStrategy: Tägliche Steigerung bis Target
  i) DecreaseDailyStrategy: Tägliche Reduktion bis Target
  j) AverageAboveStrategy: average >= target
  k) AverageBelowStrategy: average <= target
  l) ConditionalStrategy: X erreichen unter Bedingung Y
```

**Backend Implementierung:**

```python
# Goal definieren
goal = Goal(
    description="100 km pro Monat Joggen",
    variable_reference="distance",
    goal_type=GoalType.MORE_THAN,
    target=100.0,
    period=GoalPeriod.MONTHLY,
)

# Progress berechnen
calculator = GoalProgressCalculator()
progress = calculator.calculate_progress(
    sessions=challenge.sessions,
    goal=goal,
    date_from="2026-03-01",
    date_to="2026-03-31"
)

# Response:
# {
#   "value": 234.5,
#   "target": 100,
#   "status": "completed",
#   "percentage": 100,
#   "period": "monthly",
#   "message": "100 von 100 km ✓"
# }
```

**Frontend Integration:**

```jsx
// components/Goal/GoalDisplay.js
function GoalDisplay({ goal, progress }) {
  if (!goal) return <div>Kein Goal gesetzt</div>;

  const statusColor = {
    'completed': 'green',
    'in_progress': 'blue',
    'not_completed': 'red',
    'no_data': 'gray'
  }[progress.status];

  return (
    <div className="goal-display">
      <h3>{goal.description}</h3>
      <GoalProgressBar
        value={progress.value}
        target={progress.target}
        percentage={progress.percentage}
        unit={progress.unit}
        status={progress.status}
        color={statusColor}
      />
      <p>{progress.value} / {progress.target} {progress.unit}</p>
      <p className={`status ${progress.status}`}>{progress.message}</p>
    </div>
  );
}
```

---

## Best Practices & Design Patterns

### 1. Architektur-Pattern: 3-Layer Architecture

```
┌─ Web Layer (Controllers/Routes)        ← Handling HTTP
├─ Business Logic Layer (Services)       ← Core Logic
└─ Data Layer (Models/Storage)           ← Persistence

Vorteile:
  ✅ Separation of Concerns
  ✅ Testbarkeit
  ✅ Wartbarkeit
  ✅ Wiederverwendbarkeit
```

### 2. Design Patterns

**Registry/Factory Pattern - Activity Management**
```python
# PROBLEM: 40+ Aktivitäten mit unterschiedlichen Feldkombinationen
# LÖSUNG: Zentrale Registry statt Dutzende von Klassen

class ActivityRegistry:  # Singleton + Factory
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def get_activity(self, activity_type):
        return self._activities[activity_type]

# Verwendung:
registry = ActivityRegistry()
jogging_activity = registry.get_activity(ActivityType.JOGGING)
```

**Strategy Pattern - Goal Calculation**
```python
# PROBLEM: 12 verschiedene Goal-Berechnungstypen
# LÖSUNG: Strategy Pattern - eine Klasse pro Typ

class GoalStrategy(ABC):
    @abstractmethod
    def calculate(self, sessions, goal):
        pass

class MoreThanStrategy(GoalStrategy):
    def calculate(self, sessions, goal):
        # Berechnung für "mehr als X"

calculator = GoalProgressCalculator()
calculator._strategies[GoalType.MORE_THAN] = MoreThanStrategy()

# Verwendung:
result = calculator.calculate_progress(sessions, goal)
```

**Dataclass Pattern - Type-Safe Models**
```python
# PYTHON: Minimale Boilerplate, maximal Type-Safe

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Challenge:
    name: str
    activity_type: ActivityType
    sessions: List[Session] = field(default_factory=list)
    goal: Optional[Goal] = None

    def add_session(self, session: Session):
        self.sessions.append(session)

# Vorteile:
# ✅ Automatischerr __init__
# ✅ Automatischer __repr__
# ✅ Type Hints
# ✅ Serialisierbar
```

**Custom Hook Pattern - React**
```jsx
// REACT: Zusätzliche State-Logik in einer Funktion

export function useChallenge(name) {
  const [challenge, setChallenge] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load Challenge
  }, [name]);

  const addSession = useCallback(async (data) => {
    // Add Session
  }, [name]);

  return { challenge, loading, addSession };
}

// Verwendung:
const { challenge, loading, addSession } = useChallenge('Joggen');
```

### 3. Code-Quality Standards

**Python: Type Hints überall**
```python
def calculate_average(
    sessions: List[Session],
    field_key: str
) -> float:
    """Berechnet Durchschnitt eines Feldes"""
    values: List[float] = [
        s.values[field_key]
        for s in sessions
        if field_key in s.values
    ]
    return sum(values) / len(values) if values else 0.0

# Überprüfen mit: mypy domains/
```

**React: PropTypes / JSDoc**
```jsx
import PropTypes from 'prop-types';

function SessionForm({ fields, onSubmit }) {
  return <form>...</form>;
}

SessionForm.propTypes = {
  fields: PropTypes.arrayOf(PropTypes.object).isRequired,
  onSubmit: PropTypes.func.isRequired,
};
```

**Fehlerbehandlung**
```python
# Backend
try:
    session = Session(date, time, values)
    challenge.add_session(session)
except ValueError as e:
    logger.error(f"Invalid session: {e}")
    return {"error": str(e)}, 400

# Frontend
try {
  const response = await addSession(data);
  setSuccessMessage('Session erfolgreich');
} catch (err) {
  setError(`Fehler: ${err.message}`);
}
```

**Logging**
```python
# Backend: Structured Logging
logger = logging.getLogger(__name__)

logger.info(
    f"Challenge created",
    extra={
        "challenge_name": challenge.name,
        "activity_type": challenge.activity_type.value,
    }
)

logger.error(
    f"Failed to calculate goal progress",
    exc_info=True,
    extra={"goal_id": goal.id}
)
```

### 4. OOP Best Practices

**Komposition statt Vererbung**
```python
# ❌ NICHT: Activity erbt von BaseEntity
class Activity(BaseEntity):
    pass

# ✅ JA: Activity nutzt Field-Komposition
@dataclass
class Activity:
    type: ActivityType
    fields: List[Field]  # Komposition!
```

**Single Responsibility Principle**
```python
# ❌ NICHT: Eine Klasse macht alles
class ChallengeManager:
    def create_challenge(self): pass
    def calculate_goal(self): pass
    def filter_data(self): pass
    def export_json(self): pass

# ✅ JA: Getrennte Verantwortlichkeiten
class ChallengeService:
    def create_challenge(self): pass

class GoalCalculator:
    def calculate(self): pass

class DataFilterer:
    def filter(self): pass

class JsonExporter:
    def export(self): pass
```

**Interface/Contract Principle**
```python
# Python: Mit ABC (Abstract Base Class)
from abc import ABC, abstractmethod

class GoalStrategy(ABC):
    @abstractmethod
    def calculate(self, sessions: List[Session], goal: Goal) -> Dict:
        """Berechnet Goal-Progress"""
        pass

class MoreThanStrategy(GoalStrategy):
    def calculate(self, sessions, goal):
        # Implementation
        pass

# Frontend (React):
function SessionForm({ fields }) {
  // Erwartet: Array von Objects mit { key, label, fieldType, ... }
  // Keine spezifischen Implementierungen
}
```

---

## Implementierungsreihenfolge

### Phase 1: Foundation (1-2 Tage)

**Backend:**
1. ✅ Enums definieren (ActivityType, GoalType, FieldType, etc.)
2. ✅ Models/Dataclasses erstellen (Activity, Challenge, Session, Goal, Field)
3. ✅ FIELD_DEFINITIONS mit 85+ Feldern erstellen
4. ✅ ActivityRegistry + ACTIVITY_FIELD_MAPPINGS aufbauen
5. ✅ JSON Storage refaktorieren (Serialization/Deserialization)

**Frontend:**
1. ✅ Ordnerstruktur aufbauen
2. ✅ Global CSS Setup (variablen, Responsive)
3. ✅ HTTP Client Setup (fetch wrapper)
4. ✅ ActivitiesContext + useActivities Hook

### Phase 2: Core Features (2-3 Tage)

**Backend:**
1. ✅ Activity API Routes (GET /activities, GET /activities/:name)
2. ✅ Challenge CRUD Routes überarbeiten
3. ✅ Session Management verbessern
4. ✅ Field Validation implementieren

**Frontend:**
1. ✅ Challenge List Page mit CRUD
2. ✅ SessionForm Component mit dynamischen Fields
3. ✅ SessionList Component
4. ✅ Reusable Form Components (TextInput, NumberInput, EnumSelect)

### Phase 3: Goals (2-3 Tage)

**Backend:**
1. ✅ GoalProgressCalculator + Strategy Pattern
2. ✅ Alle 12 Goal-Strategien implementieren
3. ✅ Goal API Routes
4. ✅ Progress-Berechnung für verschiedene Perioden

**Frontend:**
1. ✅ GoalForm Component
2. ✅ GoalDisplay + Progress Bar
3. ✅ useGoalProgress Hook
4. ✅ Integration in ChallengeDetail

### Phase 4: Advanced Features (2-3 Tage)

**Backend:**
1. ✅ Field Calculator für Hidden Fields
2. ✅ Data Aggregation (average, sum, streak)
3. ✅ Advanced Filtering
4. ✅ Chart Data API

**Frontend:**
1. ✅ ChartPlot Component mit Filterung
2. ✅ ChallengeStatsPage
3. ✅ Advanced Chart Settings
4. ✅ Performance-Optimierung

### Phase 5: Polish (1-2 Tage)

1. ✅ Error Handling überall
2. ✅ Logging hinzufügen
3. ✅ Tests schreiben
4. ✅ Dokumentation
5. ✅ UI/UX Polish

---

## Code-Standards

### Python Backend Standards

```python
# 1. Type Hints überall
def calculate_progress(
    sessions: List[Session],
    goal: Goal,
    date_from: Optional[str] = None
) -> Dict[str, Any]:
    """Berechnet den Goal-Fortschritt"""
    pass

# 2. Dataclass für Models
@dataclass
class Session:
    date: str
    time: str
    values: Dict[str, Any]

# 3. Enums für Konstanten
class ActivityType(Enum):
    JOGGING = "Joggen"

# 4. Fehlerbehandlung
try:
    result = do_something()
except ValueError as e:
    logger.error(f"Invalid input: {e}")
    raise

# 5. Docstrings
def calculate():
    """
    Berechnet Wert.

    Returns:
        Dict mit Ergebnis

    Raises:
        ValueError: Falls Input ungültig
    """
    pass

# 6. Logging
logger.info(f"Challenge {name} erstellt")
logger.error(f"Fehler beim Laden", exc_info=True)

# 7. Constants in CAPS
MAX_SESSIONS_PER_CHALLENGE = 1000
DEFAULT_PERIOD = GoalPeriod.MONTHLY
```

### React Frontend Standards

```jsx
// 1. Funktionale Komponenten mit Hooks
export default function SessionForm({ onSubmit }) {
  const [data, setData] = useState({});

  useEffect(() => {
    // Seiteneffekte hier
  }, []);

  return <div>...</div>;
}

// 2. Custom Hooks für Logik
export function useChallenge(name) {
  const [challenge, setChallenge] = useState(null);
  // ...
  return { challenge };
}

// 3. PropTypes für Runtime-Validierung
SessionForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
  fields: PropTypes.arrayOf(PropTypes.object),
};

// 4. try-catch bei Async
try {
  await addSession(data);
} catch (err) {
  setError(err.message);
}

// 5. Bedingte Rendering lesbar
if (loading) return <Loading />;
if (error) return <Error message={error} />;

return <div>{challenge.name}</div>;

// 6. Callbacks mit useCallback
const handleSubmit = useCallback(async (data) => {
  await api.submit(data);
}, []);

// 7. useState besser organisieren
const [data, setData] = useState({});
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);
// NICHT: const [dataLoadingError, setDataLoadingError] = useState({...});
```

---

## Zusammenfassung und Nächste Schritte

### Wenn Sie bereit sind zu implementieren:

1. **Backend Foundation starten**: Enums, Models, Registry
2. **Frontend Ordner aufbauen**: React Struktur einrichten
3. **API Contracts definieren**: Dokumentieren Sie, was Backend liefert
4. **Inkrementell bauen**: Jede Feature komplett testen vor nächster
5. **Tests schreiben**: Besonders für Business Logic (Goals, Calculations)

### Key Success Factors:

✅ **Zentrale Field-Registry**: Keine Redundanz, einfach zu erweitern
✅ **Strategy Pattern für Goals**: Skalierbar auf neue Goal-Typen
✅ **Type Safety überall**: Python Type Hints, React PropTypes
✅ **Separation of Concerns**: Web Layer → Business Layer → Data Layer
✅ **Custom Hooks in React**: Logik aus Komponenten rausziehen
✅ **Dataclasses in Python**: Minimale Boilerplate, maximale Klarheit

---

## Dokumentation & Referenzen

**Backend Referenz-URLs:**
- Python Dataclasses: https://docs.python.org/3/library/dataclasses.html
- Type Hints: https://docs.python.org/3/library/typing.html
- Flask Patterns: https://flask.palletsprojects.com/

**Frontend Referenz-URLs:**
- React Hooks: https://react.dev/reference/react
- PropTypes: https://prop-types-in-action.vercel.app/
- Custom Hooks: https://react.dev/learn/reusing-logic-with-custom-hooks

---

**Letztes Update**: März 2026
**Erstellt für**: ChallengeMyself v2.0
