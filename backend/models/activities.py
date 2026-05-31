from dataclasses import dataclass, field as dataclass_field
from typing import Optional, List, Callable
import logging
from .enums import *
from .field import FIELD_DEFINITIONS

logger = logging.getLogger(__name__)

@dataclass
class Field:
    name: str
    type: str
    unit: Optional[str] = None
    values: Optional[List[str]] = None
    chart_type: str = "both"
    required: bool = False
    hidden: bool = False
    calculator: Optional[Callable] = None

    def to_dict(self) -> dict:
        data = {
            "name": self.name,
            "type": self.type,
            "chart_type": self.chart_type,
            "required": self.required,
            "hidden": self.hidden,
        }
        if self.unit is not None:
            data["unit"] = self.unit
        if self.values is not None:
            data["values"] = self.values
        return data

def calc_geschwindigkeit_kmh(session: dict) -> Optional[float]:
    if "distanz_km" in session and "dauer_min" in session:
        distanz = session.get("distanz_km")
        dauer = session.get("dauer_min")
        if distanz and dauer and dauer > 0:
            return round((distanz / dauer) * 60, 2)
    return None

def calc_seiten_pro_stunde(session: dict) -> Optional[float]:
    if "seiten_anzahl" in session and "dauer_min" in session:
        seiten = session.get("seiten_anzahl")
        dauer = session.get("dauer_min")
        if seiten and dauer and dauer > 0:
            return round((seiten / dauer) * 60, 2)
    return None

def calc_gesamtanzahl_liegestutze(session: dict) -> Optional[int]:
    if "sets_anzahl" in session and "durchschnitt_pro_set" in session:
        sets = session.get("sets_anzahl")
        avg = session.get("durchschnitt_pro_set")
        if sets and avg:
            return int(sets * avg)
    return None

def calc_durchschnittliche_geschwindigkeit_schwimmen(session: dict) -> Optional[float]:
    if "distanz_m" in session and "dauer_min" in session:
        distanz = session.get("distanz_m")
        dauer = session.get("dauer_min")
        if distanz and dauer and dauer > 0:
            return round((distanz / dauer) * 60, 2)
    return None

ACTIVITIES: dict[str, list[str]] = {
    ActivityType.CYCLING.value: [
        "notes", "date", "time",
        "distance", "duration", "velocity", "number_of_breaks", "break_duration", "calorie_consumption", "altitude", "max_speed", "elevation_gain", "elevation_loss", "cadence", "heart_rate", "recovery_time", "humidity", "wind_speed",
        "WeatherType", "RouteType", "TimeOfDayType", "InitiatorType",
        "clarity_range", "discipline_range", "energy_range", "fitness_level_range", "focus_range", "mood_range", "motivation_range", "movement_intensity_range", "physical_discomfort_range", "physical_energy_range", "success_range", "sugar_craving_range", "tension_range", 
        # hier davor und danach messen?
    # Vielleicht so?:
        # "metrics": [...]
        # "context": [...]
        # "body": [...]
        # "mental": [...]
    ],
    ActivityType.JOGGING.value: [
        "notes", "date", "time",
        "distance", "number_of_steps", "duration", "velocity", "number_of_breaks", "break_duration", "calorie_consumption", "altitude", "max_speed", "elevation_gain", "elevation_loss", "cadence", "heart_rate", "recovery_time", "humidity", "wind_speed",
        "WeatherType", "RouteType", "TimeOfDayType", "InitiatorType",
        "clarity_range", "discipline_range", "energy_range", "fitness_level_range", "focus_range", "mood_range", "motivation_range", "movement_intensity_range", "physical_discomfort_range", "physical_energy_range", "success_range", "sugar_craving_range", "tension_range", 
    ],
    ActivityType.WANDERING.value: [
        "notes", "date", "time",
        "distance", "number_of_steps", "duration", "velocity", "number_of_breaks", "break_duration", "calorie_consumption", "altitude", "elevation_gain", "elevation_loss", "cadence", "heart_rate", "recovery_time", "humidity",
        "WeatherType", "RouteType", "TimeOfDayType", "InitiatorType",
        "clarity_range", "discipline_range", "energy_range", "fitness_level_range", "focus_range", "mood_range", "motivation_range", "movement_intensity_range", "physical_discomfort_range", "physical_energy_range", "success_range", "sugar_craving_range", "tension_range", 
    ],

}



# GoalType Definitionen pro Aktivität
# Diese Struktur definiert, welche GoalTypes für welche Aktivität verfügbar sind
# und enthält die Standard-Konfiguration für jeden GoalType
ACTIVITY_GOAL_TYPES: dict[str, dict] = {
    ActivityType.JOGGING.value: {
        "MORE_THAN": {
            "label": "Gesamtdistanz pro Periode",
            "description": "Joggen Sie insgesamt mindestens X km pro Periode",
            "default_unit": "km",
            "default_metric": "distance",
            "default_period": "monthly",
            "example": "120 km pro Monat"
        },
        "FREQUENCY_MIN": {
            "label": "Mindestens X Sessions",
            "description": "Mindestens X-mal pro Periode joggen gehen",
            "default_period": "weekly",
            "example": "3 mal pro Woche oder 20 mal pro Monat"
        },
        "AVERAGE_ABOVE": {
            "label": "Durchschnittliche Dauer",
            "description": "Jede Session soll durchschnittlich mindestens X Minuten sein",
            "default_metric": "duration",
            "default_unit": "minutes",
            "example": "mindestens 30 Minuten pro Session"
        },
        "RECURRENCE_PATTERN": {
            "label": "An bestimmten Wochentagen",
            "description": "Joggen Sie an bestimmten Wochentagen",
            "example": "Jeden Dienstag, Mittwoch und Samstag"
        }
    },
    ActivityType.CYCLING.value: {},
    ActivityType.WANDERING.value: {},
}


def get_available_goal_types(activity: str) -> dict:
    """Gibt die verfügbaren GoalTypes für eine Aktivität zurück"""
    try:
        return ACTIVITY_GOAL_TYPES.get(activity, {})
    except Exception:
        logger.exception(f"Failed to get available goal types for {activity}")
        return {}


def get_activity_names() -> list[str]:
    """Returns all available activity names."""
    try:
        return sorted(list(ACTIVITIES.keys()))
    except Exception:
        logger.exception("Failed to get activity names")
        return []


def get_fields(activity: str) -> list[dict]:
    """Returns all fields for a specific activity as dicts."""
    try:
        field_keys = ACTIVITIES.get(activity, [])
        result = []
        for key in field_keys:
            if key in FIELD_DEFINITIONS:
                field_obj = FIELD_DEFINITIONS[key]
                field_dict = {
                    "name": field_obj.key,  # Use "name" for frontend compatibility
                    "key": field_obj.key,
                    "label": field_obj.label,
                    "type": field_obj.field_type.value,  # Use "type" for frontend
                    "field_type": field_obj.field_type.value,
                    "chart_type": field_obj.chart_type.value,
                    "required": field_obj.required,
                    "hidden": field_obj.hidden,
                    "unit": field_obj.unit,
                    "options": field_obj.options,
                }
                result.append(field_dict)
        return result
    except Exception:
        logger.exception("Failed to get fields for activity %s", activity)
        return []


def get_field_objects(activity: str) -> list:
    """Returns all field objects for a specific activity."""
    try:
        field_keys = ACTIVITIES.get(activity, [])
        return [FIELD_DEFINITIONS[key] for key in field_keys if key in FIELD_DEFINITIONS]
    except Exception:
        logger.exception("Failed to get field objects for %s", activity)
        return []


def get_required_fields(activity: str) -> list[str]:
    """Returns required field names for an activity."""
    try:
        field_keys = ACTIVITIES.get(activity, [])
        return [key for key in field_keys
                if key in FIELD_DEFINITIONS and FIELD_DEFINITIONS[key].required and not FIELD_DEFINITIONS[key].hidden]
    except Exception:
        logger.exception(f"Failed to get required fields for {activity}")
        return []


def get_hidden_fields(activity: str) -> list[str]:
    """Returns hidden (calculated) field names for an activity."""
    try:
        field_keys = ACTIVITIES.get(activity, [])
        return [key for key in field_keys if key in FIELD_DEFINITIONS and FIELD_DEFINITIONS[key].hidden]
    except Exception:
        logger.exception(f"Failed to get hidden fields for {activity}")
        return []


def calculate_hidden_fields(activity: str, session: dict) -> dict:
    """
    Calculates all hidden fields for a session.
    
    Args:
        activity: Activity name
        session: Session data dict
    
    Returns:
        Dict with calculated field values
    """
    calculated = {}
    try:
        fields = ACTIVITIES.get(activity, [])
        for field in fields:
            if field.hidden and field.calculator:
                try:
                    value = field.calculator(session)
                    if value is not None:
                        calculated[field.name] = value
                except Exception as e:
                    logger.warning(f"Failed to calculate {field.name}: {e}")
        return calculated
    except Exception:
        logger.exception(f"Failed to calculate hidden fields for {activity}")
        return {}


def get_numeric_fields(activity: str, chart_type: Optional[str] = None) -> list[str]:
    try:
        field_keys = ACTIVITIES.get(activity, [])
        numeric = [
            key for key in field_keys
            if key in FIELD_DEFINITIONS
            and FIELD_DEFINITIONS[key].field_type.value in ["number", "integer"]
            and FIELD_DEFINITIONS[key].chart_type.value != "none"
            and not FIELD_DEFINITIONS[key].hidden
        ]

        if chart_type:
            numeric = [
                key for key in field_keys
                if key in FIELD_DEFINITIONS
                and FIELD_DEFINITIONS[key].field_type.value in ["number", "integer"]
                and (FIELD_DEFINITIONS[key].chart_type.value == chart_type or FIELD_DEFINITIONS[key].chart_type.value == "both")
                and FIELD_DEFINITIONS[key].chart_type.value != "none"
                and not FIELD_DEFINITIONS[key].hidden
            ]

        return numeric
    except Exception:
        logger.exception(f"Failed to get numeric fields for {activity}")
        return []


def get_enum_fields(activity: str) -> list[str]:
    try:
        field_keys = ACTIVITIES.get(activity, [])
        return [key for key in field_keys
                if key in FIELD_DEFINITIONS
                and FIELD_DEFINITIONS[key].field_type.value == "enum"
                and FIELD_DEFINITIONS[key].chart_type.value in ["enum_bar", "both"]]
    except Exception:
        logger.exception(f"Failed to get enum fields for {activity}")
        return []


def get_category_fields(activity: str) -> list[str]:
    try:
        field_keys = ACTIVITIES.get(activity, [])
        return [key for key in field_keys
                if key in FIELD_DEFINITIONS
                and FIELD_DEFINITIONS[key].field_type.value == "enum"
                and FIELD_DEFINITIONS[key].chart_type.value == "none"]
    except Exception:
        logger.exception(f"Failed to get category fields for {activity}")
        return []


def get_field_unit(activity: str, field_name: str) -> Optional[str]:
    try:
        field_keys = ACTIVITIES.get(activity, [])
        for key in field_keys:
            if key == field_name and key in FIELD_DEFINITIONS:
                return FIELD_DEFINITIONS[key].unit
        return None
    except Exception:
        logger.exception(f"Failed to get unit for {activity}.{field_name}")
        return None


def get_comparison_features(activity: str) -> List[str]:
    return COMPARISON_FEATURES.get(activity, [])