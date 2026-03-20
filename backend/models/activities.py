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
    ActivityType.JOGGING.value: [
        "distance",
        "duration",
        "weather",
        "route_type",
        "notes"
    ],

    # "Radfahren": [
    #     Field("distanz_km", "number", "km", chart_type="line", required=True),
    #     Field("dauer_min", "number", "min", chart_type="line", required=True),
        
    #     Field("geschwindigkeit_kmh", "number", "km/h", chart_type="line", 
    #           hidden=True, calculator=calc_geschwindigkeit_kmh),
        
    #     Field("kalorienverbrauch", "number", "kcal", chart_type="line", required=False),
    #     Field("hoehenmeter", "number", "m", chart_type="line", required=False),
    #     Field("pausen_anzahl", "number", chart_type="both", required=False),
    #     Field("pausen_dauer_min", "number", "min", chart_type="both", required=False),
        
    #     Field("intensitaet", "enum", values=["gemütlich", "mittel", "stark"], 
    #           chart_type="enum_bar", required=False),
    #     Field("strecke_typ", "enum", values=["mix", "asphalt", "feldweg", "waldweg", "berg"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Spazieren": [
    #     Field("distanz_km", "number", "km", chart_type="line", required=True),
    #     Field("dauer_min", "number", "min", chart_type="line", required=True),
    #     Field("schritte_anzahl", "number", chart_type="both", required=False),
    #     Field("intensitaet", "enum", values=["gemütlich", "mittel", "flott"], 
    #           chart_type="enum_bar", required=False),
    #     Field("strecke_typ", "enum", values=["mix", "stadt", "natur", "park"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Schwimmen": [
    #     Field("distanz_m", "number", "m", chart_type="line", required=True),
    #     Field("dauer_min", "number", "min", chart_type="line", required=True),
        
    #     Field("durchschnittliche_geschwindigkeit_pro_min", "number", "m/min", chart_type="line",
    #           hidden=True, calculator=calc_durchschnittliche_geschwindigkeit_schwimmen),
        
    #     Field("kalorienverbrauch", "number", "kcal", chart_type="line", required=False),
    #     Field("pausen_anzahl", "number", chart_type="both", required=False),
    #     Field("beckenlaenge_m", "number", "m", chart_type="line", required=False),
        
    #     Field("schwimmstil", "enum", values=["kraul", "brust", "rücken", "delphin", "mix"], 
    #           chart_type="enum_bar", required=False),
    #     Field("intensitaet", "enum", values=["gemütlich", "mittel", "stark"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Workout": [
    #     Field("dauer_min", "number", "min", chart_type="line", required=True),
    #     Field("uebungen_anzahl", "number", chart_type="both", required=True),
    #     Field("kalorienverbrauch", "number", "kcal", chart_type="line", required=False),
        
    #     Field("trainingsart", "enum", values=["krafttraining", "ausdauer", "flexibilität", "mix"], 
    #           chart_type="enum_bar", required=False),
    #     Field("intensitaet", "enum", values=["gemütlich", "mittel", "stark"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Liegestütze": [
    #     Field("sets_anzahl", "number", chart_type="both", required=True),
    #     Field("durchschnitt_pro_set", "number", chart_type="line", required=True),
        
    #     Field("gesamtanzahl_liegestutze", "number", chart_type="line",
    #           hidden=True, calculator=calc_gesamtanzahl_liegestutze),
        
    #     Field("saubere_wiederholungen_anzahl", "number", chart_type="both", required=False),
    #     Field("intensitaet", "enum", values=["gemütlich", "mittel", "stark"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Lesen": [
    #     Field("dauer_min", "number", "min", chart_type="line", required=True),
    #     Field("seiten_anzahl", "number", chart_type="both", required=True),
        
    #     Field("seiten_pro_stunde", "number", "Seiten/h", chart_type="line",
    #           hidden=True, calculator=calc_seiten_pro_stunde),
        
    #     Field("unterbrechungen_anzahl", "number", chart_type="both", required=False),
    #     Field("konzentration_wert", "number", "%", chart_type="line", required=False),
        
    #     Field("medium", "enum", values=["buch", "ebook", "artikel", "comic"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Lernen": [
    #     Field("dauer_min", "number", "min", chart_type="line", required=True),
    #     Field("erfolg_wert", "number", "%", chart_type="line", required=True),
        
    #     Field("unterbrechungen_anzahl", "number", chart_type="both", required=False),
    #     Field("konzentration_wert", "number", "%", chart_type="line", required=False),
        
    #     Field("lernform", "enum", values=["video", "buch", "üben", "wiederholung", "gruppe"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Schlaf": [
    #     Field("dauer_stunden", "number", "h", chart_type="line", required=True),
    #     Field("schlafqualitaet", "number", "%", chart_type="line", required=True),
    #     Field("tiefschlaf_prozent", "number", "%", chart_type="line", required=False),
    #     Field("einschlafdauer_min", "number", "min", chart_type="both", required=False),
    #     Field("aufwach_anzahl", "number", chart_type="both", required=False),
    #     Field("ruhequalitaet", "number", "%", chart_type="line", required=False),
    # ],

    # "Bildschirmzeit": [
    #     Field("dauer_min", "number", "min", chart_type="line", required=True),
        
    #     Field("geraet_typ", "enum", values=["handy", "laptop", "tablet", "tv", "monitor"], 
    #           chart_type="enum_bar", required=False),
    #     Field("hauptnutzung", "enum", values=["arbeit", "social-media", "unterhaltung", "gaming", "lesen"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Wasser": [
    #     Field("menge_ml", "number", "ml", chart_type="line", required=True),
        
    #     Field("quelle", "enum", values=["leitungswasser", "flasche", "sprudel", "infusedwater"], 
    #           chart_type="enum_bar", required=False),
    #     Field("temperatur", "enum", values=["kalt", "zimmertemperatur", "warm", "heiß"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Alkohol": [
    #     Field("menge_ml", "number", "ml", chart_type="line", required=True),
    #     Field("alkohol_einheiten", "number", "Einheiten", chart_type="line", required=False),
        
    #     Field("getraenk_typ", "enum", values=["bier", "wein", "schnaps", "cocktail", "sonstige"], 
    #           chart_type="enum_bar", required=False),
    #     Field("anlass", "enum", values=["feier", "stress", "sozial", "freizeit", "besonderes"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Rauchen": [
    #     Field("anzahl_pro_tag", "number", chart_type="line", required=True),
    #     Field("abstand_min", "number", "min", chart_type="both", required=False),
    #     Field("verlangens_intensitaet", "number", "%", chart_type="line", required=False),
        
    #     Field("produkt_typ", "enum", values=["zigarette", "zigarre", "pfeife", "vape"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Stimmung": [
    #     Field("stimmung_wert", "number", "(1-10)", chart_type="line", required=True),        
    #     Field("hauptgefuehl", "enum", values=["glücklich", "traurig", "neutral", "gestresst", "vergnügt"], 
    #           chart_type="enum_bar", required=False),
    #     Field("ausloeser", "enum", values=["erfolg", "freunde", "natur", "hobby", "stress", "unbekannt"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Stress": [
    #     Field("stress_wert", "number", "(1-10)", chart_type="line", required=True),       
    #     Field("physisches_unbehagen", "number", "%", chart_type="line", required=False),
    #     Field("hauptursache", "enum", values=["arbeit", "privat", "gesundheit", "finanzen", "beziehung"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Energielevel": [
    #     Field("energie_wert", "number", "(1-10)", chart_type="line", required=True),       
    #     Field("koerperliche_energie", "number", "%", chart_type="line", required=False),
    #     Field("mentale_energie", "number", "%", chart_type="line", required=False),
    #     Field("tageszeit", "enum", values=["morgens", "mittags", "nachmittags", "abends", "nacht"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Motivation": [
    #     Field("motivation_wert", "number", "(1-10)", chart_type="line", required=True),        
    #     Field("selbstvertrauen", "number", "%", chart_type="line", required=False),
    #     Field("bezogen_auf", "enum", values=["sport", "lernen", "arbeit", "kreativität", "allgemein"], 
    #           chart_type="enum_bar", required=False),
    #     Field("hindernis", "enum", values=["müdigkeit", "stress", "ablenkung", "zweifel", "keine"], 
    #           chart_type="enum_bar", required=False),
    # ],

    # "Events": [
    #     Field("ort_typ", "enum", values=["kino", "oper", "restaurant", "kneipenabend", "konzert", 
    #                                       "theater", "museum", "park", "strand", "sport_event", 
    #                                       "freunde_treffen", "festival", "hochzeit", "geburtstag", "sonstige"],
    #           chart_type="enum_bar", required=True),
    #     Field("kosten", "number", "€", chart_type="bar", required=False),
    #     Field("begleitung_anzahl", "number", chart_type="bar", required=False),
    #     Field("begleitung_typ", "enum", values=["alleine", "partner", "familie", "freunde", "freunde+partner", "gruppe"],
    #           chart_type="enum_bar", required=False),
    #     Field("bewertung", "number", "(1-10)", chart_type="line", required=False),
    #     Field("notizen", "text", chart_type="none", required=False),
    # ],
}

COMPARISON_FEATURES: dict[str, List[str]] = {
    ActivityType.JOGGING.value: ["weather_type"],
    "Radfahren": ["strecke_typ", "intensitaet"],
    "Spazieren": ["strecke_typ", "intensitaet"],
    "Schwimmen": ["schwimmstil", "intensitaet"],
    "Workout": ["trainingsart", "intensitaet"],
    "Lesen": ["medium"],
    "Lernen": ["lernform"],
    "Wasser": ["quelle", "temperatur"],
    "Alkohol": ["getraenk_typ", "anlass"],
    "Rauchen": ["produkt_typ"],
    "Stimmung": ["hauptgefuehl", "ausloeser"],
    "Stress": ["hauptursache"],
    "Energielevel": ["tageszeit"],
    "Motivation": ["bezogen_auf", "hindernis"],
    "Events": ["ort_typ", "begleitung_typ"],
}

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
        return [FIELD_DEFINITIONS[key].to_dict() if hasattr(FIELD_DEFINITIONS[key], 'to_dict')
                else {
                    "key": FIELD_DEFINITIONS[key].key,
                    "label": FIELD_DEFINITIONS[key].label,
                    "field_type": FIELD_DEFINITIONS[key].field_type.value,
                    "chart_type": FIELD_DEFINITIONS[key].chart_type.value,
                    "required": FIELD_DEFINITIONS[key].required,
                    "hidden": FIELD_DEFINITIONS[key].hidden,
                    "unit": FIELD_DEFINITIONS[key].unit,
                    "options": FIELD_DEFINITIONS[key].options,
                }
                for key in field_keys if key in FIELD_DEFINITIONS]
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