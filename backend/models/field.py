"""
Zentrale Feldefinitionen für alle 85+ Felder
Definiert die Field-Klasse und zentrale Field-Registry mit FieldManager
"""

from dataclasses import dataclass
from typing import Optional, List, Any
from .enums import FieldType, ChartType


@dataclass
class Field:
    """
    Definiert ein einzelnes Feld (z.B. distance_km, mood_value)
    Zentrale Stelle für alle Feldkonfigurationen
    """
    key: str                            # Eindeutige ID: z.B. "distance"
    label: str                          # Benutzer-freundlich: z.B. "Distanz"
    field_type: FieldType              # number, integer, enum, text, boolean
    chart_type: ChartType              # Wie wird es visualisiert
    unit: Optional[str] = None         # z.B. "km", "min", "%", "0-10"
    required: bool = False              # Pflichtfeld?
    hidden: bool = False                # Berechnetes Feld (nicht von User eingegeben)
    options: Optional[List[str]] = None # Enum-Optionen
    description: Optional[str] = None   # Dokumentation
    min_value: Optional[float] = None   # Validierung: Minimum
    max_value: Optional[float] = None   # Validierung: Maximum
    calculator: Optional[str] = None    # Funktionsreferenz für Hidden Fields

    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """
        Validiert einen Wert gegen dieses Field.
        Returns: (is_valid, error_message)
        """
        if value is None and not self.required:
            return True, None

        if value is None and self.required:
            return False, f"{self.label} ist erforderlich"

        try:
            if self.field_type == FieldType.NUMBER or self.field_type == FieldType.INTEGER:
                if not isinstance(value, (int, float)):
                    return False, f"{self.label} muss eine Zahl sein"

                num_value = float(value)

                if self.min_value is not None and num_value < self.min_value:
                    return False, f"{self.label} muss mindestens {self.min_value} sein"

                if self.max_value is not None and num_value > self.max_value:
                    return False, f"{self.label} darf maximal {self.max_value} sein"

            elif self.field_type == FieldType.ENUM:
                if self.options and value not in self.options:
                    return False, f"{self.label} muss eine der Optionen sein: {', '.join(self.options)}"

            elif self.field_type == FieldType.TEXT:
                if not isinstance(value, str):
                    return False, f"{self.label} muss Text sein"

            elif self.field_type == FieldType.BOOLEAN:
                if not isinstance(value, bool):
                    return False, f"{self.label} muss wahr oder falsch sein"

            return True, None

        except Exception as e:
            return False, f"Validierungsfehler: {str(e)}"


# ============================================================================
# ZENTRALE FIELD-REGISTRY - ALLE 85+ FELDER DEFINIERT
# ============================================================================

FIELD_DEFINITIONS: dict[str, Field] = {
    # UNIVERSELLE FELDER
    "notes": Field(
        key="notes",
        label="Notizen",
        field_type=FieldType.TEXT,
        chart_type=ChartType.NONE,
        required=False,
        hidden=False,
        description="Zusätzliche Notizen zur Session"
    ),

    # ========== DISTANZ & BEWEGUNG ==========
    "distance": Field(
        key="distance",
        label="Distanz",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.BOTH,
        unit="km",
        required=True,
        hidden=False,
        min_value=0,
        description="Zurückgelegte Distanz"
    ),
    "average_distance": Field(
        key="average_distance",
        label="⌀ Distanz",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="km",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),
    "number_of_steps": Field(
        key="number_of_steps",
        label="Schritte",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="Schritte",
        required=False,
        hidden=False,
        min_value=0,
    ),
    "average_number_of_steps": Field(
        key="average_number_of_steps",
        label="⌀ Schritte",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="Schritte",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),

    # ========== ZEIT & DAUER ==========
    "duration": Field(
        key="duration",
        label="Dauer",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.BOTH,
        unit="min",
        required=True,
        hidden=False,
        min_value=0,
        description="Dauer in Minuten"
    ),
    "average_duration": Field(
        key="average_duration",
        label="⌀ Dauer",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="min",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),

    # ========== GESCHWINDIGKEIT (BERECHNET) ==========
    "velocity": Field(
        key="velocity",
        label="Geschwindigkeit",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.LINE,
        unit="km/h",
        required=False,
        hidden=True,
        calculator="calculate_velocity",
    ),
    "average_velocity": Field(
        key="average_velocity",
        label="⌀ Geschwindigkeit",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="km/h",
        required=False,
        hidden=True,
        calculator="calculate_average_velocity",
    ),

    # ========== PAUSEN ==========
    "number_of_breaks": Field(
        key="number_of_breaks",
        label="Anzahl Pausen",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BAR,
        required=False,
        hidden=False,
        min_value=0,
    ),
    "break_duration": Field(
        key="break_duration",
        label="Pausendauer",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.BOTH,
        unit="min",
        required=False,
        hidden=False,
        min_value=0,
    ),

    # ========== INTENSITÄT & QUALITÄT ==========
    "movement_intensity": Field(
        key="movement_intensity",
        label="Intensität",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["sehr leicht", "leicht", "mittel", "intensiv", "sehr intensiv"],
    ),
    "route_type": Field(
        key="route_type",
        label="Streckentyp",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["asphalt", "schotter", "pfad", "wald", "mix"],
    ),
    "weather": Field(
        key="weather",
        label="Wetter",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["sonnig", "bewölkt", "regnerisch", "schneereich", "windig", "neblig"],
    ),

    # ========== KALORIENVERBRAUCH & ENERGIE ==========
    "calorie_consumption": Field(
        key="calorie_consumption",
        label="Kalorienverbrauch",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="kcal",
        required=False,
        hidden=False,
        min_value=0,
    ),
    "altitude": Field(
        key="altitude",
        label="Höhenmeter",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.BOTH,
        unit="m",
        required=False,
        hidden=False,
        min_value=0,
    ),

    # ========== SCHWIMMEN ==========
    "swimming_style": Field(
        key="swimming_style",
        label="Schwimmstil",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["freistil", "rückenschwimmen", "brustschwimmen", "schmetterling", "gemischt"],
    ),

    # ========== WORKOUT & TRAINING ==========
    "workout_type": Field(
        key="workout_type",
        label="Trainingsart",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["kraft", "ausdauer", "flexibilität", "gemischt", "yoga", "pilates"],
    ),
    "number_of_exercises": Field(
        key="number_of_exercises",
        label="Anzahl Übungen",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="Übungen",
        required=False,
        hidden=False,
        min_value=0,
    ),

    # ========== LESEN & SCHREIBEN ==========
    "number_of_pages": Field(
        key="number_of_pages",
        label="Seiten",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="Seiten",
        required=False,
        hidden=False,
        min_value=0,
    ),
    "pages_per_hour": Field(
        key="pages_per_hour",
        label="Seiten/Stunde",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="Seiten/h",
        required=False,
        hidden=True,
        calculator="calculate_pages_per_hour",
    ),
    "pages_per_minute": Field(
        key="pages_per_minute",
        label="Seiten/Minute",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="Seiten/min",
        required=False,
        hidden=True,
        calculator="calculate_pages_per_minute",
    ),
    "reading_medium": Field(
        key="reading_medium",
        label="Lesemedium",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["papierbuch", "ebook", "hörbuch", "artikel"],
    ),
    "writing_medium": Field(
        key="writing_medium",
        label="Schreibmedium",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["papier", "digital", "handschrift"],
    ),

    # ========== KONZENTRATION & FOKUS ==========
    "concentration_value": Field(
        key="concentration_value",
        label="Konzentration",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="%",
        required=False,
        hidden=False,
        min_value=0,
        max_value=100,
    ),
    "average_concentration_value": Field(
        key="average_concentration_value",
        label="⌀ Konzentration",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="%",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),
    "success_value": Field(
        key="success_value",
        label="Erfolgswert",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="%",
        required=False,
        hidden=False,
        min_value=0,
        max_value=100,
    ),
    "average_success_value": Field(
        key="average_success_value",
        label="⌀ Erfolgswert",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="%",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),
    "focus_level": Field(
        key="focus_level",
        label="Fokus",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
    ),
    "average_focus_level": Field(
        key="average_focus_level",
        label="⌀ Fokus",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="0-10",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),

    # ========== SCHLAF ==========
    "sleep_quality": Field(
        key="sleep_quality",
        label="Schlafqualität",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="%",
        required=False,
        hidden=False,
        min_value=0,
        max_value=100,
    ),
    "average_sleep_quality": Field(
        key="average_sleep_quality",
        label="⌀ Schlafqualität",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="%",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),
    "number_of_wakeups": Field(
        key="number_of_wakeups",
        label="Aufwachanzahl",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BAR,
        required=False,
        hidden=False,
        min_value=0,
    ),

    # ========== GETRÄNKE & WASSER ==========
    "amount": Field(
        key="amount",
        label="Menge",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.BOTH,
        unit="ml",
        required=True,
        hidden=False,
        min_value=0,
    ),
    "average_amount": Field(
        key="average_amount",
        label="⌀ Menge",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="ml",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),
    "water_source": Field(
        key="water_source",
        label="Wasserquelle",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["leitung", "flasche", "brunnen", "fluss", "sonstig"],
    ),
    "water_temperature": Field(
        key="water_temperature",
        label="Wassertemperatur",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["eiskalt", "kalt", "kühl", "zimmertemperatur", "warm", "heiß"],
    ),
    "drink_type": Field(
        key="drink_type",
        label="Getränketyp",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["wasser", "kaffee", "tee", "limonade", "saft", "milch", "alkohol", "sonstig"],
    ),
    "drink_temperature": Field(
        key="drink_temperature",
        label="Getränketemperatur",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["eiskalt", "kalt", "zimmertemperatur", "warm", "heiß"],
    ),
    "alcohol_type": Field(
        key="alcohol_type",
        label="Alkoholtyp",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["bier", "wein", "spirituosen", "cocktail", "apfelwein"],
    ),
    "occasion": Field(
        key="occasion",
        label="Anlass",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["feier", "gesellig", "entspannung", "stressabbau", "sonstig"],
    ),

    # ========== RAUCHEN ==========
    "smoke_amount": Field(
        key="smoke_amount",
        label="Rauchmenge",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        required=False,
        hidden=False,
        min_value=0,
    ),
    "average_smoke_amount": Field(
        key="average_smoke_amount",
        label="⌀ Rauchmenge",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),
    "craving_intensity": Field(
        key="craving_intensity",
        label="Verlangen Intensität",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="%",
        required=False,
        hidden=False,
        min_value=0,
        max_value=100,
    ),

    # ========== STIMMUNG & EMOTIONEN ==========
    "mood_value": Field(
        key="mood_value",
        label="Stimmung",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=True,
        hidden=False,
        min_value=0,
        max_value=10,
    ),
    "average_mood_value": Field(
        key="average_mood_value",
        label="⌀ Stimmung",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="0-10",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),
    "stress_value": Field(
        key="stress_value",
        label="Stress",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=True,
        hidden=False,
        min_value=0,
        max_value=10,
    ),
    "average_stress_value": Field(
        key="average_stress_value",
        label="⌀ Stress",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="0-10",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),
    "energy_level": Field(
        key="energy_level",
        label="Energie",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=True,
        hidden=False,
        min_value=0,
        max_value=10,
    ),
    "average_energy_level": Field(
        key="average_energy_level",
        label="⌀ Energie",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="0-10",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),
    "motivation_value": Field(
        key="motivation_value",
        label="Motivation",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=True,
        hidden=False,
        min_value=0,
        max_value=10,
    ),
    "average_motivation_value": Field(
        key="average_motivation_value",
        label="⌀ Motivation",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="0-10",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),
    "main_mood": Field(
        key="main_mood",
        label="Hauptgefühl",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["freude", "traurigkeit", "wut", "angst", "überraschung", "ekel", "neutral"],
    ),
    "trigger": Field(
        key="trigger",
        label="Auslöser",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["arbeit", "beziehung", "gesundheit", "geld", "familie", "soziales", "sonstig"],
    ),
    "time_of_day": Field(
        key="time_of_day",
        label="Tageszeit",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["morgen", "mittag", "abend", "nacht"],
    ),
    "obstacle": Field(
        key="obstacle",
        label="Hindernis",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["zeit", "motivation", "energie", "geld", "gesundheit", "wetter", "sonstig"],
    ),
    "physical_discomfort": Field(
        key="physical_discomfort",
        label="Körperliches Unbehagen",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
    ),
    "average_physical_discomfort": Field(
        key="average_physical_discomfort",
        label="⌀ Körperliches Unbehagen",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="0-10",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),

    # ========== KÖRPER & MENTAL ==========
    "physical_energy": Field(
        key="physical_energy",
        label="Körperliche Energie",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
    ),
    "average_physical_energy": Field(
        key="average_physical_energy",
        label="⌀ Körperliche Energie",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="0-10",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),
    "mental_energy": Field(
        key="mental_energy",
        label="Mentale Energie",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
    ),
    "average_mental_energy": Field(
        key="average_mental_energy",
        label="⌀ Mentale Energie",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="0-10",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),
    "self_confidence": Field(
        key="self_confidence",
        label="Selbstvertrauen",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
    ),
    "average_self_confidence": Field(
        key="average_self_confidence",
        label="⌀ Selbstvertrauen",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="0-10",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),
    "anxiety_level": Field(
        key="anxiety_level",
        label="Angstzustand",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
    ),
    "average_anxiety_level": Field(
        key="average_anxiety_level",
        label="⌀ Angstzustand",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="0-10",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),

    # ========== ERNÄHRUNG ==========
    "meal_type": Field(
        key="meal_type",
        label="Mahlzeittyp",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["frühstück", "mittagessen", "abendessen", "snack", "dessert"],
    ),
    "food_quality": Field(
        key="food_quality",
        label="Lebensmittelqualität",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["sehr ungesund", "ungesund", "neutral", "gesund", "sehr gesund"],
    ),
    "portion_size": Field(
        key="portion_size",
        label="Portionsgröße",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["sehr klein", "klein", "mittel", "groß", "sehr groß"],
    ),
    "hunger_level": Field(
        key="hunger_level",
        label="Hungerlevel",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
    ),
    "satiety_level": Field(
        key="satiety_level",
        label="Sättigungsgefühl",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
    ),

    # ========== BILDSCHIRMZEIT & GERÄTE ==========
    "device_type": Field(
        key="device_type",
        label="Gerätetyp",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["telefon", "tablet", "laptop", "desktop", "smartwatch"],
    ),
    "device_main_use": Field(
        key="device_main_use",
        label="Hauptnutzung",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["arbeit", "kommunikation", "unterhaltung", "bildung", "sonstig"],
    ),

    # ========== LERNFORMAT & SPRACHE ==========
    "learn_format": Field(
        key="learn_format",
        label="Lernformat",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["video", "buch", "interaktiv", "praktisch", "gruppe"],
    ),
    "language": Field(
        key="language",
        label="Sprache",
        field_type=FieldType.TEXT,
        chart_type=ChartType.NONE,
        required=True,
        hidden=False,
        description="Lernsprache (z.B. Spanisch, Französisch)"
    ),
    "language_training_type": Field(
        key="language_training_type",
        label="Trainingstyp",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["sprechen", "hören", "lesen", "schreiben", "grammatik", "vokabeln"],
    ),

    # ========== AUSGABEN & FINANZEN ==========
    "costs_amount": Field(
        key="costs_amount",
        label="Ausgabenbetrag",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.BOTH,
        unit="€",
        required=True,
        hidden=False,
        min_value=0,
    ),
    "average_costs_amount": Field(
        key="average_costs_amount",
        label="⌀ Ausgabenbetrag",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="€",
        required=False,
        hidden=True,
        calculator="calculate_average",
    ),

    # ========== ORT & SOZIALES ==========
    "location_type": Field(
        key="location_type",
        label="Ort",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["zuhause", "arbeit", "draußen", "fitnessstudio", "park", "öffentlich"],
    ),
    "social_context": Field(
        key="social_context",
        label="Sozialer Kontext",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["allein", "mit freund", "mit familie", "mit gruppe", "mit partner"],
    ),

    # ========== HAUSHALT ==========
    "household_task": Field(
        key="household_task",
        label="Haushaltsaufgabe",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["küche", "wohnzimmer", "schlafzimmer", "badezimmer", "wäsche", "putzen"],
    ),
    "house_area": Field(
        key="house_area",
        label="Wohnungsbereich",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["küche", "wohnzimmer", "schlafzimmer", "badezimmer", "wäsche", "putzen"],
    ),

    # ========== STATUS ==========
    "status": Field(
        key="status",
        label="Status",
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=["geplant", "in_progress", "completed", "pausiert", "abgebrochen"],
    ),
}


class FieldManager:
    """
    Zentrale Verwaltung aller Feldoperationen
    Single Point of Truth für alle Field-Definitionen
    """

    @staticmethod
    def get_field(field_key: str) -> Optional[Field]:
        """Gibt ein einzelnes Field zurück"""
        return FIELD_DEFINITIONS.get(field_key)

    @staticmethod
    def get_all_fields() -> dict[str, Field]:
        """Gibt alle Felder zurück"""
        return FIELD_DEFINITIONS.copy()

    @staticmethod
    def get_required_fields() -> List[Field]:
        """Gibt alle Pflichtfelder zurück"""
        return [f for f in FIELD_DEFINITIONS.values() if f.required]

    @staticmethod
    def get_trackable_fields() -> List[Field]:
        """Gibt alle nicht-versteckten (User-eingabe) Felder zurück"""
        return [f for f in FIELD_DEFINITIONS.values() if not f.hidden]

    @staticmethod
    def get_hidden_fields() -> List[Field]:
        """Gibt alle berechneten Felder zurück"""
        return [f for f in FIELD_DEFINITIONS.values() if f.hidden]

    @staticmethod
    def get_chart_fields() -> List[Field]:
        """Gibt Felder zurück, die in Diagrammen angezeigt werden können"""
        return [f for f in FIELD_DEFINITIONS.values() if f.chart_type.value != "none"]

    @staticmethod
    def validate_value(field_key: str, value: Any) -> tuple[bool, Optional[str]]:
        """Validiert einen Wert gegen sein Field"""
        field = FIELD_DEFINITIONS.get(field_key)
        if not field:
            return False, f"Feld '{field_key}' existiert nicht"
        return field.validate(value)

    @staticmethod
    def validate_session_values(field_keys: List[str], values: dict[str, Any]) -> tuple[bool, dict[str, str]]:
        """Validiert alle Werte einer Session"""
        errors = {}
        for field_key in field_keys:
            if field_key in values:
                is_valid, error_msg = FieldManager.validate_value(field_key, values[field_key])
                if not is_valid:
                    errors[field_key] = error_msg
        return len(errors) == 0, errors
