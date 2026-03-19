"""
Zentrale Enum-Definitionen für das ChallengeMyself System
"""

from enum import Enum


class ActivityType(Enum):
    """40+ Aktivitätstypen"""
    JOGGING = "Joggen"
    CYCLING = "Radfahren"
    WALKING = "Spazieren"
    SWIMMING = "Schwimmen"
    WORKOUT = "Workout"
    SLEEPING = "Schlaf"
    READING = "Lesen"
    LEARNING = "Lernen"
    EATING = "Ernährung"
    COFFEE_CONSUMPTION = "Koffeinkonsum"
    ALCOHOL_CONSUMPTION = "Alkoholkonsum"
    SMOKING = "Rauchverhalten"
    MOOD = "Stimmung"
    STRESS = "Stress"
    ENERGY = "Energie"
    MOTIVATION = "Motivation"
    WATER_CONSUMPTION = "Wasserkonsum"
    DRINK_CONSUMPTION = "Getränkekonsum"
    LANGUAGE_TRAINING = "Sprachtraining"
    WRITING = "Schreiben"
    SCREEN_TIME = "Bildschirmzeit"
    SOCIAL_INTERACTION = "Soziale Interaktion"
    HOUSEHOLD = "Haushalt"
    EXPENSES = "Ausgaben"
    MEDITATION = "Meditation"
    CREATIVITY = "Kreativitaet"
    ART = "Kunst"
    MUSIC = "Musikpraxis"
    NATURE = "Natur"
    PRODUCTIVITY = "Produktivitaet"
    SAVINGS = "Sparen"
    WANDERING = "Wandern"
    YOGA = "Yoga"
    FAMILY_TIME = "Familienzeit"
    RELATIONSHIP = "Beziehungszeit (Quality Time)"
    HABIT_BREAKING = "Gewohnheitsbruch (Rückfälle)"
    DRUG_USE = "Drogenkonsum"


class GoalType(Enum):
    """12 Zieltypen A-L"""
    MORE_THAN = "a"           # Mehr als X
    LESS_THAN = "b"           # Weniger als X
    AVOID = "c"               # Ganz vermeiden
    FREQUENCY_EXACT = "d"     # Genau X-mal pro Periode
    FREQUENCY_MIN = "e"       # Mindestens X-mal
    FREQUENCY_MAX = "f"       # Maximal X-mal
    STREAK = "g"              # X Tage in Folge
    INCREASE_DAILY = "h"      # Täglich X mehr bis Y
    DECREASE_DAILY = "i"      # Täglich X weniger bis Y
    AVERAGE_ABOVE = "j"       # Durchschnitt über X
    AVERAGE_BELOW = "k"       # Durchschnitt unter X
    CONDITIONAL = "l"         # X erreichen unter Bedingung Y


class GoalPeriod(Enum):
    """Zeiträume für Goals"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    DATE_RANGE = "date_range"


class FieldType(Enum):
    """Feldtypen"""
    NUMBER = "number"
    INTEGER = "integer"
    ENUM = "enum"
    TEXT = "text"
    BOOLEAN = "boolean"


class ChartType(Enum):
    """Diagrammtypen"""
    LINE = "line"
    BAR = "bar"
    BOTH = "both"
    ENUM_BAR = "enum_bar"
    NONE = "none"
    VALUE = "value"


class MovementIntensity(Enum):
    """Intensitätsstufen"""
    VERY_LIGHT = "sehr leicht"
    LIGHT = "leicht"
    MODERATE = "mittel"
    INTENSE = "intensiv"
    VERY_INTENSE = "sehr intensiv"


class WeatherType(Enum):
    """Wettertypen"""
    SUNNY = "sonnig"
    CLOUDY = "bewölkt"
    RAINY = "regnerisch"
    SNOWY = "schneereich"
    WINDY = "windig"
    FOGGY = "neblig"


class RouteType(Enum):
    """Streckentypen"""
    ASPHALT = "asphalt"
    GRAVEL = "schotter"
    TRAIL = "pfad"
    FOREST = "wald"
    MIXED = "mix"


class SwimmingStyle(Enum):
    """Schwimmstile"""
    FREESTYLE = "freistil"
    BACKSTROKE = "rückenschwimmen"
    BREASTSTROKE = "brustschwimmen"
    BUTTERFLY = "schmetterling"
    MIXED = "gemischt"


class WorkoutType(Enum):
    """Trainingsarten"""
    STRENGTH = "kraft"
    CARDIO = "ausdauer"
    FLEXIBILITY = "flexibilität"
    MIXED = "gemischt"
    YOGA = "yoga"
    PILATES = "pilates"


class ReadingMedium(Enum):
    """Lesemedien"""
    PHYSICAL_BOOK = "papierbuch"
    EBOOK = "ebook"
    AUDIOBOOK = "hörbuch"
    ARTICLE = "artikel"


class WritingMedium(Enum):
    """Schreibmedien"""
    PHYSICAL = "papier"
    DIGITAL = "digital"
    HANDWRITING = "handschrift"


class LearningFormat(Enum):
    """Lernformate"""
    VIDEO = "video"
    BOOK = "buch"
    INTERACTIVE = "interaktiv"
    PRACTICAL = "praktisch"
    GROUP = "gruppe"


class EnergyLevel(Enum):
    """Energielevel"""
    VERY_LOW = "sehr niedrig"
    LOW = "niedrig"
    MODERATE = "mittel"
    HIGH = "hoch"
    VERY_HIGH = "sehr hoch"


class MoodType(Enum):
    """Stimmungstypen"""
    VERY_SAD = "sehr traurig"
    SAD = "traurig"
    NEUTRAL = "neutral"
    HAPPY = "glücklich"
    VERY_HAPPY = "sehr glücklich"


class TimeOfDay(Enum):
    """Tageszeiten"""
    MORNING = "morgen"
    AFTERNOON = "mittag"
    EVENING = "abend"
    NIGHT = "nacht"


class DeviceType(Enum):
    """Gerätetypen"""
    PHONE = "telefon"
    TABLET = "tablet"
    LAPTOP = "laptop"
    DESKTOP = "desktop"
    SMART_WATCH = "smartwatch"


class LocationType(Enum):
    """Ort-Typen"""
    HOME = "zuhause"
    WORK = "arbeit"
    OUTDOOR = "draußen"
    GYM = "fitnessstudio"
    PARK = "park"
    PUBLIC = "öffentlich"


class SocialContext(Enum):
    """Sozialer Kontext"""
    ALONE = "allein"
    WITH_FRIEND = "mit freund"
    WITH_FAMILY = "mit familie"
    WITH_GROUP = "mit gruppe"
    WITH_PARTNER = "mit partner"


class MealType(Enum):
    """Mahlzeittypen"""
    BREAKFAST = "frühstück"
    LUNCH = "mittagessen"
    DINNER = "abendessen"
    SNACK = "snack"
    DESSERT = "dessert"


class FoodQuality(Enum):
    """Lebensmittelqualität"""
    VERY_UNHEALTHY = "sehr ungesund"
    UNHEALTHY = "ungesund"
    NEUTRAL = "neutral"
    HEALTHY = "gesund"
    VERY_HEALTHY = "sehr gesund"


class PortionSize(Enum):
    """Portionsgröße"""
    VERY_SMALL = "sehr klein"
    SMALL = "klein"
    MEDIUM = "mittel"
    LARGE = "groß"
    VERY_LARGE = "sehr groß"


class DrinkType(Enum):
    """Getränketypen"""
    WATER = "wasser"
    COFFEE = "kaffee"
    TEA = "tee"
    SODA = "limonade"
    JUICE = "saft"
    MILK = "milch"
    ALCOHOL = "alkohol"
    OTHER = "sonstig"


class AlcoholType(Enum):
    """Alkoholtypen"""
    BEER = "bier"
    WINE = "wein"
    SPIRITS = "spirituosen"
    COCKTAIL = "cocktail"
    CIDER = "apfelwein"


class OccasionType(Enum):
    """Anlass"""
    CELEBRATION = "feier"
    SOCIAL = "gesellig"
    RELAXATION = "entspannung"
    STRESS_RELIEF = "stressabbau"
    OTHER = "sonstig"


class MainMood(Enum):
    """Hauptgefühl"""
    JOY = "freude"
    SADNESS = "traurigkeit"
    ANGER = "wut"
    FEAR = "angst"
    SURPRISE = "überraschung"
    DISGUST = "ekel"
    NEUTRAL = "neutral"


class TriggerType(Enum):
    """Auslöser"""
    WORK = "arbeit"
    RELATIONSHIP = "beziehung"
    HEALTH = "gesundheit"
    MONEY = "geld"
    FAMILY = "familie"
    SOCIAL = "soziales"
    OTHER = "sonstig"


class ObstacleType(Enum):
    """Hindernis"""
    TIME = "zeit"
    MOTIVATION = "motivation"
    ENERGY = "energie"
    MONEY = "geld"
    HEALTH = "gesundheit"
    WEATHER = "wetter"
    OTHER = "sonstig"


class HouseArea(Enum):
    """Wohnungsbereich/Haushalt"""
    KITCHEN = "küche"
    LIVING_ROOM = "wohnzimmer"
    BEDROOM = "schlafzimmer"
    BATHROOM = "badezimmer"
    LAUNDRY = "wäsche"
    CLEANING = "putzen"


class LanguageTrainingType(Enum):
    """Sprachtraining Typ"""
    SPEAKING = "sprechen"
    LISTENING = "hören"
    READING = "lesen"
    WRITING = "schreiben"
    GRAMMAR = "grammatik"
    VOCABULARY = "vokabeln"


class StatusType(Enum):
    """Status"""
    PLANNED = "geplant"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "pausiert"
    CANCELLED = "abgebrochen"
