import { ActivityTypeEnum } from "../../enums/ActivityTypeEnum";
import { GoalTypeEnum } from "../../enums/GoalTypeEnum";

/**
 * Definiert, welche Goal-Typen für welche Aktivitäten verfügbar sind
 * Diese Mappings ermöglichen es, nur sinnvolle Goals für eine Aktivität anzuzeigen
 */
export const activityGoalsMapping: Record<ActivityTypeEnum, GoalTypeEnum[]> = {
  // Joggen: Entfernung, Häufigkeit und Streaks
  [ActivityTypeEnum.Joggen]: [GoalTypeEnum.MoreThan, GoalTypeEnum.FrequencyExact],

  // Wandern
  [ActivityTypeEnum.Wandern]: [],

  // Weitere Aktivitäten können später hinzugefügt werden
  [ActivityTypeEnum.Alkoholkonsum]: [],
  [ActivityTypeEnum.Ausgaben]: [],
  [ActivityTypeEnum.Beziehungszeit]: [],
  [ActivityTypeEnum.Bildschirmzeit]: [],
  [ActivityTypeEnum.Drogenkonsum]: [],
  [ActivityTypeEnum.Energie]: [],
  [ActivityTypeEnum.Ernaehrung]: [],
  [ActivityTypeEnum.Familienzeit]: [],
  [ActivityTypeEnum.Getraenkekonsum]: [],
  [ActivityTypeEnum.Gewohnheitsbruch]: [],
  [ActivityTypeEnum.Haushaltsaktivitaeten]: [],
  [ActivityTypeEnum.Koffeinkonsum]: [],
  [ActivityTypeEnum.Kreativitaet]: [],
  [ActivityTypeEnum.Kunst]: [],
  [ActivityTypeEnum.Laufen]: [],
  [ActivityTypeEnum.Lernen]: [],
  [ActivityTypeEnum.Lesen]: [],
  [ActivityTypeEnum.Meditation]: [],
  [ActivityTypeEnum.Motivation]: [],
  [ActivityTypeEnum.Musikpraxis]: [],
  [ActivityTypeEnum.Natur]: [],
  [ActivityTypeEnum.Produktivitaet]: [],
  [ActivityTypeEnum.Radfahren]: [],
  [ActivityTypeEnum.Rauchverhalten]: [],
  [ActivityTypeEnum.Schlaf]: [],
  [ActivityTypeEnum.Schreiben]: [],
  [ActivityTypeEnum.Schwimmen]: [],
  [ActivityTypeEnum.SozialeInteraktion]: [],
  [ActivityTypeEnum.Sparen]: [],
  [ActivityTypeEnum.Spazieren]: [],
  [ActivityTypeEnum.Sprachtraining]: [],
  [ActivityTypeEnum.Stimmung]: [],
  [ActivityTypeEnum.Stress]: [],
  [ActivityTypeEnum.Wasserkonsum]: [],
  [ActivityTypeEnum.Workout]: [],
  [ActivityTypeEnum.Yoga]: [],
};

/**
 * Gibt alle verfügbaren Goal-Typen für eine bestimmte Aktivität zurück
 */
export const getAvailableGoalsForActivity = (activity: ActivityTypeEnum): GoalTypeEnum[] => {
  return activityGoalsMapping[activity] || [];
};

/**
 * Prüft, ob ein Goal-Typ für eine bestimmte Aktivität verfügbar ist
 */
export const isGoalAvailableForActivity = (
  activity: ActivityTypeEnum,
  goalType: GoalTypeEnum
): boolean => {
  const availableGoals = getAvailableGoalsForActivity(activity);
  return availableGoals.includes(goalType);
};

