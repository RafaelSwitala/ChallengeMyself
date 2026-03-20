import {
    AlcoholTypeEnum,
    ConsumptionMethodTypeEnum,
    ConsumptionProductTypeEnum,
    DeviceMainUseTypeEnum,
    DeviceTypeEnum,
    DrinkTemperatureTypeEnum,
    DrinkTypeEnum,
    EatingContextEnum,
    FoodQualityTypeEnum,
    HabitTypeEnum,
    HouseAreaTypeEnum,
    HouseholdTaskTypeEnum,
    InitiatorTypeEnum,
    LanguageTrainingTypeEnum,
    LearningFormatTypeEnum,
    LocationTypeEnum,
    MainMoodTypeEnum,
    MealTypeEnum,
    MotivationReferenceTypeEnum,
    ObstacleTypeEnum,
    OccasionTypeEnum,
    PortionSizeTypeEnum,
    ReadingMediumTypeEnum,
    RouteTypeEnum,
    SideEffectTypeEnum,
    SocialContextTypeEnum,
    StatusTypeEnum,
    SubstanceTypeEnum,
    SwimmingStyleTypeEnum,
    TimeOfDayTypeEnum,
    TriggerTypeEnum,
    WaterSourceTypeEnum,
    WaterTemperatureTypeEnum,
    WeatherTypeEnum,
    WorkoutTypeEnum,
    WritingMediumTypeEnum
} from "../enums/activityTypeEnums";
import { ChartTypeEnum } from "../enums/ChartTypeEnum";
import { FieldKeyEnum } from "../enums/FieldKeyEnum";
import { FieldTypeEnum } from "../enums/FieldTypeEnum";
import { Field } from "./FieldClass";


export const fieldModels: Record<FieldKeyEnum, Field> = {
  [FieldKeyEnum.Notes]: new Field(
    FieldKeyEnum.Notes,
    "Notizen",
    FieldTypeEnum.String,
    ChartTypeEnum.None
  ),
  [FieldKeyEnum.Distance]: new Field(
    FieldKeyEnum.Distance,
    "Distanz",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "km"
  ),
  [FieldKeyEnum.NumberOfSteps]: new Field(   
    FieldKeyEnum.NumberOfSteps,
    "Anzahl Schritte",
    FieldTypeEnum.Number,   
    ChartTypeEnum.Line,
    true,
    false,
    "Schritte"
  ),
  [FieldKeyEnum.Duration]: new Field(
    FieldKeyEnum.Duration,
    "Dauer",
    FieldTypeEnum.Number,   
    ChartTypeEnum.Line,
    true,
    false,
    "Minuten"
  ),
  [FieldKeyEnum.BreakDuration]: new Field(
    FieldKeyEnum.BreakDuration,
    "Dauer der Pausen",    
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Minuten"
  ),
  [FieldKeyEnum.MovementIntensity]: new Field(
    FieldKeyEnum.MovementIntensity,
    "Bewegungsintensität",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Intensität"
  ),
    [FieldKeyEnum.NumberOfBreaks]: new Field(
    FieldKeyEnum.NumberOfBreaks,
    "Anzahl der Pausen",
    FieldTypeEnum.Number,
    ChartTypeEnum.Bar,
    true,
    false,
    "Einheiten"
  ),
  [FieldKeyEnum.RouteType]: new Field(
    FieldKeyEnum.RouteType,
    "Streckenart",
    FieldTypeEnum.Enum,
    ChartTypeEnum.Bar,
    true,
    false ,
    undefined,
    RouteTypeEnum
  ),
  [FieldKeyEnum.Weather]: new Field(
    FieldKeyEnum.Weather,
    "Wetter",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    WeatherTypeEnum
  ),
  [FieldKeyEnum.CaloryConsumption]: new Field(
    FieldKeyEnum.CaloryConsumption,
    "Kalorienverbrauch",
    FieldTypeEnum.Number,   
    ChartTypeEnum.Line,
    true,
    false,
    "kcal"
  ),  
  [FieldKeyEnum.Altitude]: new Field(
    FieldKeyEnum.Altitude,
    "Höhe",
    FieldTypeEnum.Number,   
    ChartTypeEnum.Line,
    true,
    false,
    "m"
  ),
  [FieldKeyEnum.Heartbeat]: new Field(
    FieldKeyEnum.Heartbeat,
    "Herzfrequenz",
    FieldTypeEnum.Number,   
    ChartTypeEnum.Line,
    true,
    false,
    "bpm"
  ),
  [FieldKeyEnum.SwimmingStyle]: new Field(
    FieldKeyEnum.SwimmingStyle,
    "Schwimmstil",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    SwimmingStyleTypeEnum
  ),
  [FieldKeyEnum.WorkoutType]: new Field(
    FieldKeyEnum.WorkoutType,
    "Workout-Typ",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    WorkoutTypeEnum
  ),
  [FieldKeyEnum.NumberOfExercises]: new Field(
    FieldKeyEnum.NumberOfExercises,
    "Anzahl Übungen",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,   
    false,
    "Übungen"
  ),
  [FieldKeyEnum.ExerciseDuration]: new Field(
    FieldKeyEnum.ExerciseDuration,
    "Dauer der Übungen",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,   
    false,
    "Minuten"
  ),
  [FieldKeyEnum.NumberOfPages]: new Field(
    FieldKeyEnum.NumberOfPages,
    "Anzahl Seiten",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,   
    false,
    "Seiten"
  ),
  [FieldKeyEnum.ReadingVelocity]: new Field(
    FieldKeyEnum.ReadingVelocity,
    "Lesegeschwindigkeit",    
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,   
    false,
    "Seiten/Stunde"
  ),
  [FieldKeyEnum.ConcentrationLevel]: new Field(
    FieldKeyEnum.ConcentrationLevel,
    "Konzentrationswert",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,   
    false,
    "Wert"
  ),
  [FieldKeyEnum.SuccessLevel]: new Field(
    FieldKeyEnum.SuccessLevel,
    "Erfolgswert",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,   
    false,
    "Wert"
  ),
  [FieldKeyEnum.ReadMedium]: new Field(
    FieldKeyEnum.ReadMedium,
    "Lese-Medium",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    ReadingMediumTypeEnum
  ),
  [FieldKeyEnum.WriteMedium]: new Field(
    FieldKeyEnum.WriteMedium,
    "Schreib-Medium",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    WritingMediumTypeEnum
  ),
  [FieldKeyEnum.LearnFormat]: new Field(
    FieldKeyEnum.LearnFormat,
    "Lern-Format",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    LearningFormatTypeEnum
  ),
  [FieldKeyEnum.SleepQuality]: new Field(
    FieldKeyEnum.SleepQuality,
    "Schlafqualität",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Wert"
  ),
  [FieldKeyEnum.NumberOfWakeup]: new Field(
    FieldKeyEnum.NumberOfWakeup,
    "Anzahl der Aufwachvorgänge",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Anzahl"
  ),
  [FieldKeyEnum.SleepDuration]: new Field(
    FieldKeyEnum.SleepDuration,
    "Schlafdauer",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Stunden"
  ),
  [FieldKeyEnum.DeviceType]: new Field(
    FieldKeyEnum.DeviceType,
    "Gerätetyp",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    DeviceTypeEnum
  ),
  [FieldKeyEnum.DeviceMainUse]: new Field(
    FieldKeyEnum.DeviceMainUse,
    "Hauptverwendung des Geräts",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    DeviceMainUseTypeEnum
  ),
  [FieldKeyEnum.DrinkingAmount]: new Field(
    FieldKeyEnum.DrinkingAmount,
    "Menge",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Einheiten"
  ),
  [FieldKeyEnum.WaterSource]: new Field(
    FieldKeyEnum.WaterSource,
    "Wasserquelle",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    WaterSourceTypeEnum
  ),
  [FieldKeyEnum.WaterTemperature]: new Field(
    FieldKeyEnum.WaterTemperature,
    "Wassertemperatur",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    undefined,
    WaterTemperatureTypeEnum
  ),
  [FieldKeyEnum.DrinkingType]: new Field(
    FieldKeyEnum.DrinkingType,
    "Getränketyp",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    DrinkTypeEnum
  ),
  [FieldKeyEnum.AlcoholType]: new Field(
    FieldKeyEnum.AlcoholType,
    "Alkoholtyp",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    AlcoholTypeEnum
  ),
  [FieldKeyEnum.DrinkingTemperature]: new Field(
    FieldKeyEnum.DrinkingTemperature,
    "Getränketemperatur",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line, 
    true,
    false,
    undefined,
    DrinkTemperatureTypeEnum
  ),
  [FieldKeyEnum.Occasion]: new Field(
    FieldKeyEnum.Occasion,
    "Anlass",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    OccasionTypeEnum
  ),
  [FieldKeyEnum.ConsumptionCount]: new Field(
    FieldKeyEnum.ConsumptionCount,
    "Rauchmenge",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,    
    "Zigaretten"
  ),
  [FieldKeyEnum.ConsumptionProduct]: new Field(
    FieldKeyEnum.ConsumptionProduct,
    "Rauchprodukt",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    ConsumptionProductTypeEnum
  ),
  [FieldKeyEnum.CravingIntensity]: new Field(
    FieldKeyEnum.CravingIntensity,
    "Craving-Intensität",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Intensität"
  ),
  [FieldKeyEnum.MoodLevel]: new Field(
    FieldKeyEnum.MoodLevel,
    "Stimmungswert",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Wert"
  ),
  [FieldKeyEnum.StressLevel]: new Field(
    FieldKeyEnum.StressLevel,
    "Stresswert",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Wert"
  ),
  [FieldKeyEnum.MotivationLevel]: new Field(
    FieldKeyEnum.MotivationLevel,
    "Motivationswert",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Wert"
  ),
  [FieldKeyEnum.MainMood]: new Field(
    FieldKeyEnum.MainMood,
    "Hauptstimmung",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    MainMoodTypeEnum
  ),
  [FieldKeyEnum.Trigger]: new Field(
    FieldKeyEnum.Trigger,
    "Auslöser",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    TriggerTypeEnum
  ),
  [FieldKeyEnum.TimeOfDay]: new Field(
    FieldKeyEnum.TimeOfDay,
    "Tageszeit",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    TimeOfDayTypeEnum
  ),
  [FieldKeyEnum.Obstacle]: new Field(
    FieldKeyEnum.Obstacle,
    "Hindernis",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    ObstacleTypeEnum
  ),
  [FieldKeyEnum.PhysicalDiscomfort]: new Field(
    FieldKeyEnum.PhysicalDiscomfort,
    "Physisches Unwohlsein",    
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,    "Wert"
  ),
  [FieldKeyEnum.PhysicalEnergy]: new Field(
    FieldKeyEnum.PhysicalEnergy,
    "Physische Energie",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Wert"
  ),
  [FieldKeyEnum.MentalEnergy]: new Field(
    FieldKeyEnum.MentalEnergy,
    "Mentale Energie",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Wert"
  ),
  [FieldKeyEnum.SelfConfidence]: new Field(
    FieldKeyEnum.SelfConfidence,
    "Selbstvertrauen",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Wert"
  ),
  [FieldKeyEnum.MotivationReference]: new Field(
    FieldKeyEnum.MotivationReference,
    "Motivationsreferenz",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    MotivationReferenceTypeEnum
  ),
  [FieldKeyEnum.CostsAmount]: new Field(
    FieldKeyEnum.CostsAmount,
    "Kosten",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Euro"
  ),
  [FieldKeyEnum.AnxietyLevel]: new Field(
    FieldKeyEnum.AnxietyLevel,
    "Angstlevel",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Wert"
  ),
  [FieldKeyEnum.FocusLevel]: new Field(
    FieldKeyEnum.FocusLevel,
    "Fokuslevel",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Wert"
  ),
  [FieldKeyEnum.LocationType]: new Field(
    FieldKeyEnum.LocationType,
    "Ortstyp",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    LocationTypeEnum
  ),
  [FieldKeyEnum.SocialContext]: new Field(
    FieldKeyEnum.SocialContext,
    "Sozialer Kontext",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    SocialContextTypeEnum
  ),
  [FieldKeyEnum.HouseholdTask]: new Field(
    FieldKeyEnum.HouseholdTask,
    "Haushaltsaufgabe",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    HouseholdTaskTypeEnum
  ),
  [FieldKeyEnum.HouseArea]: new Field(
    FieldKeyEnum.HouseArea,
    "Bereich im Haus",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    HouseAreaTypeEnum
  ),
  [FieldKeyEnum.Status]: new Field(
    FieldKeyEnum.Status,
    "Status",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    StatusTypeEnum
  ),
  [FieldKeyEnum.MealType]: new Field(
    FieldKeyEnum.MealType,
    "Mahlzeitentyp",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    MealTypeEnum
  ),
  [FieldKeyEnum.FoodQuality]: new Field(
    FieldKeyEnum.FoodQuality,
    "Lebensmittelqualität",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    FoodQualityTypeEnum
  ),
  [FieldKeyEnum.PortionSize]: new Field(
    FieldKeyEnum.PortionSize,
    "Portionsgröße",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    PortionSizeTypeEnum
  ),
  [FieldKeyEnum.HungerLevel]: new Field(
    FieldKeyEnum.HungerLevel,
    "Hungerlevel",
    FieldTypeEnum.Number,
    ChartTypeEnum.Line,
    true,
    false,
    "Wert"
  ),
  [FieldKeyEnum.SatietyLevel]: new Field(
    FieldKeyEnum.SatietyLevel,
    "Sättigungslevel",
    FieldTypeEnum.Number,   
    ChartTypeEnum.Line,
    true,
    false,
    "Wert"
  ),
  [FieldKeyEnum.EatingContext]: new Field(
    FieldKeyEnum.EatingContext,
    "Essenskontext",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    EatingContextEnum
  ),
  [FieldKeyEnum.Language]: new Field(
    FieldKeyEnum.Language,
    "Sprache",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false
  ),
  [FieldKeyEnum.LanguageTrainingType]: new Field(
    FieldKeyEnum.LanguageTrainingType,
    "Sprachtrainingstyp",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    LanguageTrainingTypeEnum
  ),
  [FieldKeyEnum.ConsumptionMethod]: new Field(
    FieldKeyEnum.ConsumptionMethod,
    "Konsumart",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    ConsumptionMethodTypeEnum
  ),
  [FieldKeyEnum.HabitType]: new Field(
    FieldKeyEnum.HabitType,
    "Gewohnheitstyp",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    HabitTypeEnum
  ),
  [FieldKeyEnum.Initiator]: new Field(
    FieldKeyEnum.Initiator,
    "Initiator",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    InitiatorTypeEnum
  ),
  [FieldKeyEnum.SideEffect]: new Field(
    FieldKeyEnum.SideEffect,
    "Nebenwirkungen",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    SideEffectTypeEnum
  ),
  [FieldKeyEnum.SubstanceType]: new Field(
    FieldKeyEnum.SubstanceType,
    "Substanz-Art",
    FieldTypeEnum.String,
    ChartTypeEnum.Bar,
    true,
    false,
    undefined,
    SubstanceTypeEnum
  ),
  [FieldKeyEnum.ConflictLevel]: new Field(
    FieldKeyEnum.ConflictLevel,
    "Konflikt Level",
    FieldTypeEnum.Number,
    ChartTypeEnum.Bar,
    true,
    false,
    "Einheiten"
  ),
  [FieldKeyEnum.SatisfactionLevel]: new Field(
    FieldKeyEnum.SatisfactionLevel,
    "Zufriedenheit",
    FieldTypeEnum.Number,
    ChartTypeEnum.Bar,
    true,
    false,
    "Einheiten"
  ),
  [FieldKeyEnum.QualityLevel]: new Field(
    FieldKeyEnum.QualityLevel,
    "Qualität",
    FieldTypeEnum.Number,
    ChartTypeEnum.Bar,
    true,
    false,
    "Einheiten"
  ),
  [FieldKeyEnum.NumberOfMembers]: new Field(
    FieldKeyEnum.NumberOfMembers,
    "Anzahl der Personen",
    FieldTypeEnum.Number,
    ChartTypeEnum.Bar,
    true,
    false,
    "Einheiten"
  ),
  [FieldKeyEnum.HarmonyLevel]: new Field(
    FieldKeyEnum.HarmonyLevel,
    "Harmonie-Level",
    FieldTypeEnum.Number,
    ChartTypeEnum.Bar,
    true,
    false,
    "Einheiten"
  ),
  [FieldKeyEnum.IntensityLevel]: new Field(
    FieldKeyEnum.IntensityLevel,
    "Intensität",
    FieldTypeEnum.Number,
    ChartTypeEnum.Bar,
    true,
    false,
    "Einheiten"
  ),
  [FieldKeyEnum.MoodBefore]: new Field(
    FieldKeyEnum.MoodBefore,
    "Stimmung davor",
    FieldTypeEnum.Number,
    ChartTypeEnum.Bar,
    true,
    false,
    "Einheiten"
  ),
  [FieldKeyEnum.MoodAfter]: new Field(
    FieldKeyEnum.MoodAfter,
    "Stimmung danach",
    FieldTypeEnum.Number,
    ChartTypeEnum.Bar,
    true,
    false,
    "Einheiten"
  ),
};
