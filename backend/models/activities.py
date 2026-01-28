from dataclasses import dataclass
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

@dataclass
class Field:
    name: str
    type: str
    unit: Optional[str] = None
    values: Optional[List[str]] = None
    chart_type: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Wandelt das Field-Objekt in ein JSON-kompatibles dict um
        (für API / Frontend)
        """
        data = {
            "name": self.name,
            "type": self.type,
        }
        if self.unit is not None:
            data["unit"] = self.unit
        if self.values is not None:
            data["values"] = self.values
        if self.chart_type is not None:
            data["chart_type"] = self.chart_type
        return data


ACTIVITIES: dict[str, list[Field]] = {

    # Bewegung & Sport
    "Laufen": [
        Field("distanz_km", "number", "km", chart_type="line"),
        Field("dauer_min", "number", "min", chart_type="line"),
        Field("pausen_anzahl", "number", chart_type="line"),
        Field("pausen_dauer_min", "number", "min", chart_type="line"),
        Field("intensitaet", "enum", values=["gemuetlich", "mittel", "stark"]),
        Field("strecke_typ", "enum", values=["mix", "asphalt", "feldweg", "waldweg", "schotter", "park"]),
    ],

    "Radfahren": [
        Field("distanz_km", "number", "km", chart_type="line"),
        Field("dauer_min", "number", "min", chart_type="line"),
        Field("pausen_anzahl", "number", chart_type="bar"),
        Field("pausen_dauer_min", "number", "min", chart_type="line"),
        Field("intensitaet", "enum", values=["gemuetlich", "mittel", "stark"]),
        Field("strecke_typ", "enum", values=["mix", "asphalt", "feldweg", "waldweg", "schotter", "park"]),
    ],

    "Spazieren": [
        Field("distanz_km", "number", "km"),
        Field("dauer_min", "number", "min"),
        Field("schritte_anzahl", "number"),
        Field("intensitaet", "enum", values=["gemuetlich", "mittel", "stark"]),
        Field("strecke_typ", "enum", values=["mix", "asphalt", "feldweg", "waldweg", "schotter", "park"]),
    ],

    "Schwimmen": [
        Field("distanz_m", "number", "m"),
        Field("dauer_min", "number", "min"),
        Field("pausen_anzahl", "number"),
        Field("beckenlaenge_m", "number", "m"),
        Field("schwimmstil", "text"),
    ],

    "Workout": [
        Field("dauer_min", "number", "min", chart_type="line"),
        Field("uebungen_anzahl", "number", chart_type="line"),
        Field("uebung_name", "text"),
        Field("intensitaet", "enum", values=["gemuetlich", "mittel", "stark"]),
        Field("trainingsart", "text"),
    ],

    "Liegestütze": [
        Field("wiederholungen_anzahl", "number"),
        Field("sets_anzahl", "number"),
        Field("set_definition", "text"),
        Field("saubere_wiederholungen_anzahl", "number"),
        Field("intensitaet", "enum", values=["gemuetlich", "mittel", "stark"]),
    ],

    # Lernen & Fokus
    "Lesen": [
        Field("dauer_min", "number", "min"),
        Field("unterbrechungen_anzahl", "number"),
        Field("seiten_anzahl", "number"),
        Field("medium", "text"),
    ],

    "Lernen": [
        Field("dauer_min", "number", "min"),
        Field("unterbrechungen_anzahl", "number"),
        Field("thema", "text"),
        Field("lernform", "text"),
    ],

    # Schlaf & Regeneration
    "Schlaf": [
        Field("dauer_stunden", "number", "h"),
        Field("dauer_min", "number", "min"),
        Field("schlafqualitaet", "number"),
        Field("einschlafdauer_min", "number", "min"),
        Field("aufwach_anzahl", "number"),
    ],

    # Alltag & Medien
    "Bildschirmzeit": [
        Field("dauer_min", "number", "min", chart_type="line"),
        Field("geraet_typ", "text"),
        Field("hauptnutzung", "text"),
    ],

    # Konsum
    "Wasser": [
        Field("menge_ml", "number", "ml"),
        Field("quelle", "text"),
        Field("temperatur", "enum", values=["kalt", "zimmertemperatur", "warm", "heiß"]),
    ],

    "Alkohol": [
        Field("menge_ml", "number", "ml"),
        Field("getraenk_typ", "text"),
        Field("alkohol_prozent", "number"),
        Field("anlass", "text"),
    ],

    "Rauchen": [
        Field("anzahl_pro_tag", "number"),
        Field("abstand_min", "number", "min"),
        Field("produkt_typ", "text"),
        Field("verlangen_wert", "number"),
    ],

    # Mentales & Wohlbefinden
    "Stimmung": [
        Field("wert", "number"),
        Field("hauptgefuehl", "text"),
        Field("ausloeser", "text"),
    ],

    "Stress": [
        Field("wert", "number"),
        Field("hauptursache", "text"),
        Field("koerperliche_symptome", "text"),
    ],

    "Energielevel": [
        Field("wert", "number"),
        Field("tageszeit", "text"),
        Field("koerperliches_gefuehl", "text"),
    ],

    "Motivation": [
        Field("wert", "number"),
        Field("bezogen_auf", "text"),
        Field("hindernis", "text"),
    ],
}


def get_activity_names() -> list[str]:
    try:
        return list(ACTIVITIES.keys())
    except Exception:
        logger.exception("Failed to get activity names")
        return []


def get_fields(activity: str) -> list[dict]:
    try:
        fields = ACTIVITIES.get(activity, [])
        return [f.to_dict() for f in fields]
    except Exception:
        logger.exception("Failed to get fields for activity %s", activity)
        return []