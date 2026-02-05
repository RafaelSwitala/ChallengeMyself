from dataclasses import dataclass
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

@dataclass
class Field:
    """
    Represents a data field in a challenge.
    
    Attributes:
        name: Field identifier (e.g., 'distanz_km')
        type: Data type ('number', 'enum', 'text')
        unit: Optional unit for display (e.g., 'km', 'min', '%')
        values: For enum fields, list of allowed values
        chart_type: Which charts support this field
                   - 'line': only line charts
                   - 'bar': only bar charts
                   - 'both': line and bar
                   - 'none': category field (not for charts)
    """
    name: str
    type: str
    unit: Optional[str] = None
    values: Optional[List[str]] = None
    chart_type: str = "both"  # 'line', 'bar', 'both', 'none'

    def to_dict(self) -> dict:
        """Converts Field to JSON-compatible dict."""
        data = {
            "name": self.name,
            "type": self.type,
            "chart_type": self.chart_type,
        }
        if self.unit is not None:
            data["unit"] = self.unit
        if self.values is not None:
            data["values"] = self.values
        return data


# ============================================================================
# ACTIVITIES DEFINITION - Alle Aktivitäten mit logischen Feldkategorisierungen
# ============================================================================

ACTIVITIES: dict[str, list[Field]] = {

    # ========================================================================
    # SPORT & BEWEGUNG
    # ========================================================================
    "Laufen": [
        # Numerische Messwerte (gut für Linien)
        Field("distanz_km", "number", "km", chart_type="line"),
        Field("dauer_min", "number", "min", chart_type="line"),
        Field("geschwindigkeit_kmh", "number", "km/h", chart_type="line"),
        Field("kalorienverbrauch", "number", "kcal", chart_type="line"),
        
        # Pausen (kann bar oder line sein)
        Field("pausen_anzahl", "number", chart_type="both"),
        Field("pausen_dauer_min", "number", "min", chart_type="both"),
        
        # Kategorische Felder (nur für Filter/Vergleich, nicht direkt für Chart)
        Field("intensitaet", "enum", values=["gemütlich", "mittel", "stark"], chart_type="none"),
        Field("strecke_typ", "enum", values=["mix", "asphalt", "feldweg", "waldweg", "schotter", "park"], chart_type="none"),
        Field("wetter", "enum", values=["sonnig", "bewölkt", "regnerisch", "schnee"], chart_type="none"),
    ],

    "Radfahren": [
        Field("distanz_km", "number", "km", chart_type="line"),
        Field("dauer_min", "number", "min", chart_type="line"),
        Field("geschwindigkeit_kmh", "number", "km/h", chart_type="line"),
        Field("kalorienverbrauch", "number", "kcal", chart_type="line"),
        Field("hoehenmeter", "number", "m", chart_type="line"),
        
        Field("pausen_anzahl", "number", chart_type="both"),
        Field("pausen_dauer_min", "number", "min", chart_type="both"),
        
        Field("intensitaet", "enum", values=["gemütlich", "mittel", "stark"], chart_type="none"),
        Field("strecke_typ", "enum", values=["mix", "asphalt", "feldweg", "waldweg", "berg"], chart_type="none"),
    ],

    "Spazieren": [
        Field("distanz_km", "number", "km", chart_type="line"),
        Field("dauer_min", "number", "min", chart_type="line"),
        Field("schritte_anzahl", "number", chart_type="line"),
        
        Field("intensitaet", "enum", values=["gemütlich", "mittel", "flott"], chart_type="none"),
        Field("strecke_typ", "enum", values=["mix", "stadt", "natur", "park"], chart_type="none"),
    ],

    "Schwimmen": [
        Field("distanz_m", "number", "m", chart_type="line"),
        Field("dauer_min", "number", "min", chart_type="line"),
        Field("kalorienverbrauch", "number", "kcal", chart_type="line"),
        
        Field("pausen_anzahl", "number", chart_type="both"),
        Field("beckenlaenge_m", "number", "m", chart_type="line"),
        
        Field("schwimmstil", "enum", values=["kraul", "brust", "rücken", "delphin", "mix"], chart_type="none"),
        Field("intensitaet", "enum", values=["gemütlich", "mittel", "stark"], chart_type="none"),
    ],

    "Workout": [
        Field("dauer_min", "number", "min", chart_type="line"),
        Field("uebungen_anzahl", "number", chart_type="both"),
        Field("kalorienverbrauch", "number", "kcal", chart_type="line"),
        
        Field("trainingsart", "enum", values=["krafttraining", "ausdauer", "flexibilität", "mix"], chart_type="none"),
        Field("intensitaet", "enum", values=["gemütlich", "mittel", "stark"], chart_type="none"),
    ],

    "Liegestütze": [
        Field("wiederholungen_anzahl", "number", chart_type="both"),
        Field("sets_anzahl", "number", chart_type="both"),
        Field("saubere_wiederholungen_anzahl", "number", chart_type="both"),
        Field("durchschnitt_pro_set", "number", chart_type="line"),
        
        Field("intensitaet", "enum", values=["gemütlich", "mittel", "stark"], chart_type="none"),
    ],

    # ========================================================================
    # LERNEN & FOKUS
    # ========================================================================
    "Lesen": [
        Field("dauer_min", "number", "min", chart_type="line"),
        Field("seiten_anzahl", "number", chart_type="both"),
        Field("seiten_pro_stunde", "number", chart_type="line"),
        
        Field("unterbrechungen_anzahl", "number", chart_type="both"),
        
        Field("medium", "enum", values=["buch", "ebook", "artikel", "comic"], chart_type="none"),
        Field("konzentration_wert", "number", "%", chart_type="line"),
    ],

    "Lernen": [
        Field("dauer_min", "number", "min", chart_type="line"),
        Field("unterbrechungen_anzahl", "number", chart_type="both"),
        
        Field("lernform", "enum", values=["video", "buch", "üben", "wiederholung", "gruppe"], chart_type="none"),
        Field("konzentration_wert", "number", "%", chart_type="line"),
        Field("erfolg_wert", "number", "%", chart_type="line"),
    ],

    # ========================================================================
    # SCHLAF & REGENERATION
    # ========================================================================
    "Schlaf": [
        Field("dauer_stunden", "number", "h", chart_type="line"),
        Field("schlafqualitaet", "number", "%", chart_type="line"),
        Field("tiefschlaf_prozent", "number", "%", chart_type="line"),
        Field("einschlafdauer_min", "number", "min", chart_type="both"),
        Field("aufwach_anzahl", "number", chart_type="both"),
        Field("ruhequalitaet", "number", "%", chart_type="line"),
    ],

    # ========================================================================
    # ALLTAG & MEDIEN
    # ========================================================================
    "Bildschirmzeit": [
        Field("dauer_min", "number", "min", chart_type="line"),
        
        Field("geraet_typ", "enum", values=["handy", "laptop", "tablet", "tv", "monitor"], chart_type="none"),
        Field("hauptnutzung", "enum", values=["arbeit", "social-media", "unterhaltung", "gaming", "lesen"], chart_type="none"),
    ],

    # ========================================================================
    # KONSUM & SUBSTANZEN
    # ========================================================================
    "Wasser": [
        Field("menge_ml", "number", "ml", chart_type="line"),
        
        Field("quelle", "enum", values=["leitungswasser", "flasche", "sprudel", "infusedwater"], chart_type="none"),
        Field("temperatur", "enum", values=["kalt", "zimmertemperatur", "warm", "heiß"], chart_type="none"),
    ],

    "Alkohol": [
        Field("menge_ml", "number", "ml", chart_type="line"),
        Field("alkohol_einheiten", "number", "Einheiten", chart_type="line"),
        
        Field("getraenk_typ", "enum", values=["bier", "wein", "schnaps", "cocktail", "sonstige"], chart_type="none"),
        Field("anlass", "enum", values=["feier", "stress", "sozial", "freizeit", "besonderes"], chart_type="none"),
    ],

    "Rauchen": [
        Field("anzahl_pro_tag", "number", chart_type="line"),
        Field("abstand_min", "number", "min", chart_type="both"),
        Field("verlangens_intensitaet", "number", "%", chart_type="line"),
        
        Field("produkt_typ", "enum", values=["zigarette", "zigarre", "pfeife", "vape"], chart_type="none"),
    ],

    # ========================================================================
    # MENTALES & WOHLBEFINDEN
    # ========================================================================
    "Stimmung": [
        Field("wert", "number", "%", chart_type="line"),
        
        Field("hauptgefuehl", "enum", values=["glücklich", "traurig", "neutral", "gestresst", "vergnügt"], chart_type="none"),
        Field("ausloeser", "enum", values=["erfolg", "freunde", "natur", "hobby", "stress", "unbekannt"], chart_type="none"),
    ],

    "Stress": [
        Field("wert", "number", "%", chart_type="line"),
        Field("physisches_unbehagen", "number", "%", chart_type="line"),
        
        Field("hauptursache", "enum", values=["arbeit", "privat", "gesundheit", "finanzen", "beziehung"], chart_type="none"),
    ],

    "Energielevel": [
        Field("wert", "number", "%", chart_type="line"),
        Field("koerperliche_energie", "number", "%", chart_type="line"),
        Field("mentale_energie", "number", "%", chart_type="line"),
        
        Field("tageszeit", "enum", values=["morgens", "mittags", "nachmittags", "abends", "nacht"], chart_type="none"),
    ],

    "Motivation": [
        Field("wert", "number", "%", chart_type="line"),
        Field("selbstvertrauen", "number", "%", chart_type="line"),
        
        Field("bezogen_auf", "enum", values=["sport", "lernen", "arbeit", "kreativität", "allgemein"], chart_type="none"),
        Field("hindernis", "enum", values=["müdigkeit", "stress", "ablenkung", "zweifel", "keine"], chart_type="none"),
    ],
}


# ============================================================================
# COMPARISON FEATURES - Automatische Vergleichsfeatures pro Activity
# ============================================================================

COMPARISON_FEATURES: dict[str, List[str]] = {
    "Laufen": ["strecke_typ", "intensitaet", "wetter"],
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
    "Motivation": ["bezogen_auf"],
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
        fields = ACTIVITIES.get(activity, [])
        return [f.to_dict() for f in fields]
    except Exception:
        logger.exception("Failed to get fields for activity %s", activity)
        return []


def get_numeric_fields(activity: str, chart_type: Optional[str] = None) -> list[str]:
    """
    Returns numeric field names for an activity.
    
    Args:
        activity: Activity name
        chart_type: Filter by chart_type ('line', 'bar', 'both', None=all)
    
    Returns:
        List of numeric field names suitable for charts
    """
    try:
        fields = ACTIVITIES.get(activity, [])
        numeric = [
            f.name for f in fields
            if f.type == "number"
            and f.chart_type != "none"
        ]
        
        if chart_type:
            numeric = [
                f.name for f in fields
                if f.type == "number"
                and (f.chart_type == chart_type or f.chart_type == "both")
                and f.chart_type != "none"
            ]
        
        return numeric
    except Exception:
        logger.exception(f"Failed to get numeric fields for {activity}")
        return []


def get_category_fields(activity: str) -> list[str]:
    """Returns enum/text field names (for filtering/grouping)."""
    try:
        fields = ACTIVITIES.get(activity, [])
        return [f.name for f in fields if f.type == "enum" and f.chart_type == "none"]
    except Exception:
        logger.exception(f"Failed to get category fields for {activity}")
        return []


def get_field_unit(activity: str, field_name: str) -> Optional[str]:
    """Returns the unit for a specific field."""
    try:
        fields = ACTIVITIES.get(activity, [])
        for f in fields:
            if f.name == field_name:
                return f.unit
        return None
    except Exception:
        logger.exception(f"Failed to get unit for {activity}.{field_name}")
        return None


def get_comparison_features(activity: str) -> List[str]:
    """Returns category fields suitable for comparisons."""
    return COMPARISON_FEATURES.get(activity, [])