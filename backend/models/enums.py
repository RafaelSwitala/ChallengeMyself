"""
Zentrale Enum-Definitionen für das ChallengeMyself System
"""

from enum import Enum


class ActivityType(Enum):
    """40+ Aktivitätstypen"""
    # ALCOHOL_CONSUMPTION = "Alkoholkonsum"
    # ANXIETY = "Angstlevel"
    # ART = "Kunst"
    # BUDGETING = "Budgetplanung"
    # CAFFEINE_CONSUMPTION = "Koffeinkonsum"
    # COMMUNITY_ENGAGEMENT = "Gemeinschaftsaktivität"
    # CREATIVITY = "Kreativitaet"
    # CULTURAL_EVENTS = "Kulturelle Veranstaltungen"
    # CYCLING = "Radfahren"
    # DRINK_CONSUMPTION = "Getränkekonsum"
    # DRUG_USE = "Drogenkonsum"
    # EATING = "Ernährung"
    # ENERGY = "Energie"
    # EXPENSES = "Ausgaben"
    # FAMILY_TIME = "Familienzeit"
    # GAMBLING = "Glücksspiel"
    # GRATITUDE = "Dankbarkeit"
    # HABIT_BREAKING = "Gewohnheitsbruch (Rückfälle)"
    # HABIT_TRACKING = "Gewohnheiten (aufbauen)"
    # HAPPINESS = "Glücksgefühl"
    # HEALTH_CHECK = "Gesundheitscheck"
    # HOUSEHOLD = "Haushalt"
    # IMMUNITY = "Immunsystem stärken"
    # INVESTING = "Investieren"
    JOGGING = "Joggen"
    # LANGUAGE_TRAINING = "Sprachtraining"
    # LEARNING = "Lernen"
    # MEDITATION = "Meditation"
    # MENTAL_EXERCISE = "Mentale Übungen"
    # MINDFULNESS = "Achtsamkeit"
    # MOOD = "Stimmung"
    # MOTIVATION = "Motivation"
    # MUSIC = "Musikpraxis"
    # NATURE = "Natur"
    # PRODUCTIVITY = "Produktivitaet"
    # READING = "Lesen"
    # REFLECTION = "Reflexion, Tagebuch"
    # RELATIONSHIP = "Beziehungszeit (Quality Time)"
    # SAVINGS = "Sparen"
    # SCREEN_TIME = "Bildschirmzeit"
    # SKILL_TRAINING = "Fertigkeitstraining"
    # SLEEPING = "Schlaf"
    # SMOKING = "Rauchverhalten"
    # SNACKING = "Snacks"
    # SOCIAL_INTERACTION = "Soziale Interaktion"
    #  SPORTS = "Sportarten"
    # STRESS = "Stress"
    # SWIMMING = "Schwimmen"
    # TRAVELING = "Reisen"
    # VOLUNTEERING = "Freiwilligenarbeit"
    # WALKING = "Spazieren"
    # WANDERING = "Wandern"
    # WATER_CONSUMPTION = "Wasserkonsum"
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
    BEER = "Bier"
    WINE = "Wein"
    SPARKLING_WINE = "Sekt"
    SPIRITS = "Spirituosen"
    LONGDRINK = "Longdrink"
    COCKTAIL = "Cocktail"
    CIDER = "Apfelwein"

class AnxietyReasonType(Enum):
    SOCIAL = "Sozial"
    TRAUMA = "Trauma"
    SUBSTANCE = "Substanzen, Medikamente"
    UNKNOWN = "Unbekannt"

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

class BudgetCategoryType(Enum):
    INCOME = "Einnahmen"
    EXPENSE = "Ausgaben"
    SAVINGS = "Ersparnisse"
    INVESTMENTS = "Investitionen"
    DEBT = "Schulden"

class CommunityActivityType(Enum):
    VOLUNTEERING = "Freiwilligenarbeit"
    SPORTS_TEAM = "Sportverein"
    CLUBS = "Vereine"
    MEETUPS = "Treffen"
    WORKSHOP = "Workshop"
    ONLINE_COMMUNITY = "Online-Community"
    SOCIAL_EVENTS = "Soziale Events"

class ConsumptionProductType(Enum):
    CIGARETTE = "Zigarette"
    CIGAR = "Zigarre"
    PIPE = "Pfeife"
    SHISHA = "Shisha"
    E_CIGARETTE = "E-Zigarette"
    VAPE = "Vape"

class CulturalEventType(Enum):
    CONCERT = "Konzert"
    THEATER = "Theater"
    MUSEUM = "Museum / Ausstellung"
    CINEMA = "Kino"
    FESTIVAL = "Festival"
    LECTURE = "Vortrag / Lesung"
    DANCE = "Tanzveranstaltung"
    FAIR = "Messe / Jahrmarkt"

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

class DrinkTemperatureType(Enum):
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

class EatingContextType(Enum):
    ALLONE = "Alleine"
    FRIENDS = "mit Freunden"
    FAMILY = "mit Familie"
    AWAY = "unterwegs"
    RESTAURANT = "Restaurant"
    WORK = "Auf der Arbeit"

class ExpensesType(Enum):
    HOUSING = "Wohnen"
    UTILITIES = "Nebenkosten"
    FOOD = "Lebensmittel"
    TRANSPORT = "Transport"
    HEALTH = "Gesundheit"
    INSURANCE = "Versicherung"
    LEISURE = "Freizeit"
    EDUCATION = "Bildung"
    SHOPPING = "Einkäufe"
    CHARITY = "Spenden"

class FoodQualityType(Enum):
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
    EXERCISE = "Bewegung, Sport"
    HEALTHY_EATING = "Gesunde Ernährung"
    HYDRATION = "Ausreichend trinken"
    SLEEP_ROUTINE = "Schlafroutine"
    READING = "Lesen"
    JOURNALING = "Tagebuch schreiben"
    SKILL_PRACTICE = "Fertigkeitstraining"
    SOCIAL_CONTACTS = "Soziale Kontakte pflegen"
    MINDFUL_BREAKS = "Bewusste Pausen"

class HealthCheckType(Enum):
    GENERAL_CHECKUP = "Allgemeine Untersuchung"
    DENTAL = "Zahnarzt"
    EYE = "Augenarzt"
    BLOOD_TEST = "Bluttest"
    VACCINATION = "Impfung"
    SCREENING = "Screening / Früherkennung"
    SPECIALIST = "Facharztbesuch"
    PHYSICAL_FITNESS = "Sportliche Untersuchung / Fitnesscheck"

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

class HouseholdTaskType(Enum):
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

class ImmuneBoostType(Enum):
    NUTRITION = "Gesunde Ernährung"
    SLEEP = "Ausreichend Schlaf"
    EXERCISE = "Regelmäßige Bewegung"
    STRESS_MANAGEMENT = "Stress reduzieren"
    SUNLIGHT = "Sonnenlicht / Vitamin D"
    HYDRATION = "Ausreichend trinken"
    VACCINATIONS = "Impfungen"
    HYGIENE = "Hygienemaßnahmen"

class IncomeType(Enum):
    SALARY = "Gehalt"
    FREELANCE = "Freiberuflich"
    INVESTMENTS = "Investitionen"
    GIFTS = "Geschenke"

class InitiatorType(Enum):
    MYSELF = "Ich"
    PARTNER = "Partner"
    FRIENDS = "Freunde"
    FAMILY = "Familie"
    OTHER = "Andere"

class InvestmentTypes(Enum):
    STOCKS = "Aktien"
    BONDS = "Anleihen"
    REAL_ESTATE = "Immobilien"
    CRYPTOCURRENCY = "Kryptowährungen"
    MUTUAL_FUNDS = "Investmentfonds"
    ETFS = "ETFs"
    COMMODITIES = "Rohstoffe"
    OTHER = "Sonstiges"

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

class LocationType(Enum):
    HOME = "zu Hause"
    WORK = "Arbeit"
    AWAY = "unterwegs"
    OUTSIDE = "draußen"
    SCHOOL = "Schule"
    UNIVERSITY = "Universität"
    GYM = "Fitnessstudio"
    FRIENDS = "Freunde"
    FAMILY = "Familie"

class MainMoodType(Enum):
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

class MentalExerciseType(Enum):
    MEDITATION = "Meditation"
    BREATHING = "Atemübungen"
    MINDFULNESS = "Achtsamkeit"
    COGNITIVE_TRAINING = "Kognitives Training"
    VISUALIZATION = "Visualisierung"
    RELAXATION = "Entspannungsübungen"
    GRATITUDE = "Dankbarkeitstagebuch"

class MindfulnessExerciseType(Enum):
    MEDITATION = "Meditation"
    BREATHING = "Atemübungen"
    BODY_SCAN = "Body Scan"
    MINDFUL_WALK = "Achtsames Gehen"
    GRATITUDE = "Dankbarkeitspraxis"
    MINDFUL_EATING = "Achtsames Essen"
    VISUALIZATION = "Visualisierung"

class MotivationReferenceType(Enum):
    GENERAL = "Allgemein"
    SPORT = "Sport"
    LEARNING = "Lernen"
    WORK = "Arbeiten"
    SOCIAL = "Soziales"
    CREATIVITY = "Kreativität"

class MovementIntensityType(Enum):
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

class OcassionType(Enum):
    EVERYDAY = "Alltag"
    CELEBRATION = "Feier"
    VACATION = "Urlaub"
    SOCIAL = "Sozial"
    FREETIME = "Freizeit"
    STRESS = "Stress"
    SPECIAL = "Besonderes"

class PortionSizeType(Enum):
    SMALL = "klein"
    MEDIUM = "mittel"
    LARGE = "groß"
    EXTRA_LARGE = "sehr groß"

class ReadingMediumType(Enum):
    BOOK = "Buch"
    E_BOOK = "E-Book"
    ARTICLE = "Artikel"
    MAGAZINE = "Zeitschrift"
    NEWSPAPER = "Zeitung"
    BLOG = "Blog"
    COMIC = "Comic"

class ReflectionType(Enum):
    JOURNALING = "Tagebuch schreiben"
    SELF_QUESTIONING = "Selbstbefragung"
    MEDITATIVE_REFLECTION = "Meditative Reflexion"
    FEEDBACK = "Feedback einholen"
    GOAL_REVIEW = "Zielüberprüfung"
    GRATITUDE = "Dankbarkeitsreflexion"

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

class SavingGoalType(Enum):
    EMERGENCY_FUND = "Notfallfonds"
    VACATION = "Urlaub"
    BIG_PURCHASE = "Großer Einkauf"
    RETIREMENT = "Rente"
    INVESTMENTS = "Investitionen"

class SideEffectType(Enum):
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

class SkillTrainingType(Enum):
    LANGUAGE = "Sprache lernen"
    MUSICAL = "Musik / Instrument"
    ARTISTIC = "Kunst / Kreativität"
    CODING = "Programmieren"
    SPORTS_SKILLS = "Sportliche Fähigkeiten"
    COOKING = "Kochen"
    HANDICRAFT = "Handwerk / DIY"
    LEADERSHIP = "Führungskompetenzen"

class SnackType(Enum):
    FRUITS = "Obst"
    VEGETABLES = "Gemüse"
    NUTS = "Nüsse"
    CHOCOLATE = "Schokolade"
    CHIPS = "Chips / Salzige Snacks"
    SWEETS = "Süßigkeiten"
    YOGURT = "Joghurt"
    OTHER = "Sonstiges"

class SocialContextType(Enum):
    ALLONE = "Alleine"
    PARTNER = "Partner"
    FAMILY = "Familie"
    FRIENDS = "Freunde"
    COLLEAGUES = "Kollegen"
    ACQUAINTANCE = "Bekannte"
    FOREIGN = "Fremde"
    GROUP = "Gruppe"
    PUBLIC = "Öffentlichkeit"

class SportType(Enum):
    RUNNING = "Laufen"
    SWIMMING = "Schwimmen"
    CYCLING = "Radfahren"
    YOGA = "Yoga"
    WEIGHT_TRAINING = "Krafttraining"
    TEAM_SPORTS = "Mannschaftssport"
    MARTIAL_ARTS = "Kampfsport"
    DANCE = "Tanzen"
    HIKING = "Wandern"
    OTHER = "Sonstiges"

class StatusType(Enum):
    STARTED = "Begonnen"
    PARTIALLY = "Teilweise"
    ABORTED = "Abgebrochen"
    COMPLETED = "Abgeschlossen"

class SubstanceType(Enum):
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

class SwimmingStyleType(Enum):
    MIX = "Mix"
    FREETIME = "Freizeit"
    FRONT_CRAWL = "Kraulen"
    BACKSTROKE = "Rücken"
    BREASTSTROKE = "Brust"
    BUTTERFLY = "Schmetterling"
    DOLPHIN_KICK = "Delfin"
    TECHNIQUE = "Techniktraining"

class TimeOfDayType(Enum):
    MORNING = "Morgen"
    LATE_MORNING = "Vormittag"
    MIDDAY = "Mittag"
    AFTERNOON = "Nachmittag"
    EVENING = "Abend"
    NIGHT = "Nacht"

class TravelType(Enum):
    LEISURE = "Freizeit / Urlaub"
    BUSINESS = "Geschäftlich"
    CULTURAL = "Kulturreisen"
    NATURE = "Natur- / Outdoorreisen"
    ADVENTURE = "Abenteuer / Aktivurlaub"
    STAYCATION = "Urlaub zuhause"
    FAMILY = "Familie"

class TriggerType(Enum):
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

class VolunteeringType(Enum):
    COMMUNITY_SERVICE = "Gemeinnützige Arbeit"
    ENVIRONMENTAL = "Umweltschutz"
    EDUCATION = "Bildung / Nachhilfe"
    ANIMAL_CARE = "Tierschutz"
    HEALTHCARE = "Gesundheitswesen"
    EVENT_SUPPORT = "Veranstaltungsunterstützung"

class WaterSourceType(Enum):
    TAP_WATER = "Leitungswasser"
    MINERAL_WATER = "Mineralwasser"
    SPRING_WATER = "Quellwasser"
    BOTTLED_WATER = "Flaschenwasser"
    SPARKLING_WATER = "Sprudelwasser"

class WaterTemperatureType(Enum):
    COLD = "kalt"
    LUKEWARM = "lauwarm"
    WARM = "warm"

class WeatherType(Enum):
    SUNNY = "sonnig"
    CLOUDY = "bewölkt"
    RAINY = "regnerisch"
    SNOWY = "schnee"
    STORMY = "stürmisch"

class WeatherExposureType(Enum):
    SUNLIGHT = "Sonnenlicht / UV-Exposition"
    COLD = "Kälte"
    HEAT = "Hitze"
    RAIN = "Regen"
    WIND = "Wind"
    FRESH_AIR = "Frische Luft"

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

class WritingMediumType(Enum):
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