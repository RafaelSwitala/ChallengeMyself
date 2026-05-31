import { GoalPeriodTypeEnum } from "../../enums/GoalPeriodTypeEnum";
import { GoalTypeEnum } from "../../enums/GoalTypeEnum";
import { Goal } from "../../models/GoalClass";
import { Session } from "../../models/SessionClass";
import { calculateCurrentStreak } from "../calculations/streakCalculator";

/**
 * Interface für das Evaluierungsergebnis eines Goals
 */
export interface GoalEvaluationResult {
  goal: Goal;
  isAchieved: boolean;
  progress: number; // 0-100%
  currentValue: number;
  targetValue: number;
  remainingValue: number;
  message: string;
  details?: any;
}

/**
 * Hauptfunktion zur Evaluierung eines Goals
 */
export const evaluateGoal = (
  goal: Goal,
  sessions: Session[],
  periodSessions?: Session[] // Sessions für die aktuelle Periode, falls vorgefiltert
): GoalEvaluationResult => {
  const sessionsToEvaluate = periodSessions || filterSessionsByPeriod(sessions, goal.period);

  switch (goal.type) {
    case GoalTypeEnum.MoreThan:
      return evaluateMoreThan(goal, sessionsToEvaluate);
    case GoalTypeEnum.LessThan:
      return evaluateLessThan(goal, sessionsToEvaluate);
    case GoalTypeEnum.Avoid:
      return evaluateAvoid(goal, sessionsToEvaluate);
    case GoalTypeEnum.FrequencyExact:
      return evaluateFrequencyExact(goal, sessionsToEvaluate);
    case GoalTypeEnum.FrequencyMax:
      return evaluateFrequencyMax(goal, sessionsToEvaluate);
    case GoalTypeEnum.FrequencyMin:
      return evaluateFrequencyMin(goal, sessionsToEvaluate);
    case GoalTypeEnum.Streak:
      return evaluateStreak(goal, sessions);
    case GoalTypeEnum.IncreaseDaily:
      return evaluateIncreaseDaily(goal, sessionsToEvaluate);
    case GoalTypeEnum.DecreaseDaily:
      return evaluateDecreaseDaily(goal, sessionsToEvaluate);
    case GoalTypeEnum.AverageAbove:
      return evaluateAverageAbove(goal, sessionsToEvaluate);
    case GoalTypeEnum.AverageBelow:
      return evaluateAverageBelow(goal, sessionsToEvaluate);
    case GoalTypeEnum.ConditionalTarget:
      return evaluateConditionalTarget(goal, sessionsToEvaluate);
    default:
      return createFailedResult(goal, 0, 0, "Goal-Typ nicht bekannt");
  }
};

/**
 * MoreThan: Prüft, ob die Summe > target ist
 */
const evaluateMoreThan = (goal: Goal, sessions: Session[]): GoalEvaluationResult => {
  const sum = sumFieldValues(sessions, goal.variableReference);
  const isAchieved = sum > goal.target;
  const progress = Math.min((sum / goal.target) * 100, 100);

  return {
    goal,
    isAchieved,
    progress,
    currentValue: sum,
    targetValue: goal.target,
    remainingValue: Math.max(goal.target - sum, 0),
    message: isAchieved
      ? `✓ Ziel erreicht: ${sum.toFixed(2)} von ${goal.target}`
      : `${sum.toFixed(2)} von ${goal.target} erreicht, noch ${Math.max(goal.target - sum, 0).toFixed(2)} zu gehen`,
  };
};

/**
 * LessThan: Prüft, ob die Summe < target ist
 */
const evaluateLessThan = (goal: Goal, sessions: Session[]): GoalEvaluationResult => {
  const sum = sumFieldValues(sessions, goal.variableReference);
  const isAchieved = sum < goal.target;
  const progress = Math.min((sum / goal.target) * 100, 100);

  return {
    goal,
    isAchieved,
    progress,
    currentValue: sum,
    targetValue: goal.target,
    remainingValue: Math.max(sum - goal.target, 0),
    message: isAchieved
      ? `✓ Ziel erreicht: ${sum.toFixed(2)} unter ${goal.target}`
      : `${sum.toFixed(2)} überschreitet Limit von ${goal.target} um ${(sum - goal.target).toFixed(2)}`,
  };
};

/**
 * Avoid: Prüft, ob keine Sessions vorhanden sind
 */
const evaluateAvoid = (goal: Goal, sessions: Session[]): GoalEvaluationResult => {
  const isAchieved = sessions.length === 0;
  const progress = isAchieved ? 100 : 0;

  return {
    goal,
    isAchieved,
    progress,
    currentValue: sessions.length,
    targetValue: 0,
    remainingValue: sessions.length,
    message: isAchieved
      ? "✓ Ziel erreicht: Diese Aktivität wurde nicht durchgeführt"
      : `${sessions.length} Aktivitäten durchgeführt, sollte vermieden werden`,
  };
};

/**
 * FrequencyExact: Prüft, ob exakt target Sessions vorhanden sind
 */
const evaluateFrequencyExact = (goal: Goal, sessions: Session[]): GoalEvaluationResult => {
  const count = sessions.length;
  const isAchieved = count === goal.target;
  const progress = count === 0 ? 0 : Math.min((count / goal.target) * 100, 100);

  return {
    goal,
    isAchieved,
    progress,
    currentValue: count,
    targetValue: goal.target,
    remainingValue: Math.abs(goal.target - count),
    message: isAchieved
      ? `✓ Ziel erreicht: Exakt ${count}x durchgeführt`
      : `${count} von ${goal.target}x durchgeführt`,
  };
};

/**
 * FrequencyMax: Prüft, ob Sessions <= target sind
 */
const evaluateFrequencyMax = (goal: Goal, sessions: Session[]): GoalEvaluationResult => {
  const count = sessions.length;
  const isAchieved = count <= goal.target;
  const progress = Math.min((count / goal.target) * 100, 100);

  return {
    goal,
    isAchieved,
    progress,
    currentValue: count,
    targetValue: goal.target,
    remainingValue: Math.max(count - goal.target, 0),
    message: isAchieved
      ? `✓ Ziel erreicht: Maximal ${count} Sessions`
      : `${count} Sessions überschreitet Limit von ${goal.target} um ${count - goal.target}`,
  };
};

/**
 * FrequencyMin: Prüft, ob Sessions >= target sind
 */
const evaluateFrequencyMin = (goal: Goal, sessions: Session[]): GoalEvaluationResult => {
  const count = sessions.length;
  const isAchieved = count >= goal.target;
  const progress = (count / goal.target) * 100;

  return {
    goal,
    isAchieved,
    progress: Math.min(progress, 100),
    currentValue: count,
    targetValue: goal.target,
    remainingValue: Math.max(goal.target - count, 0),
    message: isAchieved
      ? `✓ Ziel erreicht: ${count}x durchgeführt`
      : `${count} von ${goal.target}x durchgeführt, noch ${goal.target - count}x zu gehen`,
  };
};

/**
 * Streak: Prüft die aktuelle Streak (benötigt streakCalculator)
 */
const evaluateStreak = (goal: Goal, sessions: Session[]): GoalEvaluationResult => {
  const currentStreak = calculateCurrentStreak(sessions, goal.variableReference);
  const isAchieved = currentStreak >= goal.target;
  const progress = (currentStreak / goal.target) * 100;

  return {
    goal,
    isAchieved,
    progress: Math.min(progress, 100),
    currentValue: currentStreak,
    targetValue: goal.target,
    remainingValue: Math.max(goal.target - currentStreak, 0),
    message: isAchieved
      ? `✓ Streak erreicht: ${currentStreak} Tage hintereinander`
      : `${currentStreak} von ${goal.target} Tagen erreicht, noch ${goal.target - currentStreak} Tage zu gehen`,
    details: { currentStreak },
  };
};

/**
 * IncreaseDaily: Prüft, ob die Werte täglich steigen
 */
const evaluateIncreaseDaily = (goal: Goal, sessions: Session[]): GoalEvaluationResult => {
  const values = getFieldValuesWithDates(sessions, goal.variableReference);
  const target = goal.secondaryTarget || goal.target;
  const dailyIncrease = goal.target;

  if (values.length === 0) {
    return createFailedResult(goal, 0, target, "Keine Daten vorhanden");
  }

  // Sortiere nach Datum
  values.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  // Prüfe, ob die Werte kontinuierlich steigen
  let previousValue = values[0].value;
  let consistentIncreases = 0;

  for (let i = 1; i < values.length; i++) {
    const currentValue = values[i].value;
    if (currentValue >= previousValue + dailyIncrease) {
      consistentIncreases++;
      previousValue = currentValue;
    } else {
      break;
    }
  }

  const currentValue = values[values.length - 1].value;
  const isAchieved = currentValue >= target;
  const progress = Math.min((currentValue / target) * 100, 100);

  return {
    goal,
    isAchieved,
    progress,
    currentValue,
    targetValue: target,
    remainingValue: Math.max(target - currentValue, 0),
    message: isAchieved
      ? `✓ Ziel erreicht: ${currentValue.toFixed(2)} erreicht (Ziel: ${target})`
      : `${currentValue.toFixed(2)} von ${target} erreicht`,
    details: { consistentIncreases, daysDataCollected: values.length },
  };
};

/**
 * DecreaseDaily: Prüft, ob die Werte täglich sinken
 */
const evaluateDecreaseDaily = (goal: Goal, sessions: Session[]): GoalEvaluationResult => {
  const values = getFieldValuesWithDates(sessions, goal.variableReference);
  const target = goal.secondaryTarget || goal.target;
  const dailyDecrease = goal.target;

  if (values.length === 0) {
    return createFailedResult(goal, 0, target, "Keine Daten vorhanden");
  }

  // Sortiere nach Datum
  values.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  // Prüfe, ob die Werte kontinuierlich sinken
  let previousValue = values[0].value;
  let consistentDecreases = 0;

  for (let i = 1; i < values.length; i++) {
    const currentValue = values[i].value;
    if (currentValue <= previousValue - dailyDecrease) {
      consistentDecreases++;
      previousValue = currentValue;
    } else {
      break;
    }
  }

  const currentValue = values[values.length - 1].value;
  const isAchieved = currentValue <= target;
  const progress = Math.min((currentValue / target) * 100, 100);

  return {
    goal,
    isAchieved,
    progress,
    currentValue,
    targetValue: target,
    remainingValue: Math.max(currentValue - target, 0),
    message: isAchieved
      ? `✓ Ziel erreicht: ${currentValue.toFixed(2)} erreicht (Ziel: ${target})`
      : `${currentValue.toFixed(2)} unter Ziel von ${target}`,
    details: { consistentDecreases, daysDataCollected: values.length },
  };
};

/**
 * AverageAbove: Prüft, ob Durchschnitt > target ist
 */
const evaluateAverageAbove = (goal: Goal, sessions: Session[]): GoalEvaluationResult => {
  const values = getFieldValues(sessions, goal.variableReference);

  if (values.length === 0) {
    return createFailedResult(goal, 0, goal.target, "Keine Daten vorhanden");
  }

  const average = values.reduce((a, b) => a + b, 0) / values.length;
  const isAchieved = average > goal.target;
  const progress = (average / goal.target) * 100;

  return {
    goal,
    isAchieved,
    progress: Math.min(progress, 100),
    currentValue: average,
    targetValue: goal.target,
    remainingValue: Math.max(goal.target - average, 0),
    message: isAchieved
      ? `✓ Ziel erreicht: Durchschnitt ${average.toFixed(2)} über ${goal.target}`
      : `Durchschnitt ${average.toFixed(2)}, Ziel: ${goal.target}`,
  };
};

/**
 * AverageBelow: Prüft, ob Durchschnitt < target ist
 */
const evaluateAverageBelow = (goal: Goal, sessions: Session[]): GoalEvaluationResult => {
  const values = getFieldValues(sessions, goal.variableReference);

  if (values.length === 0) {
    return createFailedResult(goal, 0, goal.target, "Keine Daten vorhanden");
  }

  const average = values.reduce((a, b) => a + b, 0) / values.length;
  const isAchieved = average < goal.target;
  const progress = Math.min((average / goal.target) * 100, 100);

  return {
    goal,
    isAchieved,
    progress,
    currentValue: average,
    targetValue: goal.target,
    remainingValue: Math.max(average - goal.target, 0),
    message: isAchieved
      ? `✓ Ziel erreicht: Durchschnitt ${average.toFixed(2)} unter ${goal.target}`
      : `Durchschnitt ${average.toFixed(2)}, Ziel: unter ${goal.target}`,
  };
};

/**
 * ConditionalTarget: Prüft, ob target unter Bedingung erfüllt ist
 */
const evaluateConditionalTarget = (goal: Goal, sessions: Session[]): GoalEvaluationResult => {
  // Filtere Sessions, die die Bedingung erfüllen
  const filteredSessions = sessions.filter(session => {
    const conditionValue = session.values[goal.secondaryReference!];
    if (conditionValue === null || conditionValue === undefined) return false;
    // Beispiel: Bedingung ist "Temperatur < 20"
    return conditionValue <= goal.secondaryTarget!;
  });

  const sum = sumFieldValues(filteredSessions, goal.variableReference);
  const isAchieved = sum >= goal.target;
  const progress = Math.min((sum / goal.target) * 100, 100);

  return {
    goal,
    isAchieved,
    progress,
    currentValue: sum,
    targetValue: goal.target,
    remainingValue: Math.max(goal.target - sum, 0),
    message: isAchieved
      ? `✓ Ziel erreicht: ${sum.toFixed(2)} unter Bedingung`
      : `${sum.toFixed(2)} von ${goal.target} unter Bedingung`,
    details: { sessionsMatchingCondition: filteredSessions.length },
  };
};

/**
 * Hilfsfunktionen
 */

/**
 * Summiert die Werte eines Fields über alle Sessions
 */
function sumFieldValues(sessions: Session[], fieldKey: string): number {
  return sessions.reduce((sum, session) => {
    const value = session.values[fieldKey];
    if (value === null || value === undefined || value === "") return sum;
    const num = typeof value === "number" ? value : parseFloat(value);
    return sum + (isNaN(num) ? 0 : num);
  }, 0);
}

/**
 * Gibt alle Werte eines Fields aus Sessions zurück
 */
function getFieldValues(sessions: Session[], fieldKey: string): number[] {
  return sessions
    .map(session => session.values[fieldKey])
    .filter(value => value !== null && value !== undefined && value !== "")
    .map(value => {
      const num = typeof value === "number" ? value : parseFloat(value);
      return isNaN(num) ? null : num;
    })
    .filter((value): value is number => value !== null);
}

/**
 * Gibt Werte mit Daten zurück
 */
function getFieldValuesWithDates(
  sessions: Session[],
  fieldKey: string
): Array<{ date: string; value: number }> {
  return sessions
    .map(session => ({
      date: session.date,
      value: session.values[fieldKey],
    }))
    .filter(item => item.value !== null && item.value !== undefined && item.value !== "")
    .map(item => {
      const num = typeof item.value === "number" ? item.value : parseFloat(item.value);
      return isNaN(num) ? null : { date: item.date, value: num };
    })
    .filter((item): item is { date: string; value: number } => item !== null);
}

/**
 * Filtert Sessions nach Periode
 */
function filterSessionsByPeriod(sessions: Session[], period: GoalPeriodTypeEnum): Session[] {
  const now = new Date();
  let startDate = new Date();

  switch (period) {
    case GoalPeriodTypeEnum.Daily:
      startDate.setHours(0, 0, 0, 0);
      break;
    case GoalPeriodTypeEnum.Weekly:
      startDate.setDate(now.getDate() - now.getDay());
      startDate.setHours(0, 0, 0, 0);
      break;
    case GoalPeriodTypeEnum.Monthly:
      startDate.setDate(1);
      startDate.setHours(0, 0, 0, 0);
      break;
    case GoalPeriodTypeEnum.Yearly:
      startDate.setMonth(0, 1);
      startDate.setHours(0, 0, 0, 0);
      break;
  }

  return sessions.filter(session => new Date(session.date) >= startDate);
}

/**
 * Hilfsfunktion für gescheiterte Evaluierungen
 */
function createFailedResult(
  goal: Goal,
  currentValue: number,
  targetValue: number,
  message: string
): GoalEvaluationResult {
  return {
    goal,
    isAchieved: false,
    progress: 0,
    currentValue,
    targetValue,
    remainingValue: targetValue - currentValue,
    message,
  };
}
