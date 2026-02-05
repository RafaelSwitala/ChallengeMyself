# 🚀 ChallengeMyself - Umfangreiche Diagramm & Daten-Updates

## Zusammenfassung der Änderungen (V2.0)

Große Überarbeitung des Diagramm- und Visualisierungssystems mit erweiterten Filter-, Vergleichs- und Datenoptionen.

---

## 📋 Änderungen im Detail

### 1. **Neue Dateistruktur in `backend/models/activities.py`**

#### Feldkategorisierung
Alle 17 Activities wurden neu strukturiert mit logischer Feldkategorisierung:

```
Field(name, type, unit, values, chart_type)
- chart_type: 'line', 'bar', 'both', 'none'
  - 'line': nur Liniendiagramme
  - 'bar': nur Säulendiagramme  
  - 'both': sowohl Line als auch Bar möglich
  - 'none': Kategorie-Feld (nicht für Charts)
```

#### Neue Helper-Funktionen
```python
get_numeric_fields(activity, chart_type=None)     # Numerische Felder filtern
get_category_fields(activity)                       # Kategorische Felder (Filter)
get_field_unit(activity, field_name)                # Einheiten abrufen
get_comparison_features(activity)                   # Vergleichsfelder pro Activity
```

#### Neue Activities & Felder
- **Erweiterte Metriken**: Geschwindigkeit, Kalorienverbrauch, Durchschnitte (auto-berechnet)
- **Neue Aktivitäten**: Energielevel, Motivation (zusätzlich zu Stimmung, Stress)
- **Bessere Enum-Werte**: Standardisierte, deutsche Bezeichnungen statt Text-Felder

#### Beispiele:
- **Laufen**: distanz_km, dauer_min, geschwindigkeit_kmh, kalorienverbrauch, pausen_anzahl, intensitaet, strecke_typ, wetter
- **Alkohol**: menge_ml, alkohol_einheiten, getraenk_typ, anlass
- **Stimmung**: wert (%), hauptgefuehl, ausloeser

### 2. **Enhanced Plot Handler in `backend/app.py`**

#### Neue Features
- ✅ **Mehrere Felder gleichzeitig**: Wähle 2+ Felder um sie zu vergleichen
- ✅ **Vergleiche nach Kategorien**: Z.B. "strecke_typ" → Sieh Distanz für Asphalt vs Feldweg vs Waldweg getrennt
- ✅ **Dynamische Y-Achse**: Auto-Skalierung mit 10% Puffer, erkennt Einheiten
- ✅ **Einheiten in Tooltips**: Zeigt "Distanz: 5.2 km" statt nur "Distanz: 5.2"
- ✅ **Improved Hover**: Format: "<b>Feldname - Kategorie</b><br>Datum: X<br>Wert: Y [Einheit]"
- ✅ **Bar Charts funktionieren**: Vorher nur teilweise, jetzt vollständig
- ✅ **Vergleiche pro Activity**: Jede Activity hat definierte Vergleichsfelder (COMPARISON_FEATURES dict)

#### Technische Verbesserungen
```python
# Vor: Einfache Aggregation
agg = df.groupby("date")[f].sum().reset_index()

# Nach: Intelligente Kategorisierung + dynamische Achsen
if comparison_field:
    for comp_val in comparison_values:
        df_subset = df[df[comparison_field] == comp_val]
        # ... pro Kategorie separate Traces
```

### 3. **Komplett neues `plot.html` Template**

#### Layout & Design
- Modernes 3-Row Layout mit CSS-Grid
- Farbliche Gruppierung: Chat-Typ, Vergleich, Felder, Filter
- Responsive Design (Mobile-friendly)
- Info-Panel mit Tipps

#### Neue Kontroll-Elemente
1. **Chart-Typ Selector**: Line / Bar / Scatter
2. **Kategorie-Vergleich**: Dropdown mit Vergleichsfeldern pro Activity
3. **Datenfeld Checkboxen**: Alle numerischen Felder (max N auswählbar)
4. **Intensitäts-Filter**: Multi-Select für Intensität
5. **Action Buttons**: "Aktualisieren" & "Zurücksetzen"
6. **Legende**: Auto-generiert von Plotly (clickable)

#### Template Variables (neu)
```jinja2
numeric_fields          # Alle Felder die in Charts erscheinen können
category_fields         # Alle Filter-Felder
comparison_features     # Vergleichsoptionen für diese Activity
selected_fields         # Aktuell gewählte Felder
comparison_field        # Aktuell gewähltes Vergleichsfeld
comparison_values       # Verfügbare Werte für Vergleichsfeld
```

---

## 🎯 Beispiele für neue Funktionalität

### Beispiel 1: Laufen - Vergleich nach Streckentyp
```
Activity: Laufen
Chart-Typ: Line
Felder: distanz_km, geschwindigkeit_kmh
Vergleichsfeld: strecke_typ

Ergebnis:
- 4 Linien (distanz_km für mix, asphalt, feldweg, waldweg)
- 4 Linien (geschwindigkeit_kmh für mix, asphalt, feldweg, waldweg)
- Farblich unterschieden in Legende
- Hover zeigt z.B. "distanz_km - asphalt, Datum: 2026-02-02, Wert: 5.2 km"
```

### Beispiel 2: Alkohol - Kategorisieren
```
Activity: Alkohol
Chart-Typ: Bar
Felder: menge_ml, alkohol_einheiten
Vergleichsfeld: getraenk_typ

Ergebnis:
- Gruppierte Balken (menge_ml für Bier, Wein, Schnaps, Cocktail)
- Separate Balken (alkohol_einheiten für jeder Typ)
- Aggregate pro Datum
- Y-Achse auto-skaliert
```

### Beispiel 3: Stimmung - Trend Analyse
```
Activity: Stimmung
Chart-Typ: Line
Felder: wert (%)
Vergleichsfeld: ausloeser

Ergebnis:
- 5 separate Trends (erfolg, freunde, natur, hobby, stress)
- Zeigt wie Stimmung sich bei verschiedenen Auslösern entwickelt
- Leicht zu sehen welcher Auslöser die beste Stimmung bringt
```

---

## 🔧 Technische Details

### Neue Imports in `app.py`
```python
from models.activities import (
    get_numeric_fields,
    get_category_fields,
    get_field_unit,
    get_comparison_features
)
import numpy as np  # Für numerische Operationen
```

### Y-Achsen-Optimierung
```python
# Berechne Range aus allen Y-Werten
all_y = [y for trace in data for y in trace["y"] if y is not None]
if all_y:
    y_min, y_max = min(all_y), max(all_y)
    y_range = y_max - y_min
    # 10% Puffer
    layout["yaxis"]["range"] = [y_min - 0.1*y_range, y_max + 0.1*y_range]
```

### Plotly Config
```python
config = {
    "responsive": True,           # Auto-resize
    "displayModeBar": True,        # Zeige Toolbar
    "displaylogo": False           # Kein Plotly-Logo
}
```

---

## 📊 Activity-spezifische Vergleichsfelder

```python
COMPARISON_FEATURES = {
    "Laufen": ["strecke_typ", "intensitaet", "wetter"],
    "Radfahren": ["strecke_typ", "intensitaet"],
    "Schwimmen": ["schwimmstil", "intensitaet"],
    "Workout": ["trainingsart", "intensitaet"],
    "Lesen": ["medium"],
    "Alkohol": ["getraenk_typ", "anlass"],
    "Stimmung": ["hauptgefuehl", "ausloeser"],
    # ...etc
}
```

---

## ✨ Neue UI/UX Features

### Checkboxen-Grid
```css
.checkbox-group {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
}
```
- Responsive Spalten
- Hover-Effekte
- Gutes Spacing

### Vergleichs-Selector
```html
<select name="comparison_field">
    <option value="">-- Kein Vergleich --</option>
    {% for feature in comparison_features %}
        <option value="{{ feature }}">{{ feature }}</option>
    {% endfor %}
</select>
```
- Dynamisch pro Activity
- Zeigt verfügbare Werte
- Auto-Submit

### Info-Panel
```
💡 Tipps zur Visualisierung
- Mehrere Felder: Wähle mehrere um zu vergleichen
- Vergleich: Nutze Kategorie-Dropdown
- Intensität: Filtere nach Wert
- Interaktion: Hover, Zoom, Legende
```

---

## 🐛 Bugfixes

### Vorher
- ❌ Säulendiagramm: Nicht aggregiert, Y-Achse falsch
- ❌ Mehrere Felder: Nicht kombinierbar
- ❌ Keine Einheiten in Tooltips
- ❌ Feste Y-Achse führt zu schlechtem Layout
- ❌ Kategorische Felder in Charts: Nicht möglich

### Nachher
- ✅ Säulendiagramm: Korrekt aggregiert mit groupby().sum()
- ✅ Mehrere Felder: Alle kombinierbar (je nach chart_type)
- ✅ Einheiten: Automatisch aus Field.unit hinzugefügt
- ✅ Y-Achse: Dynamisch mit 10% Puffer-Zone
- ✅ Kategorien: Nutzen Vergleichsmechanismus

---

## 🚀 Deployment

### Installation
```powershell
# Neue activities.py Funktionen werden automatisch geladen
# Neue plot.html wird automatisch gerenderweise
# Kein pip install nötig (nur Backend-Dateien geändert)

.\start.ps1
```

### Testing
```powershell
# Im Browser:
# 1. Gehe auf http://localhost:5000/
# 2. Öffne eine Challenge mit Sessions
# 3. Klick auf "Visualisierung"
# 4. Teste die neuen Filter
```

---

## 📝 Nächste Schritte (Optional)

### Kurz-Fristig
- [ ] Automatische Metriken-Berechnung (Geschwindigkeit, Kalorien)
- [ ] Export-Funktion (PDF, CSV)
- [ ] Sessions-Bearbeitung

### Mittel-Fristig
- [ ] Datenbank (statt JSON)
- [ ] Prognosen & Trends-Analyse
- [ ] Mobile-App
- [ ] Mehrbenutzer-Support

---

## 📚 Dokumentation

- [activities.py](./backend/models/activities.py) - Feldkategorisierung
- [app.py](./backend/app.py) - Plot-Handler (Zeile 327+)
- [plot.html](./backend/templates/plot.html) - Template
- [styles.css](./backend/static/styles.css) - Styling
