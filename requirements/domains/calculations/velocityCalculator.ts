import { FieldKeyEnum } from "../../enums/FieldKeyEnum";
import { Session } from "../../models/SessionClass";

/**
 * Einheiten für Geschwindigkeitsberechnung
 */
export enum VelocityUnit {
  KmH = "km/h",
  MsH = "m/s",
  MilesPH = "mph",
}

/**
 * Interface für ein einzelnes Geschwindigkeitsergebnis
 */
export interface VelocityResult {
  sessionId: string;
  sessionDate: string;
  distance: number; // in km
  duration: number; // in Minuten
  velocity: number; // in der gewünschten Einheit
  unit: VelocityUnit;
}

/**
 * Interface für aggregierte Geschwindigkeitsergebnisse
 */
export interface VelocityStats {
  averageVelocity: number;
  maxVelocity: number;
  minVelocity: number;
  unit: VelocityUnit;
  results: VelocityResult[];
}

/**
 * Berechnet die Geschwindigkeit aus Distanz und Dauer
 * @param distance Distanz in km
 * @param duration Dauer in Minuten
 * @param unit Ausgabeeinheit (default: km/h)
 * @returns Geschwindigkeit in der gewünschten Einheit
 */
export const calculateVelocity = (
  distance: number,
  duration: number,
  unit: VelocityUnit = VelocityUnit.KmH
): number => {
  if (distance <= 0 || duration <= 0) {
    return 0;
  }

  // Berechne km/h
  const kmH = (distance / duration) * 60;

  // Konvertiere in die gewünschte Einheit
  switch (unit) {
    case VelocityUnit.MsH:
      return kmH / 3.6; // km/h zu m/s
    case VelocityUnit.MilesPH:
      return kmH / 1.60934; // km/h zu mph
    case VelocityUnit.KmH:
    default:
      return kmH;
  }
};

/**
 * Berechnet die Geschwindigkeit für eine einzelne Session
 */
export const calculateSessionVelocity = (
  session: Session,
  distanceFieldKey: FieldKeyEnum | string = FieldKeyEnum.Distance,
  durationFieldKey: FieldKeyEnum | string = FieldKeyEnum.Duration,
  unit: VelocityUnit = VelocityUnit.KmH
): VelocityResult | null => {
  const distance = session.values[distanceFieldKey as string];
  const duration = session.values[durationFieldKey as string];

  if (distance === null || distance === undefined || duration === null || duration === undefined) {
    return null;
  }

  const distanceNum = typeof distance === "number" ? distance : parseFloat(distance);
  const durationNum = typeof duration === "number" ? duration : parseFloat(duration);

  if (isNaN(distanceNum) || isNaN(durationNum) || distanceNum <= 0 || durationNum <= 0) {
    return null;
  }

  const velocity = calculateVelocity(distanceNum, durationNum, unit);

  return {
    sessionId: session.id,
    sessionDate: session.date,
    distance: distanceNum,
    duration: durationNum,
    velocity,
    unit,
  };
};

/**
 * Berechnet die Geschwindigkeiten für mehrere Sessions
 */
export const calculateMultipleSessionsVelocities = (
  sessions: Session[],
  distanceFieldKey: FieldKeyEnum | string = FieldKeyEnum.Distance,
  durationFieldKey: FieldKeyEnum | string = FieldKeyEnum.Duration,
  unit: VelocityUnit = VelocityUnit.KmH,
  limit?: number
): VelocityStats => {
  const results: VelocityResult[] = [];

  // Sortiere nach Datum (neueste zuerst)
  const sortedSessions = [...sessions].sort((a, b) => {
    return new Date(b.date).getTime() - new Date(a.date).getTime();
  });

  // Limitiere falls gewünscht
  const sessionsToProcess = limit ? sortedSessions.slice(0, limit) : sortedSessions;

  sessionsToProcess.forEach(session => {
    const result = calculateSessionVelocity(session, distanceFieldKey, durationFieldKey, unit);
    if (result) {
      results.push(result);
    }
  });

  // Berechne Statistiken
  if (results.length === 0) {
    return {
      averageVelocity: 0,
      maxVelocity: 0,
      minVelocity: 0,
      unit,
      results: [],
    };
  }

  const velocities = results.map(r => r.velocity);
  const averageVelocity = velocities.reduce((a, b) => a + b, 0) / velocities.length;
  const maxVelocity = Math.max(...velocities);
  const minVelocity = Math.min(...velocities);

  return {
    averageVelocity,
    maxVelocity,
    minVelocity,
    unit,
    results: results.sort((a, b) => new Date(b.sessionDate).getTime() - new Date(a.sessionDate).getTime()),
  };
};

/**
 * Berechnet die Geschwindigkeit für die letzten x Sessions
 */
export const calculateLastNSessionsVelocities = (
  sessions: Session[],
  n: number,
  distanceFieldKey: FieldKeyEnum | string = FieldKeyEnum.Distance,
  durationFieldKey: FieldKeyEnum | string = FieldKeyEnum.Duration,
  unit: VelocityUnit = VelocityUnit.KmH
): VelocityStats => {
  return calculateMultipleSessionsVelocities(
    sessions,
    distanceFieldKey,
    durationFieldKey,
    unit,
    n
  );
};

/**
 * Konvertiert Geschwindigkeit zwischen verschiedenen Einheiten
 */
export const convertVelocity = (
  velocity: number,
  fromUnit: VelocityUnit,
  toUnit: VelocityUnit
): number => {
  if (fromUnit === toUnit) return velocity;

  // Konvertiere zuerst zu km/h
  let kmH: number;
  switch (fromUnit) {
    case VelocityUnit.MsH:
      kmH = velocity * 3.6;
      break;
    case VelocityUnit.MilesPH:
      kmH = velocity * 1.60934;
      break;
    case VelocityUnit.KmH:
    default:
      kmH = velocity;
  }

  // Konvertiere von km/h zur Zieleinheit
  switch (toUnit) {
    case VelocityUnit.MsH:
      return kmH / 3.6;
    case VelocityUnit.MilesPH:
      return kmH / 1.60934;
    case VelocityUnit.KmH:
    default:
      return kmH;
  }
};
