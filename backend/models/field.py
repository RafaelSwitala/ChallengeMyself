"""
Zentrale Feldefinitionen für alle 85+ Felder
Definiert die Field-Klasse und zentrale Field-Registry mit FieldManager
"""

from dataclasses import dataclass
from typing import Optional, List, Any, Type
from .enums import *


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
    unit: Optional[str] = None         # z.B. "km", "min", "%"
    required: bool = False              # Pflichtfeld?
    hidden: bool = False                # Berechnetes Feld (nicht von User eingegeben)
    options: Optional[List[str]] = None # Enum-Optionen
    description: Optional[str] = None   # Dokumentation
    min_value: Optional[float] = None   # Validierung: Minimum
    max_value: Optional[float] = None   # Validierung: Maximum
    calculator: Optional[str] = None    # Funktionsreferenz für Hidden Fields
    average_possible: bool = False      # Kann ein Durchschnitt berechnet werden?

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
# HELPER-FUNKTIONEN FÜR ENUM-FIELD GENERIERUNG
# ============================================================================

def create_enum_field(enum_cls: Type[Enum], custom_label: Optional[str] = None, custom_key: Optional[str] = None) -> Field:
    """
    Generiert automatisch ein Field aus einem Enum-Klasse.

    Args:
        enum_cls: Die Enum-Klasse (z.B. WeatherType, RouteType)
        custom_label: Optionales benutzerdefiniertes Label (z.B. "Wetter" statt "WeatherType")
        custom_key: Optionaler benutzerdefinierter Key
    """
    key = custom_key or enum_cls.__name__
    label = custom_label or enum_cls.__name__

    return Field(
        key=key,
        label=label,
        field_type=FieldType.ENUM,
        chart_type=ChartType.ENUM_BAR,
        required=False,
        hidden=False,
        options=[x.value for x in enum_cls],
    )


# ============================================================================
# ENUM-TYPEN FÜR AUTOMATISCHE FIELD-GENERIERUNG
# ============================================================================

ENUM_TYPES_WITH_LABELS = {
    # Key: Enum-Klasse, Value: Benutzer-freundliches Label
    WeatherType: "Wetter",
    RouteType: "Streckentyp",
    MovementIntensityType: "Intensität",
    AlcoholType: "Alkoholtyp",
    AnxietyReasonType: "Angst-Grund",
    CunsumptionMethodType: "Konsummethode",
    BudgetCategoryType: "Budget-Kategorie",
    CommunityActivityType: "Gemeinschaftsaktivität",
    ConsumptionProductType: "Verbrauchsprodukt",
    CulturalEventType: "Kulturelle Veranstaltung",
    DeviceMainUseType: "Hauptnutzung Gerät",
    DeviceType: "Gerätetyp",
    DrinkTemperatureType: "Getränk-Temperatur",
    DrinkType: "Getränketyp",
    EatingContextType: "Ess-Kontext",
    ExpensesType: "Ausgabentyp",
    FoodQualityType: "Lebensmittelqualität",
    HabitType: "Gewohnheitstyp",
    HealthCheckType: "Gesundheitscheck",
    HouseAreaType: "Wohnbereich",
    HouseholdTaskType: "Haushaltsaufgabe",
    ImmuneBoostType: "Immunstärkung",
    IncomeType: "Einkommenstype",
    InitiatorType: "Initiator",
    InvestmentTypes: "Investitionstyp",
    LanguageTrainingType: "Sprachtraining",
    LearningFormatType: "Lernformat",
    LocationType: "Ort",
    MainMoodType: "Hauptstimmung",
    MealType: "Mahlzeittyp",
    MentalExerciseType: "Mentale Übung",
    MindfulnessExerciseType: "Achtsamkeitsübung",
    MotivationReferenceType: "Motivations-Bezug",
    ObstacleType: "Hindernis",
    OcassionType: "Anlass",
    PortionSizeType: "Portionsgröße",
    ReadingMediumType: "Lesemedium",
    ReflectionType: "Reflexionstyp",
    SavingGoalType: "Sparziel",
    SideEffectType: "Nebenwirkung",
    SkillTrainingType: "Skill-Training",
    SnackType: "Snack-Typ",
    SocialContextType: "Sozialer Kontext",
    SportType: "Sporttyp",
    StatusType: "Status",
    SubstanceType: "Substanztyp",
    SwimmingStyleType: "Schwimmstil",
    TimeOfDayType: "Tageszeit",
    TravelType: "Reiseart",
    TriggerType: "Auslöser",
    VolunteeringType: "Freiwilligenarbeit",
    WaterSourceType: "Wasserquelle",
    WaterTemperatureType: "Wassertemperatur",
    WeatherExposureType: "Wetter-Exposition",
    WorkoutType: "Trainingstyp",
    WritingMediumType: "Schreibmedium",
}

# Generiere automatisch alle Enum Fields
ENUM_FIELDS = {
    create_enum_field(enum_cls, label).key: create_enum_field(enum_cls, label)
    for enum_cls, label in ENUM_TYPES_WITH_LABELS.items()
}


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
        average_possible=True,
        description="Zurückgelegte Distanz"
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
        average_possible=True,
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
        average_possible=True,
        description="Dauer in Minuten"
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
        average_possible=True,
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
        average_possible=True,
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
        average_possible=True,
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
        average_possible=True,
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
        average_possible=True,
    ),

    # ========== TRAININGSPARAMETER ==========
    "number_of_exercises": Field(
        key="number_of_exercises",
        label="Anzahl Übungen",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="Übungen",
        required=False,
        hidden=False,
        min_value=0,
        average_possible=True,
    ),

    # ========== SEITENANZAHL & LESEN ==========
    "number_of_pages": Field(
        key="number_of_pages",
        label="Seiten",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="Seiten",
        required=False,
        hidden=False,
        min_value=0,
        average_possible=True,
    ),

    # ========== KONZENTRATION & FOKUS (0-10 RANGE) ==========
    "concentration_value": Field(
        key="concentration_value",
        label="Konzentration",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
        average_possible=True,
    ),
    "success_value": Field(
        key="success_value",
        label="Erfolgswert",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
        average_possible=True,
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
        average_possible=True,
    ),

    # ========== SCHLAF ==========
    "sleep_quality": Field(
        key="sleep_quality",
        label="Schlafqualität",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
        average_possible=True,
    ),
    "number_of_wakeups": Field(
        key="number_of_wakeups",
        label="Aufwachanzahl",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BAR,
        required=False,
        hidden=False,
        min_value=0,
        average_possible=True,
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
        average_possible=True,
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
        average_possible=True,
    ),
    "craving_intensity": Field(
        key="craving_intensity",
        label="Verlangen Intensität",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
        average_possible=True,
    ),

    # ========== STIMMUNG & EMOTIONEN (0-10 RANGE) ==========
    "mood_value": Field(
        key="mood_value",
        label="Stimmung",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
        average_possible=True,
    ),
    "stress_value": Field(
        key="stress_value",
        label="Stress",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
        average_possible=True,
    ),
    "energy_level": Field(
        key="energy_level",
        label="Energie",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
        average_possible=True,
    ),
    "motivation_value": Field(
        key="motivation_value",
        label="Motivation",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BOTH,
        unit="0-10",
        required=False,
        hidden=False,
        min_value=0,
        max_value=10,
        average_possible=True,
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
        average_possible=True,
    ),

    # ========== KÖRPER & MENTAL (0-10 RANGE) ==========
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
        average_possible=True,
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
        average_possible=True,
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
        average_possible=True,
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
        average_possible=True,
    ),

    # ========== ERNÄHRUNG ==========
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
        average_possible=True,
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
        average_possible=True,
    ),

    # ========== AUSGABEN & FINANZEN ==========
    "costs_amount": Field(
        key="costs_amount",
        label="Ausgabenbetrag",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.BOTH,
        unit="€",
        required=False,
        hidden=False,
        min_value=0,
        average_possible=True,
    ),

    # ========== ENUM-TYPES (AUTOMATISCH GENERIERT) ==========
    **ENUM_FIELDS
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
        return [f for f in FIELD_DEFINITIONS.values() if f.chart_type != ChartType.NONE]

    @staticmethod
    def get_average_fields() -> List[Field]:
        """Gibt Felder zurück, für die Durchschnitte berechnet werden können"""
        return [f for f in FIELD_DEFINITIONS.values() if f.average_possible and f.field_type in [FieldType.NUMBER, FieldType.INTEGER]]

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
