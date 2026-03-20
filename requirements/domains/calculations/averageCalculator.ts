import { FieldKeyEnum } from "../../enums/FieldKeyEnum";
import { Session } from "../../models/SessionClass";

/**
 * Optionen für Durchschnittsberechnungen
 */
export enum AveragePeriodEnum {
  Total = "total", // Gesamter Durchschnitt aller Werte
  Weekly = "weekly", // Wöchentlicher Durchschnitt (pro KW)
  Monthly = "monthly", // Monatlicher Durchschnitt (pro Monat)
  Custom = "custom", // Benutzerdefinierten Zeitraum
}

/**
 * Interface für einen durchschnittlichen Wert mit Periode
 */
export interface AveragePeriodValue {
  period: string; // z.B. "KW 5" oder "Januar" oder "2026-01-15 bis 2026-01-22"
  value: number;
  count: number; // Anzahl der Sessions in dieser Periode
}

/**
 * Interface für das Ergebnis einer Durchschnittsberechnung
 */
export interface AverageResult {
  fieldKey: FieldKeyEnum;
  period: AveragePeriodEnum;
  overallAverage: number;
  periodValues: AveragePeriodValue[];
  unit?: string;
}

/**
 * Berechnet den Durchschnitt eines FieldKeys aus allen Sessions
 */
export const calculateTotalAverage = (
  sessions: Session[],
  fieldKey: FieldKeyEnum | string,
  unit?: string
): AverageResult => {
  const values = sessions
    .map(session => session.values[fieldKey as string])
    .filter(value => value !== null && value !== undefined && value !== "")
    .map(value => {
      const num = typeof value === "number" ? value : parseFloat(value);
      return isNaN(num) ? null : num;
    })
    .filter((value): value is number => value !== null);

  const average = values.length > 0 ? values.reduce((a, b) => a + b, 0) / values.length : 0;

  return {
    fieldKey: fieldKey as FieldKeyEnum,
    period: AveragePeriodEnum.Total,
    overallAverage: average,
    periodValues: [
      {
        period: "Gesamt",
        value: average,
        count: values.length,
      },
    ],
    unit,
  };
};

/**
 * Berechnet den wöchentlichen Durchschnitt (gruppiert nach Kalenderwoche)
 */
export const calculateWeeklyAverage = (
  sessions: Session[],
  fieldKey: FieldKeyEnum | string,
  unit?: string
): AverageResult => {
  const weeklyGroups: Map<string, number[]> = new Map();

  sessions.forEach(session => {
    const value = session.values[fieldKey as string];
    if (value === null || value === undefined || value === "") return;

    const num = typeof value === "number" ? value : parseFloat(value);
    if (isNaN(num)) return;

    const date = new Date(session.date);
    const week = getCalendarWeek(date);
    const year = date.getFullYear();
    const key = `KW ${week} (${year})`;

    if (!weeklyGroups.has(key)) {
      weeklyGroups.set(key, []);
    }
    weeklyGroups.get(key)!.push(num);
  });

  const periodValues: AveragePeriodValue[] = Array.from(weeklyGroups.entries())
    .map(([period, values]) => ({
      period,
      value: values.reduce((a, b) => a + b, 0) / values.length,
      count: values.length,
    }))
    .sort((a, b) => a.period.localeCompare(b.period));

  const overallAverage =
    periodValues.length > 0
      ? periodValues.reduce((sum, pv) => sum + pv.value * pv.count, 0) /
        periodValues.reduce((sum, pv) => sum + pv.count, 0)
      : 0;

  return {
    fieldKey: fieldKey as FieldKeyEnum,
    period: AveragePeriodEnum.Weekly,
    overallAverage,
    periodValues,
    unit,
  };
};

/**
 * Berechnet den monatlichen Durchschnitt (gruppiert nach Monat)
 */
export const calculateMonthlyAverage = (
  sessions: Session[],
  fieldKey: FieldKeyEnum | string,
  unit?: string
): AverageResult => {
  const monthlyGroups: Map<string, number[]> = new Map();

  sessions.forEach(session => {
    const value = session.values[fieldKey as string];
    if (value === null || value === undefined || value === "") return;

    const num = typeof value === "number" ? value : parseFloat(value);
    if (isNaN(num)) return;

    const date = new Date(session.date);
    const monthName = getMonthName(date.getMonth());
    const year = date.getFullYear();
    const key = `${monthName} ${year}`;

    if (!monthlyGroups.has(key)) {
      monthlyGroups.set(key, []);
    }
    monthlyGroups.get(key)!.push(num);
  });

  const periodValues: AveragePeriodValue[] = Array.from(monthlyGroups.entries())
    .map(([period, values]) => ({
      period,
      value: values.reduce((a, b) => a + b, 0) / values.length,
      count: values.length,
    }))
    .sort((a, b) => {
      const dateA = new Date(a.period);
      const dateB = new Date(b.period);
      return dateA.getTime() - dateB.getTime();
    });

  const overallAverage =
    periodValues.length > 0
      ? periodValues.reduce((sum, pv) => sum + pv.value * pv.count, 0) /
        periodValues.reduce((sum, pv) => sum + pv.count, 0)
      : 0;

  return {
    fieldKey: fieldKey as FieldKeyEnum,
    period: AveragePeriodEnum.Monthly,
    overallAverage,
    periodValues,
    unit,
  };
};

/**
 * Berechnet den Durchschnitt für einen benutzerdefinierten Zeitraum
 */
export const calculateCustomPeriodAverage = (
  sessions: Session[],
  fieldKey: FieldKeyEnum | string,
  startDate: Date,
  endDate: Date,
  unit?: string
): AverageResult => {
  const filteredSessions = sessions.filter(session => {
    const date = new Date(session.date);
    return date >= startDate && date <= endDate;
  });

  const values = filteredSessions
    .map(session => session.values[fieldKey as string])
    .filter(value => value !== null && value !== undefined && value !== "")
    .map(value => {
      const num = typeof value === "number" ? value : parseFloat(value);
      return isNaN(num) ? null : num;
    })
    .filter((value): value is number => value !== null);

  const average = values.length > 0 ? values.reduce((a, b) => a + b, 0) / values.length : 0;

  const period = `${startDate.toLocaleDateString("de-DE")} bis ${endDate.toLocaleDateString(
    "de-DE"
  )}`;

  return {
    fieldKey: fieldKey as FieldKeyEnum,
    period: AveragePeriodEnum.Custom,
    overallAverage: average,
    periodValues: [
      {
        period,
        value: average,
        count: values.length,
      },
    ],
    unit,
  };
};

/**
 * Hilfsfunktion: Gibt die Kalenderwoche eines Datums zurück
 */
function getCalendarWeek(date: Date): number {
  const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
  const pastDaysOfYear = (date.getTime() - firstDayOfYear.getTime()) / 86400000;
  return Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7);
}

/**
 * Hilfsfunktion: Gibt den Monatsnamen auf Deutsch zurück
 */
function getMonthName(month: number): string {
  const months = [
    "Januar",
    "Februar",
    "März",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember",
  ];
  return months[month];
}
