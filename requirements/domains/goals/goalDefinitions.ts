import { FieldKeyEnum } from "../../enums/FieldKeyEnum";
import { GoalPeriodTypeEnum } from "../../enums/GoalPeriodTypeEnum";
import { GoalTypeEnum } from "../../enums/GoalTypeEnum";
import { Goal } from "../../models/GoalClass";

/**
 * Factory-Funktionen für verschiedene Goal-Typen
 * Jede Funktion erstellt ein Goal mit vordefinierter Logik
 */

/**
 * MoreThan: Ziel - Mehr als...
 * Beispiel: Mehr als 10km in der Woche joggen
 */
export const createMoreThanGoal = (
  description: string,
  variableReference: FieldKeyEnum | string,
  targetValue: number,
  period: GoalPeriodTypeEnum
): Goal => {
  return new Goal({
    description,
    variableReference: variableReference as string,
    type: GoalTypeEnum.MoreThan,
    target: targetValue,
    period,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  });
};

/**
 * LessThan: Ziel - Weniger als...
 * Beispiel: Weniger als 30 Minuten Bildschirmzeit pro Tag
 */
export const createLessThanGoal = (
  description: string,
  variableReference: FieldKeyEnum | string,
  targetValue: number,
  period: GoalPeriodTypeEnum
): Goal => {
  return new Goal({
    description,
    variableReference: variableReference as string,
    type: GoalTypeEnum.LessThan,
    target: targetValue,
    period,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  });
};

/**
 * Avoid: Ziel - Ganz vermeiden
 * Beispiel: Keine Aktivität "Rauchen" in dieser Woche
 */
export const createAvoidGoal = (
  description: string,
  variableReference: FieldKeyEnum | string,
  period: GoalPeriodTypeEnum
): Goal => {
  return new Goal({
    description,
    variableReference: variableReference as string,
    type: GoalTypeEnum.Avoid,
    target: 0,
    period,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  });
};

/**
 * FrequencyExact: Ziel - Exakt x-Mal pro Woche/Monat
 * Beispiel: Genau 3x pro Woche joggen
 */
export const createFrequencyExactGoal = (
  description: string,
  variableReference: FieldKeyEnum | string,
  frequency: number, // Wie oft
  period: GoalPeriodTypeEnum
): Goal => {
  return new Goal({
    description,
    variableReference: variableReference as string,
    type: GoalTypeEnum.FrequencyExact,
    target: frequency,
    period,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  });
};

/**
 * FrequencyMax: Ziel - Maximal x-Mal pro Woche/Monat
 * Beispiel: Maximal 2x pro Woche Alkoholkonsum
 */
export const createFrequencyMaxGoal = (
  description: string,
  variableReference: FieldKeyEnum | string,
  maxFrequency: number,
  period: GoalPeriodTypeEnum
): Goal => {
  return new Goal({
    description,
    variableReference: variableReference as string,
    type: GoalTypeEnum.FrequencyMax,
    target: maxFrequency,
    period,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  });
};

/**
 * FrequencyMin: Ziel - Mindestens x-Mal pro Woche/Monat
 * Beispiel: Mindestens 4x pro Woche trainieren
 */
export const createFrequencyMinGoal = (
  description: string,
  variableReference: FieldKeyEnum | string,
  minFrequency: number,
  period: GoalPeriodTypeEnum
): Goal => {
  return new Goal({
    description,
    variableReference: variableReference as string,
    type: GoalTypeEnum.FrequencyMin,
    target: minFrequency,
    period,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  });
};

/**
 * Streak: Ziel - x-mal in Folge das Ziel erreichen
 * Beispiel: 30 Tage hintereinander das tägliche Ziel erreichen
 */
export const createStreakGoal = (
  description: string,
  variableReference: FieldKeyEnum | string,
  streakDays: number,
  period: GoalPeriodTypeEnum
): Goal => {
  return new Goal({
    description,
    variableReference: variableReference as string,
    type: GoalTypeEnum.Streak,
    target: streakDays,
    period,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  });
};

/**
 * IncreaseDaily: Ziel - Täglich x mehr bis zu bestimmtem Ziel
 * Beispiel: Täglich 1 Minute mehr trainieren bis 60 Minuten
 * target = tägliche Erhöhung, secondaryTarget = maximales Ziel
 */
export const createIncreaseDailyGoal = (
  description: string,
  variableReference: FieldKeyEnum | string,
  dailyIncrease: number,
  targetValue: number,
  period: GoalPeriodTypeEnum
): Goal => {
  return new Goal({
    description,
    variableReference: variableReference as string,
    type: GoalTypeEnum.IncreaseDaily,
    target: dailyIncrease,
    period,
    secondaryTarget: targetValue,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  });
};

/**
 * DecreaseDaily: Ziel - Täglich x weniger bis zu bestimmtem Ziel
 * Beispiel: Täglich 5 Minuten weniger am Handy bis 30 Minuten
 * target = tägliche Abnahme, secondaryTarget = minimales Ziel
 */
export const createDecreaseDailyGoal = (
  description: string,
  variableReference: FieldKeyEnum | string,
  dailyDecrease: number,
  targetValue: number,
  period: GoalPeriodTypeEnum
): Goal => {
  return new Goal({
    description,
    variableReference: variableReference as string,
    type: GoalTypeEnum.DecreaseDaily,
    target: dailyDecrease,
    period,
    secondaryTarget: targetValue,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  });
};

/**
 * AverageAbove: Ziel - Durchschnitt soll über x sein
 * Beispiel: Durchschnittliche Stimmung pro Woche über 7 (1-10 Skala)
 */
export const createAverageAboveGoal = (
  description: string,
  variableReference: FieldKeyEnum | string,
  minAverage: number,
  period: GoalPeriodTypeEnum
): Goal => {
  return new Goal({
    description,
    variableReference: variableReference as string,
    type: GoalTypeEnum.AverageAbove,
    target: minAverage,
    period,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  });
};

/**
 * AverageBelow: Ziel - Durchschnitt soll unter x sein
 * Beispiel: Durchschnittlicher Stresslevel unter 4 (1-10 Skala)
 */
export const createAverageBelowGoal = (
  description: string,
  variableReference: FieldKeyEnum | string,
  maxAverage: number,
  period: GoalPeriodTypeEnum
): Goal => {
  return new Goal({
    description,
    variableReference: variableReference as string,
    type: GoalTypeEnum.AverageBelow,
    target: maxAverage,
    period,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  });
};

/**
 * ConditionalTarget: Ziel - x schaffen unter der Bedingung y
 * Beispiel: 10km bei Temperatur unter 20°C joggen
 * target = Hauptzielwert, secondaryTarget = Bedingungswert, secondaryReference = Bedingungsfeld
 */
export const createConditionalTargetGoal = (
  description: string,
  variableReference: FieldKeyEnum | string,
  targetValue: number,
  conditionField: FieldKeyEnum | string,
  conditionValue: number,
  period: GoalPeriodTypeEnum
): Goal => {
  return new Goal({
    description,
    variableReference: variableReference as string,
    type: GoalTypeEnum.ConditionalTarget,
    target: targetValue,
    period,
    secondaryTarget: conditionValue,
    secondaryReference: conditionField as string,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  });
};

