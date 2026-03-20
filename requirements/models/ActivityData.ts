import { ActivityTypeEnum } from '../enums/ActivityTypeEnum';
import { FieldKeyEnum } from '../enums/FieldKeyEnum';
import { Activity } from './ActivityClass';

export const activities: Activity[] = [
  new Activity(ActivityTypeEnum.Alkoholkonsum, [

  ]),
  new Activity(ActivityTypeEnum.Ausgaben, [

  ]),
  new Activity(ActivityTypeEnum.Beziehungszeit, [

  ]),
  new Activity(ActivityTypeEnum.Bildschirmzeit, [

  ]),
  new Activity(ActivityTypeEnum.Drogenkonsum, [

  ]),
  new Activity(ActivityTypeEnum.Ernaehrung, [

  ]),
  new Activity(ActivityTypeEnum.Familienzeit, [

  ]),
  new Activity(ActivityTypeEnum.Getraenkekonsum, [

  ]),
  new Activity(ActivityTypeEnum.Gewohnheitsbruch, [

  ]),
  new Activity(ActivityTypeEnum.Haushaltsaktivitaeten, [

  ]),
  new Activity(ActivityTypeEnum.Joggen, [
    FieldKeyEnum.Notes,
    FieldKeyEnum.Distance,
    { key: FieldKeyEnum.Duration, required: true },
    FieldKeyEnum.NumberOfSteps,
    FieldKeyEnum.NumberOfBreaks,
    FieldKeyEnum.BreakDuration,
    FieldKeyEnum.MovementIntensity,
    FieldKeyEnum.RouteType,
    FieldKeyEnum.Weather,
    FieldKeyEnum.CaloryConsumption,
    FieldKeyEnum.Altitude,
    FieldKeyEnum.PhysicalEnergy,
    FieldKeyEnum.MotivationLevel,
    FieldKeyEnum.TimeOfDay
  ]),
  new Activity(ActivityTypeEnum.Koffeinkonsum, [

  ]),
    new Activity(ActivityTypeEnum.Kreativitaet, [

  ]),
  new Activity(ActivityTypeEnum.Kunst, [

  ]),
  new Activity(ActivityTypeEnum.Laufen, [

  ]),
  new Activity(ActivityTypeEnum.Lernen, [

  ]),
    new Activity(ActivityTypeEnum.Lesen, [

  ]),
  new Activity(ActivityTypeEnum.Meditation, [

  ]),
  new Activity(ActivityTypeEnum.Motivation, [

  ]),
  new Activity(ActivityTypeEnum.Musikpraxis, [

  ]),
    new Activity(ActivityTypeEnum.Natur, [

  ]),
  new Activity(ActivityTypeEnum.Produktivitaet, [

  ]),
  new Activity(ActivityTypeEnum.Radfahren, [

  ]),
  new Activity(ActivityTypeEnum.Rauchverhalten, [

  ]),
    new Activity(ActivityTypeEnum.Schlaf, [

  ]),
  new Activity(ActivityTypeEnum.Schreiben, [

  ]),
  new Activity(ActivityTypeEnum.Schwimmen, [

  ]),
  new Activity(ActivityTypeEnum.SozialeInteraktion, [

  ]),
  new Activity(ActivityTypeEnum.Sparen, [

  ]),
  new Activity(ActivityTypeEnum.Spazieren, [

  ]),
  new Activity(ActivityTypeEnum.Sprachtraining, [

  ]),
    new Activity(ActivityTypeEnum.Stimmung, [

  ]),
  new Activity(ActivityTypeEnum.Stress, [

  ]),
  new Activity(ActivityTypeEnum.Wandern, [
    FieldKeyEnum.Notes,
    FieldKeyEnum.Distance,
    { key: FieldKeyEnum.Duration, required: false },
    FieldKeyEnum.RouteType,
    FieldKeyEnum.Weather,
    FieldKeyEnum.TimeOfDay
  ]),
  new Activity(ActivityTypeEnum.Wasserkonsum, [

  ]),
  new Activity(ActivityTypeEnum.Workout, [

  ]),
  new Activity(ActivityTypeEnum.Yoga, [

  ]),
];
