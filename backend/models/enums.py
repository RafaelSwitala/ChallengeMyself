"""
Zentrale Enum-Definitionen für das ChallengeMyself System
"""

from enum import Enum


class ActivityType(Enum):
    """40+ Aktivitätstypen"""
    # ALCOHOL_CONSUMPTION = "Alkoholkonsum"
    # ---------- ANXIETY = "Angstlevel"
    # ART = "Kunst"
    # ---------- BUDGETING = "Budgetplanung"
    # CAFFEINE_CONSUMPTION = "Koffeinkonsum"
    # ---------- COMMUNITY_ENGAGEMENT = "Gemeinschaftsaktivität"
    # CREATIVITY = "Kreativitaet"
    # ---------- CULTURAL_EVENTS = "Kulturelle Veranstaltungen"
    # CYCLING = "Radfahren"
    # DRINK_CONSUMPTION = "Getränkekonsum"
    # DRUG_USE = "Drogenkonsum"
    # EATING = "Ernährung"
    # ENERGY = "Energie"
    # EXPENSES = "Ausgaben"
    # FAMILY_TIME = "Familienzeit"
    # GAMBLING = "Glücksspiel"
    # ---------- GRATITUDE = "Dankbarkeit"
    # HABIT_BREAKING = "Gewohnheitsbruch (Rückfälle)"
    # ----------- HABIT_TRACKING = "Gewohnheiten (aufbauen)"
    # ---------- HAPPINESS = "Glücksgefühl"
    # ---------- HEALTH_CHECK = "Gesundheitscheck"
    # HOUSEHOLD = "Haushalt"
    # ---------- IMMUNITY = "Immunsystem stärken"
    # ---------- INVESTING = "Investieren"
    JOGGING = "Joggen"
    # LANGUAGE_TRAINING = "Sprachtraining"
    # LEARNING = "Lernen"
    # MEDITATION = "Meditation"
    # ---------- MENTAL_EXERCISE = "Mentale Übungen"
    # ---------- MINDFULNESS = "Achtsamkeit"
    # MOOD = "Stimmung"
    # MOTIVATION = "Motivation"
    # MUSIC = "Musikpraxis"
    # NATURE = "Natur"
    # PRODUCTIVITY = "Produktivitaet"
    # READING = "Lesen"
    # ---------- REFLECTION = "Reflexion, Tagebuch"
    # RELATIONSHIP = "Beziehungszeit (Quality Time)"
    # SAVINGS = "Sparen"
    # SCREEN_TIME = "Bildschirmzeit"
    # ---------- SKILL_TRAINING = "Fertigkeitstraining"
    # SLEEPING = "Schlaf"
    # SMOKING = "Rauchverhalten"
    # ---------- SNACKING = "Snacks"
    # SOCIAL_INTERACTION = "Soziale Interaktion"
    # ---------- SPORTS = "Sportarten"
    # STRESS = "Stress"
    # SWIMMING = "Schwimmen"
    # ----------- TRAVELING = "Reisen"
    # ---------- VOLUNTEERING = "Freiwilligenarbeit"
    # WALKING = "Spazieren"
    # WANDERING = "Wandern"
    # WATER_CONSUMPTION = "Wasserkonsum"
    # ----------- WEATHER_EXPOSURE = "Sonnenlicht, Naturkontakt"
    # WORKOUT = "Workout"
    # WRITING = "Schreiben"
    # YOGA = "Yoga"


    
    
    
    
    


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
    DATE = "Date"


class ChartType(Enum):
    """Diagrammtypen"""
    LINE = "line"
    BAR = "bar"
    ENUM_BAR = "enum_bar"
    NONE = "none"
    VALUE = "value"


# --------------- ActivityTypeEnums
class AlcoholType(Enum):
    """Alkoholtypen"""
    BEER = "Bier"
    WINE = "Wein"
    SPARKLING_WINE = "Sekt"
    SPIRITS = "Spirituosen"
    LONGDRINK = "Longdrink"
    COCKTAIL = "Cocktail"
    CIDER = "Apfelwein"

class CunsumptionMethodType(Enum):
    SMOKE = "Rauchen"
    VAPING = "Vapen"
    DRINKING = "Trinken"
    EATING = "Essem"
    ORAL = "Tablette, Tropfen, Kapsel"
    SUBLINGUAL = "unter Zunge zergehen lassen"
    NASAL = "Sniffen"
    INHALATION = "Inhalation"
    INJEKTION = "Spritzen"
    TOPICAL = "Auf die Haut"
    PLUGGING = "Rektal"

class ConsumptionProductType(Enum):
    CIGARETTE = "Zigarette"
    CIGAR = "Zigarre"
    PIPE = "Pfeife"
    SHISHA = "Shisha"
    E_CIGARETTE = "E-Zigarette"
    VAPE = "Vape"

class DeviceMainUseType(Enum):
    MIX = "Mix"
    WORK = "Arbeit"
    FREETIME = "Freizeit"
    LEARNING = "Lernen"
    CREATIVITY = "Kreativität"
    PASTIME = "Zeitvertreib"
    DIVERSION = "Ablenkung"
    SOCIAL_MEDIA = "Soziale Medien"
    ENTERTAINMENT = "Unterhaltung"
    CHATS = "Chats"
    E_BOOK = "E-Book"
    VIDEOS = "Videos"
    CALLS = "Anrufe"
    GAMES = "Spiele"
    READING = "Lesen"
    WRITING = "Schreiben"

class DeviceType(Enum):
    MOBILE_PHONE = "Handy"
    LAPTOP = "Laptop"
    DESKTOP = "Desktop"
    TABLET = "Tablet"
    TELEVISION = "Fermseher"
    GAME_CONSOLE = "Spielkonsole"

class DrinkTemperature(Enum):
    COLD = "kalt"
    LUKEWARM = "lauwarm"
    WARM = "warm"
    HOT = "heiß"

class DrinkType(Enum):
    WATER = "Wasser"
    TEA = "Tee"
    COFFEE = "Kaffee"
    JUICE = "Saft"
    SMOOTHIE = "Smoothie"
    MILK = "Milch"
    LEMONADE = "Limonade"
    BEER = "Bier"
    WINE = "Wein"
    COCKTAIL = "Cocktail"
    ALCOHOL = "Alkohol"
    ENERGY_DRINK = "Energy-Drink"

class EatingContext(Enum):
    ALLONE = "Alleine"
    FRIENDS = "mit Freunden"
    FAMILY = "mit Familie"
    AWAY = "unterwegs"
    RESTAURANT = "Restaurant"
    WORK = "Auf der Arbeit"

class FoodQuality(Enum):
    HEALTHY = "gesund"
    VERY_HEALTHY = "sehr gesund"
    UNHEALTHY = "ungesund"
    VERY_UNHEALTHY = "sehr ungesund"
    BALANCED = "ausgeglichen"
    FAST_FOOD = "Fast-Food"
    HOME_MADE = "selbstgemacht"
    NEUTRAL = "neutral"

class HabitType(Enum):
    NUTRITION = "Ernährung"
    MOVEMENT = "Bewegung"
    SLEEPING = "Schlafen"
    SCREEN_TIME = "Bildschirmzeit"
    SOCIAL_MEDIA = "Soziale Medien"
    GAMING = "Spiele"
    SMOKE = "Rauchen"
    ALCOHOL = "Alkoholkonsum"
    DRUGS = "Drogenkonsum"
    EXPENDITURE = "Ausgaben"
    IMPULSE_CONTROL = "Impulskontrolle"
    SUGAR = "Zucker"
    CAFFEINE = "Koffeinkonsum"
    HYGIENE = "Hygiene"

class HouseAreaType(Enum):
    LIVINGROOM = "Wohnzimmer"
    BEDROOM = "Schlafzimmer"
    KITCHEN = "Küche"
    BATHROOM = "Badezimmer"
    STUDYROOM = "Arbeitszimmer"
    DININGROOM = "Esszimmer"
    FLOOR = "Flur"
    BALCONY = "Balkon"
    GARAGE = "Garage"
    TERRACE = "Terasse"
    GARDEN = "Garten"
    GENERAL = "Allgemein"

class HouseholdTask(Enum):
    COOKING = "kochen"
    CLEANING = "putzen"
    WASHING = "waschen"
    SHOPPING = "einkaufen"
    REPAIRS = "reparieren"
    GARDENING = "Gartenarbeit"
    TIDYING = "aufräumen"
    DISHES = "Geschirr"
    VACUUMING = "Staub saugen"
    OFFICE_WORK = "Büroarbeit"
    ORGANIZATION = "Organisation"

class Initiator(Enum):
    MYSELF = "Ich"
    PARTNER = "Partner"
    FRIENDS = "Freunde"
    FAMILY = "Familie"
    OTHER = "Andere"

class LanguageTrainingType(Enum):
    VOCABULARY = "Vokabeln"
    GRAMMAR = "Grammatik"
    PRONUNCIATION = "Aussprache"
    LISTENING = "Hören"
    READING = "Lesen"
    WRITING = "Schreiben"

class LearningFormatType(Enum):
    MIX = "Mix"
    BOOK = "Buch"
    VIDEO = "Video"
    PADCAST = "Podcast"
    COURSE = "Kurs"
    ONLINE_COURSE = "Onlinekurs"
    RESEARCH = "Recherche"
    DISCUSSION = "Diskussion"
    PRACTICE = "Praxis"
    GROUP_WORK = "Gruppenarbeit"
    REPETITION = "Wiederholung"
    EXERCISE = "Übung"
    LECTURE = "Vorlesung"
    LESSON = "Unterricht"

class Location(Enum):
    HOME = "zu Hause"
    WORK = "Arbeit"
    AWAY = "unterwegs"
    OUTSIDE = "draußen"
    SCHOOL = "Schule"
    UNIVERSITY = "Universität"
    GYM = "Fitnessstudio"
    FRIENDS = "Freunde"
    FAMILY = "Familie"

class MainMood(Enum):
    WORK = "Arbeit"
    FREETIME = "Freizeit"
    HEALTH = "Gesundheit"
    SOCIAL = "Soziales"
    PRIVATE = "Privat"
    FINANCE = "Finanzen"
    RELATIONSHIP = "Beziehung"

class MealType(Enum):
    BREAKFAST = "Frühstück"
    LUNCH = "Mittagessen"
    DINNER = "Abendessen"
    SNACK = "Snacks"

class MotivationReference(Enum):
    GENERAL = "Allgemein"
    SPORT = "Sport"
    LEARNING = "Lernen"
    WORK = "Arbeiten"
    SOCIAL = "Soziales"
    CREATIVITY = "Kreativität"

class MovementIntensity(Enum):
    LEISURELY = "gemütlich"
    MEDIUM = "mittel"
    STRONG = "stark"
    VERY_STRONG = "sehr stark"

class ObstacleType(Enum):
    LACK_OF_TIME = "Mangel an Zeit"
    LACK_OF_MOTIVATION = "Mangel an Motivation"
    LACK_OD_RESSOURCES = "Mangel an Ressourcen"
    STRESS = "Stress"
    SOCIAL_CAUSE = "Sozialer Anlass"
    EMOTIONAL_CAUSE = "Emotionaler Anlass"
    BOREDOM = "Langeweile"
    HABIT = "Gewohnheit"
    UNKNOWN = "Unbekannt"
    DIVERSION = "Ablenkung"
    FATIGUE = "Müdigkeit"
    DOUBT = "Zweifel"
    HEALTH_PROBLEMS = "Gesundheitliche Probleme"
    WEATHER = "Wetter"
    NO_REASON = "Kein Grund"

class Ocassion(Enum):
    EVERYDAY = "Alltag"
    CELEBRATION = "Feier"
    VACATION = "Urlaub"
    SOCIAL = "Sozial"
    FREETIME = "Freizeit"
    STRESS = "Stress"
    SPECIAL = "Besonderes"

class PortionSize(Enum):
    SMALL = "klein"
    MEDIUM = "mittel"
    LARGE = "groß"
    EXTRA_LARGE = "sehr groß"

class ReadingMedium(Enum):
    BOOK = "Buch"
    E_BOOK = "E-Book"
    ARTICLE = "Artikel"
    MAGAZINE = "Zeitschrift"
    NEWSPAPER = "Zeitung"
    BLOG = "Blog"
    COMIC = "Comic"

class RouteType(Enum):
    MIX = "Mix"
    ASPHALT = "Asphalt"
    ROAD = "Straße"
    FIELD_PATH = "Feldweg"
    FOREST_PATH = "Waldweg"
    GRAVEL = "Schotter"
    PARK = "Park"
    CITY = "Stadt"
    NATURE = "Natur"
    MOUNTAIN = "Berg"

class SideEffect(Enum):
    NO = "Keine"
    NAUSEA = "Übelkeit"
    VOMITING = "Erbrechen"
    DIZZINESS = "Schwindel"
    HEADACHE = "Kopfschmerzen"
    ABDOMINAL_PAIN = "Bauchschmerzen"
    DRY_MOUTH = "Trockener Mund"
    RED_EYES = "Rote Augen"
    ANXIENTY = "Angst"
    PARANOIA = "Paranoia"
    EUPHORIA = "Euphorie"
    FATIGUE = "Müdigkeit"
    SWEATING = "Schwitzen"
    INCREASED_PULSE = "Erhöhter Puls"
    DECREASED_PULSE = "Verringerter Puls"
    CONFUSION = "Verwirrtheit"
    LIMITED_COORDINATION = "Eingeschränkte Koordination"
    MEMORY_PROBLEMS = "Gedächtnisprobleme"
    INCREASED_APPETITE = "Appetitsteigerung"
    DECREASED_APPETITE = "Appetitverringerung"
    RESTLESSNESS = "Unruhe"
    INSOMNIA = "Schlaflosigkeit"
    MUSCLE_TENSION = "Muskelverspannung"
    SHIVERING = "Frösteln"
    OTHER = "Andere"

class SocialContext(Enum):
    ALLONE = "Alleine"
    PARTNER = "Partner"
    FAMILY = "Familie"
    FRIENDS = "Freunde"
    COLLEAGUES = "Kollegen"
    ACQUAINTANCE = "Bekannte"
    FOREIGN = "Fremde"
    GROUP = "Gruppe"
    PUBLIC = "Öffentlichkeit"

class StatusType(Enum):
    STARTED = "Begonnen"
    PARTIALLY = "Teilweise"
    ABORTED = "Abgebrochen"
    COMPLETED = "Abgeschlossen"

class Substance(Enum):
    NICOTINE = "Nikotin"
    ALCOHOL = "Alkohol"
    CANNABIS = "Cannabis"
    STIMULANT = "Kokain, Amphetamin, Ritalin"
    DEPRESSANT = "Benzos"
    PSYCHEDELIC = "LSD, Psilocybin"
    OPIOID = "Heroin, Oxycodon"
    DISSOCIATIVE = "Ketamin, DXM"
    EMPATHOGEN = "MDMA"
    CAFFEINE = "Koffein"
    MEDICATION = "Medikation"
    OTHERS = "Andere"

class SwimmingStyle(Enum):
    MIX = "Mix"
    FREETIME = "Freizeit"
    FRONT_CRAWL = "Kraulen"
    BACKSTROKE = "Rücken"
    BREASTSTROKE = "Brust"
    BUTTERFLY = "Schmetterling"
    DOLPHIN_KICK = "Delfin"
    TECHNIQUE = "Techniktraining"

class TimeOfDay(Enum):
    MORNING = "Morgen"
    LATE_MORNING = "Vormittag"
    MIDDAY = "Mittag"
    AFTERNOON = "Nachmittag"
    EVENING = "Abend"
    NIGHT = "Nacht"

class Trigger(Enum):
    STRESS = "Stress"
    BOREDOM = "Langeweile"
    WAKE_UP = "Aufwachen"
    GOING_TO_SLEEP = "Schlafen gehen"
    PAUSE = "Pause"
    EMOTIONAL_SITUATION = "Emotionale Situation"
    SOCIAL_SITUATION = "Soziale Situation"
    HABIT = "Gewohnheit"
    UNKNOWN = "Unbekannt"
    SUCCESS = "Erfolg"
    FRIENDS = "Freunde"
    FAMILY = "Familie"
    WORK = "Arbeit"
    SCHOOL = "Schule"
    FREETIME = "Freizeit"
    FATIGUE = "Müdigkeit"
    ANXIETY = "Angst"
    HAPPINESS = "Freude"
    SADNESS = "Traurigkeit"
    NATURE = "Natur"
    HOBBY = "Hobby"

class WaterSource(Enum):
    TAP_WATER = "Leitungswasser"
    MINERAL_WATER = "Mineralwasser"
    SPRING_WATER = "Quellwasser"
    BOTTLED_WATER = "Flaschenwasser"
    SPARKLING_WATER = "Sprudelwasser"

class WaterTemperature(Enum):
    COLD = "kalt"
    LUKEWARM = "lauwarm"
    WARM = "warm"

class Weather(Enum):
    SUNNY = "sonnig"
    CLOUDY = "bewölkt"
    RAINY = "regnerisch"
    SNOWY = "schnee"
    STORMY = "stürmisch"

class WorkoutType(Enum):
    MIX = "Mix"
    STRENGTH = "Krafttraining"
    ENDURANCE = "Ausdauertraining"
    FUNKTIONAL = "Funktionaltraining"
    CORE = "Coretraining"
    CARDIO = "Cardiotraining"
    YOGA = "Yoga"
    HIIT = "HIIT"
    PILATES = "Pilates"
    CROSSFIT = "Crossfit"
    STRETCHING = "Stretching"
    BOBILITY = "Mobilität"
    WEIGHT_LIFTING = "Gewichtheben"
    CALISTHENICS = "Calisthenics"

class WritingMedium(enum):
    MIX = "Mix"
    BOOK = "Buch"
    TERM_PAPER = "Hausarbeit"
    ESSAY = "Aufsatz"
    DIARY = "Tagebuch"
    BLOG = "Blog"
    POEM = "Gedicht"
    NOVEL = "Roman"
    NOTES = "Notizen"
    CREATIVE = "Kreativ"
    PROFESSIONAL = "beruflich"