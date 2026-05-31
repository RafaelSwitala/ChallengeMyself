from dataclasses import dataclass
from typing import Optional, List, Any, Type
from .enums import *


@dataclass
class Field:
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


# --------- HELPER-FUNKTIONEN FÜR ENUM-FIELD GENERIERUNG

def create_enum_field(enum_cls: Type[Enum], custom_label: Optional[str] = None, custom_key: Optional[str] = None) -> Field:
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


def create_range_field(key: str, label: str) -> Field:
    return Field(
        key=key,
        label=label,
        field_type=FieldType.INTEGER,
        chart_type=ChartType.VALUE,
        unit=None,
        required=True,
        hidden=False,
        min_value=0,
        max_value=10,
        average_possible=True,
    )

# --------- ENUM-TYPEN FÜR AUTOMATISCHE FIELD-GENERIERUNG
ENUM_TYPES_WITH_LABELS = {
    AlcoholType: "Alkoholtyp",
    AnxietyReasonType: "Angst-Grund",
    BreakReasonType: "Pausengrund",
    BreakType: "Art der Pause",
    BudgetCategoryType: "Budget-Kategorie",
    CommunityActivityType: "Gemeinschaftsaktivität",
    ConsumptionProductType: "Verbrauchsprodukt",
    CulturalEventType: "Kulturelle Veranstaltung",
    ConsumptionMethodType: "Konsummethode",
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
    RouteType: "Streckentyp",
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
    WeatherType: "Wetter",
    WorkoutType: "Trainingstyp",
    WritingMediumType: "Schreibmedium",
}

ENUM_FIELDS = {
    create_enum_field(enum_cls, label).key: create_enum_field(enum_cls, label)
    for enum_cls, label in ENUM_TYPES_WITH_LABELS.items()
}

# --------- RANGE-FIELDS FÜR AUTOMATISCHE GENERIERUNG (0-10 SKALIERUNG)
RANGE_FIELDS_WITH_LABELS = {
    "air_quality_range": "Luftqualität",
    "anxiety_range": "Angstzustand",
    "appetite_range": "Appetit",
    "calmness_range": "Ruhe / Gelassenheit",
    "clarity_range": "Gedankliche Klarheit",
    "concentration_range": "Konzentration",
    "connection_range": "Verbundenheit",
    "consistency_range": "Konsistenz",
    "craving_intensity_range": "Verlangen Intensität",
    "creativity_range": "Kreativität",
    "decision_quality_range": "Entscheidungsqualität",
    "discipline_range": "Disziplin",
    "efficiency_range": "Effizienz",
    "emotional_balance_range": "Emotionale Balance",
    "energy_range": "Energie",
    "fitness_level_range": "Fitnesslevel",
    "focus_range": "Fokus",
    "food_quality_range": "Ernährungsqualität",
    "fulfillment_range": "Erfüllung",
    "fullness_comfort_range": "Völlegefühl / Wohlsein",
    "hunger_range": "Hungerlevel",
    "hydration_range": "Hydration",
    "immune_strength_range": "Immunsystem Stärke",
    "inner_tension_range": "Innere Anspannung",
    "irritability_range": "Reizbarkeit",
    "learning_efficiency_range": "Lerneffizienz",
    "loneliness_range": "Einsamkeit",
    "mental_energy_range": "Mentale Energie",
    "mental_load_range": "Mentale Belastung",
    "mood_range": "Stimmung",
    "motivation_range": "Motivation",
    "movement_intensity_range": "Bewegungsintensität",
    "overwhelm_range": "Überforderung",
    "pain_level_range": "Schmerzlevel",
    "patience_range": "Geduld",
    "perceived_exertion_range": "subjektive Anstrengung",
    "physical_discomfort_range": "Körperliches Unbehagen",
    "physical_energy_range": "Körperliche Energie",
    "productivity_range": "Produktivität",
    "purpose_range": "Sinnhaftigkeit",
    "recovery_range": "Erholung",
    "resilience_range": "Resilienz",
    "satiety_range": "Sättigungsgefühl",
    "self_awareness_range": "Selbstwahrnehmung",
    "self_confidence_range": "Selbstvertrauen",
    "sleep_quality_range": "Schlafqualität",
    "social_energy_range": "Soziale Energie",
    "social_satisfaction_range": "Soziale Zufriedenheit",
    "stress_range": "Stress",
    "success_range": "Erfolgswert",
    "sugar_craving_range": "Zuckerverlangen",
    "tension_range": "Muskelspannung",  
}

RANGE_FIELDS = {
    create_range_field(key, label).key: create_range_field(key, label)
    for key, label in RANGE_FIELDS_WITH_LABELS.items()
}


# --------- ZENTRALE FIELD-REGISTRY: Diese Fields sind in allen Activities:
FIELD_DEFINITIONS: dict[str, Field] = {
    "notes": Field(
        key="notes",
        label="Notizen",
        field_type=FieldType.TEXT,
        chart_type=ChartType.NONE,
        required=False,
        hidden=False,
        description="Zusätzliche Notizen zur Session"
    ),
    "date": Field(
        key="date",
        label="Datum",
        field_type=FieldType.DATE,
        chart_type=ChartType.NONE,
        required=True,
        hidden=False,
        description="Datum der Session"
    ),
    "time": Field(
        key="time",
        label="Uhrzeit",
        field_type=FieldType.DATE,
        chart_type=ChartType.NONE,
        required=False,
        hidden=False,
        description="Uhrzeit der Session"
    ),

# --------- INDIVIDUELLE FIELD-REGISTRY:
    "distance": Field(
        key="distance",
        label="Distanz",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.LINE,
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
        chart_type=ChartType.LINE,
        unit="Schritte",
        required=False,
        hidden=False,
        min_value=0,
        average_possible=True,
    ),
    "duration": Field(
        key="duration",
        label="Dauer",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.LINE,
        unit="min",
        required=True,
        hidden=False,
        min_value=0,
        average_possible=True,
        description="Dauer in Minuten"
    ),
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
        chart_type=ChartType.LINE,
        unit="min",
        required=False,
        hidden=False,
        min_value=0,
        average_possible=True,
    ),
    "calorie_consumption": Field(
        key="calorie_consumption",
        label="Kalorienverbrauch",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.LINE,
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
        chart_type=ChartType.LINE,
        unit="m",
        required=False,
        hidden=False,
        min_value=0,
        average_possible=True,
    ),
    "number_of_exercises": Field(
        key="number_of_exercises",
        label="Anzahl Übungen",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.BAR,
        unit="Übungen",
        required=False,
        hidden=False,
        min_value=0,
        average_possible=True,
    ),
    "number_of_pages": Field(
        key="number_of_pages",
        label="Seiten",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.LINE,
        unit="Seiten",
        required=False,
        hidden=False,
        min_value=0,
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
    "hydration_amount": Field(
        key="amount",
        label="Menge",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.LINE,
        unit="ml",
        required=True,
        hidden=False,
        min_value=0,
        average_possible=True,
    ),
    "smoke_amount": Field(
        key="smoke_amount",
        label="Rauchmenge",
        field_type=FieldType.INTEGER,
        chart_type=ChartType.LINE,
        required=False,
        hidden=False,
        min_value=0,
        average_possible=True,
    ),
    "costs_amount": Field(
        key="costs_amount",
        label="Ausgabenbetrag",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.LINE,
        unit="€",
        required=False,
        hidden=False,
        min_value=0,
        average_possible=True,
    ),
    "max_speed": Field(
        key="max_speed",
        label="Maximale Geschwindigkeit",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="km/h",
        required=False,
        hidden=True,
        average_possible=False,
        description="Maximale zurückgelegte Geschwindigkeit"
    ),
    "elevation_gain": Field(
        key="elevation_gain",
        label="Höhenmeter bergauf",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="m",
        required=False,
        hidden=True,
        average_possible=False,
        description="Höhenmeter bergauf"
    ),
    "elevation_loss": Field(
        key="elevation_loss",
        label="Höhenmeter bergab",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="m",
        required=False,
        hidden=True,
        average_possible=False,
        description="Höhenmeter bergab"
    ),
    "cadence": Field(
        key="cadence",
        label="Trittfrquenz",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.VALUE,
        unit="Schritte",
        required=False,
        hidden=True,
        average_possible=True,
        description="Schritte pro Minute",
        calculator="calculate_cadence",
    ),
    "heart_rate": Field(
        key="heart_rate",
        label="Puls",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.LINE,
        unit="",
        required=False,
        hidden=False,
        average_possible=True,
        description="Puls",
    ),
    "recovery_time": Field(
        key="recovery_time",
        label="Erholungszeit",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.BAR,
        unit="min",
        required=False,
        hidden=False,
        average_possible=True,
        description="Erholungszeit",
    ),
    "humidity": Field(
        key="humidity",
        label="Luftfeuchtigkeit",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.BAR,
        unit="%",
        required=False,
        hidden=False,
        average_possible=False,
        description="Luftfeuchtigkeit",
    ),
    "wind_speed": Field(
        key="wind_speed",
        label="Windgeschwindigkeit",
        field_type=FieldType.NUMBER,
        chart_type=ChartType.BAR,
        unit="m/s",
        required=False,
        hidden=False,
        average_possible=False,
        description="Windgeschwindigkeit",
    ),
    **ENUM_FIELDS,
    **RANGE_FIELDS
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
