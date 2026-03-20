# KeepRising - Mobiles Aktivitäts-Tracking App

Eine React Native/TypeScript Anwendung zum Verfolgen persönlicher Ziele und Aktivitäten mit umfangreicher Zielverfolgung und Datenvisualisierung.

## ✨ Neue Features (aktualisiert)

### ✅ Vollständiges Goal-System
- **12 unterschiedliche Zieltypen** (a-l):
  - `MoreThan`: Mehr als X erreichen
  - `LessThan`: Weniger als X erreichen
  - `Avoid`: Ganz vermeiden
  - `FrequencyExact`: X-mal pro Periode
  - `FrequencyMin`: Mindestens X-mal pro Periode
  - `Streak`: Tage in Folge
  - `AverageAbove`: Durchschnitt über X
  - `AverageBelow`: Durchschnitt unter X
  - Und mehr...

### 📊 Aktivitäten (aktuell aktiv)
1. **Joggen** - Distanz, Dauer, Intensität, Wetter, Energie
2. **Radfahren** - Mit Höhenmeter und Streckentyp
3. **Spazieren** - Mit Schrittzähler
4. **Schwimmen** - Mit Schwimmstil
5. **Workout** - Trainingsart und Intensität
6. **Schlaf** - Schlafqualität und Aufwachanzahl
7. **Wasserkonsum** - Mit Temperatur und Quelle

### 🎯 Verbesserte Komponenten
- `GoalWidget`: Interaktive Zielfortschrittsanzeige
- `ChallengeCard`: Übersichts-Karten mit Quick-Stats
- `SessionList`: Detaillierte Session-Auflistung
- `ChartDataService`: Professionelle Diagramm-Vorbereitung

### 💾 Persistierung
- Vollständige AsyncStorage-Integration
- Challenge/Session/Goal-Persistence
- Automatische Datei-Verwaltung

### 🎨 Theming
- Dark/Light Mode Support
- Konsistentes Farbschema

## 📦 Projekt-Struktur

```
KeepRising/
├── app/
│   ├── (tabs)/              # Hauptscreen-Tabs
│   ├── challenge/           # Challenge-Details Screen
│   └── modal.tsx
├── components/
│   ├── ChallengeCard.tsx    # Challenge-Übersicht
│   ├── GoalWidget.tsx       # Ziel-Fortschritt
│   ├── SessionList.tsx      # Sessions-Liste
│   ├── BarChart.tsx
│   ├── LineChart.tsx
│   └── ui/
├── models/                  # TypeScript Models
│   ├── Challenge.ts
│   ├── Session.ts
│   ├── Goal.ts
│   └── Field.ts
├── services/                # Business Logic
│   ├── challengeService.ts          # Challenge CRUD
│   ├── goalProgressTracker.ts       # Goal-Berechnung
│   ├── chartDataService.ts          # Chart-Daten
│   └── index.ts             # Exports
├── src/
│   ├── data/
│   │   └── activities.ts            # Activities Definition
│   ├── enums/               # TypeScript Enums
│   │   ├── MovementIntensity.ts
│   │   ├── RouteType.ts
│   │   └── Weather.ts
│   └── ...
├── constants/
│   └── activities.ts        # Activity Re-exports
└── hooks/
    ├── use-theme-color.ts
    └── use-color-scheme.ts
```

## 🚀 Verwendung

### Challenge erstellen
```typescript
import { ChallengeService } from './services';
import { GoalClass, GoalType, GoalPeriod } from './models';

const challenge = await ChallengeService.createChallenge(
  "Sommerfit 2026",
  "Joggen"
);
```

### Session hinzufügen
```typescript
import { SessionClass } from './models';

const session = new SessionClass(
  `session_${Date.now()}`,
  "2026-02-14",
  "18:30",
  { distance: 5.2, duration: 30, intensity: "mittel" }
);

await ChallengeService.addSession("Sommerfit 2026", session);
```

### Goal setzen
```typescript
const goal = new GoalClass(
  `goal_${Date.now()}`,
  "20km pro Woche",
  GoalType.MoreThan,
  "distance",
  20,
  GoalPeriod.Weekly
);

await ChallengeService.setGoal("Sommerfit 2026", goal);
```

### Zielfortschritt abrufen
```typescript
import { GoalProgressTracker } from './services';

const challenge = await ChallengeService.getChallenge("Sommerfit 2026");
const progress = GoalProgressTracker.calculateProgress(
  challenge.goal,
  challenge.sessions
);

console.log(`Fortschritt: ${progress.current}/${progress.target} ${progress.unit}`);
```

## 🛠️ Technologie-Stack

- **React Native** 0.81.5
- **TypeScript** für Typ-Sicherheit
- **Expo 54** für einfache Verwaltung
- **AsyncStorage** für Persistierung
- **React Navigation** für Routing
- **D3.js** für Datenvisualisierung

## 📋 Abhängigkeiten

- `@react-native-async-storage/async-storage` - Datenpersistierung
- `expo-sqlite` - Optional für erweiterte Datenverwaltung
- `d3` - Diagramme & Visualisierung

## 🗑️ Gelöschte Dateien

Die folgenden veralteten Dateien wurden entfernt:
- `services/storage.ts` (ersetzt durch `challengeService.ts`)
- `services/statsService.ts` (Funktionalität in `goalProgressTracker.ts`)
- `components/external-link.tsx`
- `components/hello-wave.tsx`
- `components/parallax-scroll-view.tsx`
- `src/types/` (komplett, ersetzt durch Models)

## 🎯 Nächste Schritte

1. **Screen Implementation**: Implementiere Challenge-Screens (Liste, Detail, Bearbeitung)
2. **Chart Components**: Erweitere BarChart/LineChart mit echten Daten
3. **Diagramme**: Integriere D3-Visualisierungen
4. **Testing**: Unit-Tests für Goal-Berechnungen

## 📝 Lizenz

MIT
