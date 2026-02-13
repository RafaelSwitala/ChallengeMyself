from enum import Enum


class MovementIntensityEnum(str, Enum):
    """Intensität von Bewegungsaktivitäten"""
    GEMÜTLICH = "Gemütlich"
    MITTEL = "Mittel"
    STARK = "Stark"
    EXTREM = "Extrem"


class RouteTypeEnum(str, Enum):
    """Art der Laufstrecke"""
    MIX = "Mix"
    STADT = "Stadt"
    STRASSE = "Straße"
    FELDWEG = "Feldweg"
    WALDWEG = "Waldweg"
    PARK = "Park"
    NATUR = "Natur"
    BERG = "Berg"


class WeatherEnum(str, Enum):
    """Wetterbedingungen"""
    SONNIG = "Sonnig"
    BEWÖLKT = "Bewölkt"
    REGNERISCH = "Regnerisch"
    SCHNEE = "Schnee"
    STURM = "Sturm"
    NEBEL = "Nebel"
    HITZE = "Hitze"


class SwimmingStyleEnum(str, Enum):
    """Schwimmstile"""
    MIX = "Mix"
    KRAUL = "Kraul"
    BRUST = "Brust"
    RÜCKEN = "Rücken"
    DELFIN = "Delfin"
    TECHNIKTRAINING = "Techniktraining"


class WorkoutTypesEnum(str, Enum):
    """Arten von Trainingseinheiten"""
    MIX = "Mix"
    KRAFTTRAINING = "Krafttraining"
    AUSDAUER = "Ausdauer"
    FLEXIBILITÄT = "Flexibilität"
    MOBILITY = "Mobility"
    HIIT = "HIIT"
    CORE = "Core"


class ReadMediumTypeEnum(str, Enum):
    """Medien zum Lesen"""
    BUCH = "Buch"
    E_BOOK = "E-Book"
    ARTIKEL = "Artikel"
    COMIC = "Comic"
    ZEITUNG = "Zeitung"
    BLOG = "Blog"


class WriteMediumTypeEnum(str, Enum):
    """Medien zum Schreiben"""
    BUCH = "Buch"
    HAUSARBEIT = "Hausarbeit"
    AUFSATZ = "Aufsatz"
    NOTIZEN = "Notizen"
    TAGEBUCH = "Tagebuch"
    KREATIV = "Kreativ"
    BERUFLICH = "Beruflich"


class LearningFormatEnum(str, Enum):
    """Lernformate"""
    MIX = "Mix"
    VIDEO = "Video"
    BUCH = "Buch"
    RECHERCHE_ÜBUNG = "Rescherche Übung"
    WIEDERHOLUNG = "Wiederholung"
    GRUPPE = "Gruppe"
    KURS = "Kurs"
    PODCAST = "Podcast"


class DeviceTypeEnum(str, Enum):
    """Gerätetypen"""
    HANDY = "Handy"
    LAPTOP = "Laptop"
    TABLET = "Tablet"
    FERNSEHER = "Fernseher"
    MONITOR = "Monitor"


class DeviceMainUseEnum(str, Enum):
    """Hauptnutzung von Geräten"""
    ARBEIT = "Arbeit"
    SOCIAL_MEDIA = "Social-Media"
    UNTERHALTUNG = "Unterhaltung"
    SPIELE = "Spiele"
    CHATS = "Chats"
    ANRUFE = "Anrufe"
    LESEN = "Lesen"


class WaterSourceEnum(str, Enum):
    """Wasserquellen"""
    LEITUNGSWASSER = "Leitungswasser"
    SPRUDELWASSER = "Sprudelwasser"


class WaterTemperatureEnum(str, Enum):
    """Wassertemperatur"""
    KALT = "Kalt"
    ZIMMERTEMPERATUR = "Zimmertemperatur"
    WARM = "Warm"


class DrinkTemperatureEnum(str, Enum):
    """Temperatur von Getränken"""
    KALT = "Kalt"
    ZIMMERTEMPERATUR = "Zimmertemperatur"
    WARM = "Warm"
    HEISS = "Heiß"


class DrinkTypeEnum(str, Enum):
    """Arten von Getränken"""
    WASSER = "Wasser"
    KAFFE = "Kaffe"
    TEE = "Tee"
    SAFT = "Saft"
    LIMO = "Limo"
    MILCH = "Milch"
    ENERGYDRINK = "Energydrink"
    ALKOHOL = "Alkohol"


class AlcoholTypeEnum(str, Enum):
    """Arten von alkoholischen Getränken"""
    BIER = "Bier"
    WEIN = "Wein"
    SEKT = "Sekt"
    COCKTAIL = "Cocktail"
    LONGDRINK = "Longdrink"
    SCHNAPS = "Schnaps"


class OccasionTypeEnum(str, Enum):
    """Anlässe"""
    ALLTAG = "Alltag"
    FEIER = "Feier"
    SOZIAL = "Sozial"
    FREIZEIT = "Freizeit"
    STRESS = "Stress"
    BESONDERES = "Besonderes"


class SmokeProductEnum(str, Enum):
    """Raucherprodukte"""
    ZIGARETTE = "Zigarette"
    ZIGARRE = "Zigarre"
    PFEIFE = "Pfeife"
    VAPE = "Vape"


class MainMoodEnum(str, Enum):
    """Hauptgefühle/Stimmungen"""
    ARBEIT = "Arbeit"
    PRIVAT = "Privat"
    GESUNDHEIT = "Gesundheit"
    FINANZEN = "Finanzen"
    BEZIEHUNG = "Beziehung"


class TriggerEnum(str, Enum):
    """Auslöser für Aktivitäten"""
    UNBEKANNT = "Unbekannt"
    ERFOLG = "Erfolg"
    FREUNDE = "Freunde"
    NATUR = "Natur"
    HOBBY = "Hobby"
    STRESS = "Stress"
    LANGEWEILE = "Langeweile"
    MÜDIGKEIT = "Müdigkeit"


class TimeOfDayEnum(str, Enum):
    """Tageszeiten"""
    MORGENS = "Morgens"
    MITTAGS = "Mittags"
    NACHMITTAGS = "Nachmittags"
    ABENDS = "Abends"
    NACHTS = "Nachts"


class ObstacleEnum(str, Enum):
    """Hindernisse"""
    UNBEKANNT = "Unbekannt"
    MÜDIGKEIT = "Müdigkeit"
    ABLENKUNG = "Ablenkung"
    STRESS = "Stress"
    ZWEIFEL = "Zweifel"
    KEINE = "Keine"


class MotivationReferenceEnum(str, Enum):
    """Motivationsbezüge"""
    ALLGEMEIN = "Allgemein"
    SPORT = "Sport"
    LERNEN = "Lernen"
    ARBEIT = "Arbeit"
    KREATIVITÄT = "Kreativität"


class LocationTypeEnum(str, Enum):
    """Ortstypen"""
    ZUHAUSE = "Zuhause"
    ARBEIT = "Arbeit"
    DRAUSSEN = "Draußen"
    SCHULE = "Schule"
    UNI = "Uni"
    GYM = "Gym"


class SocialContextEnum(str, Enum):
    """Sozialer Kontext"""
    ALLEINE = "Alleine"
    FREUNDE = "Freunde"
    FAMILIE = "Familie"
    PARTNER = "Partner"
    KOLLEGEN = "Kollegen"
    GRUPPE = "Gruppe"
    FREMDE = "Fremde"


class HouseholdTaskEnum(str, Enum):
    """Haushaltsaufgaben"""
    PUTZEN = "Putzen"
    AUFRÄUMEN = "Aufräumen"
    WÄSCHE = "Wäsche"
    GESCHIRR = "Geschirr"
    KOCHEN = "Kochen"
    EINKAUFEN = "Einkaufen"
    ORGANISATION = "Organisation"
    REPARATUR = "Reparatur"
    GARTEN = "Garten"
    BÜRO = "Büro"


class HouseAreaEnum(str, Enum):
    """Wohnungsbereiche"""
    KÜCHE = "Küche"
    BAD = "Bad"
    SCHLAFZIMMER = "Schlafzimmer"
    WOHNZIMMER = "Wohnzimmer"
    KELLER = "Keller"
    ALLGEMEIN = "Allgemein"


class StatusEnum(str, Enum):
    """Status von Aufgaben"""
    BEGONNEN = "Begonnen"
    TEILWEISE = "Teilweise"
    ERLEDIGT = "Erledigt"


class MealTypeEnum(str, Enum):
    """Mahlzeittypen"""
    FRÜHSTÜCK = "Frühstück"
    MITTAGESSEN = "Mittagessen"
    ABENDESSEN = "Abendessen"
    SNACK = "Snack"


class FoodQualityEnum(str, Enum):
    """Qualität von Mahlzeiten"""
    SEHR_UNGESUND = "Sehr Ungesund"
    UNGESUND = "Ungesund"
    NEUTRAL = "Neutral"
    GESUND = "Gesund"
    SEHR_GESUND = "Sehr Gesund"


class PortionSizeEnum(str, Enum):
    """Portionsgrößen"""
    KLEIN = "Klein"
    NORMAL = "Normal"
    GROSS = "Groß"


class EatingContextEnum(str, Enum):
    """Kontext von Mahlzeiten"""
    ZUHAUSE = "Zuhause"
    ARBEIT = "Arbeit"
    RESTAURANT = "Restaurant"
    UNTERWEGS = "Unterwegs"


class LanguageTrainingTypeEnum(str, Enum):
    """Arten von Sprachtraining"""
    VOKABELN = "Vokabeln"
    GRAMMATIK = "Grammatik"
    HÖREN = "Hören"
    SPRECHEN = "Sprechen"
    SCHREIBEN = "Schreiben"
    LESEN = "Lesen"
    AUSSPRACHE = "Aussprache"
