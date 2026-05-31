import { Session } from "../../models/SessionClass";

/**
 * Interface für Streak-Informationen
 */
export interface StreakInfo {
  currentStreak: number; // Aktuelle Streaks (Tage in Folge)
  longestStreak: number; // Längste bisherige Streak
  allStreaks: number[]; // Alle aufgezeichneten Streaks
  lastSessionDate?: string; // Datum der letzten Session
  isContinued: boolean; // Wird die aktuelle Streak noch fortgesetzt?
}

/**
 * Berechnet die aktuelle Streak (wie viele Tage in Folge eine Aktivität durchgeführt wurde)
 * @param sessions Alle Sessions
 * @param fieldKey Falls angegeben, wird nur nach Sessions mit Wert in diesem Field gesucht
 * @returns Anzahl der Tage in Folge
 */
export const calculateCurrentStreak = (
  sessions: Session[],
  fieldKey?: string
): number => {
  if (sessions.length === 0) return 0;

  // Sortiere Sessions nach Datum (aufsteigend)
  const sortedSessions = [...sessions].sort((a, b) => {
    return new Date(a.date).getTime() - new Date(b.date).getTime();
  });

  // Filtere falls fieldKey angegeben
  const filteredSessions = fieldKey
    ? sortedSessions.filter(s => s.values[fieldKey] !== null && s.values[fieldKey] !== undefined)
    : sortedSessions;

  if (filteredSessions.length === 0) return 0;

  // Starte von der letzten Session rückwärts
  let streak = 0;
  let lastDate = new Date(filteredSessions[filteredSessions.length - 1].date);

  for (let i = filteredSessions.length - 1; i >= 0; i--) {
    const currentDate = new Date(filteredSessions[i].date);
    const daysDifference = (lastDate.getTime() - currentDate.getTime()) / (1000 * 60 * 60 * 24);

    // Wenn die Differenz höchstens 1 Tag ist, zähle es zur Streak
    if (daysDifference <= 1) {
      streak++;
      lastDate = currentDate;
    } else {
      break;
    }
  }

  return streak;
};

/**
 * Berechnet die längste bisherige Streak
 */
export const calculateLongestStreak = (sessions: Session[], fieldKey?: string): number => {
  if (sessions.length === 0) return 0;

  const sortedSessions = [...sessions].sort((a, b) => {
    return new Date(a.date).getTime() - new Date(b.date).getTime();
  });

  const filteredSessions = fieldKey
    ? sortedSessions.filter(s => s.values[fieldKey] !== null && s.values[fieldKey] !== undefined)
    : sortedSessions;

  if (filteredSessions.length === 0) return 0;

  let maxStreak = 1;
  let currentStreak = 1;

  for (let i = 1; i < filteredSessions.length; i++) {
    const previousDate = new Date(filteredSessions[i - 1].date);
    const currentDate = new Date(filteredSessions[i].date);
    const daysDifference = (currentDate.getTime() - previousDate.getTime()) / (1000 * 60 * 60 * 24);

    if (daysDifference <= 1) {
      currentStreak++;
      maxStreak = Math.max(maxStreak, currentStreak);
    } else {
      currentStreak = 1;
    }
  }

  return maxStreak;
};

/**
 * Prüft, ob die aktuelle Streak noch fortgesetzt wird (Session heute oder gestern)
 */
export const isStreakContinued = (sessions: Session[], fieldKey?: string): boolean => {
  if (sessions.length === 0) return false;

  const sortedSessions = [...sessions].sort((a, b) => {
    return new Date(b.date).getTime() - new Date(a.date).getTime();
  });

  const filteredSessions = fieldKey
    ? sortedSessions.filter(s => s.values[fieldKey] !== null && s.values[fieldKey] !== undefined)
    : sortedSessions;

  if (filteredSessions.length === 0) return false;

  const lastSessionDate = new Date(filteredSessions[0].date);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  lastSessionDate.setHours(0, 0, 0, 0);

  const daysDifference = (today.getTime() - lastSessionDate.getTime()) / (1000 * 60 * 60 * 24);

  // Streak ist aktiv, wenn die letzte Session heute oder gestern war
  return daysDifference <= 1;
};

/**
 * Gibt umfassende Streak-Informationen zurück
 */
export const getStreakInfo = (sessions: Session[], fieldKey?: string): StreakInfo => {
  const currentStreak = calculateCurrentStreak(sessions, fieldKey);
  const longestStreak = calculateLongestStreak(sessions, fieldKey);
  const isContinued = isStreakContinued(sessions, fieldKey);

  // Berechne alle Streaks
  const allStreaks = calculateAllStreaks(sessions, fieldKey);

  // Finde das Datum der letzten Session
  const sortedSessions = [...sessions].sort((a, b) => {
    return new Date(b.date).getTime() - new Date(a.date).getTime();
  });

  const lastSessionDate = sortedSessions.length > 0 ? sortedSessions[0].date : undefined;

  return {
    currentStreak,
    longestStreak,
    allStreaks,
    lastSessionDate,
    isContinued,
  };
};

/**
 * Berechnet alle Streaks (alle aufgezeichneten Streaks, getrennt durch Lücken)
 */
function calculateAllStreaks(sessions: Session[], fieldKey?: string): number[] {
  if (sessions.length === 0) return [];

  const sortedSessions = [...sessions].sort((a, b) => {
    return new Date(a.date).getTime() - new Date(b.date).getTime();
  });

  const filteredSessions = fieldKey
    ? sortedSessions.filter(s => s.values[fieldKey] !== null && s.values[fieldKey] !== undefined)
    : sortedSessions;

  if (filteredSessions.length === 0) return [];

  const streaks: number[] = [];
  let currentStreak = 1;

  for (let i = 1; i < filteredSessions.length; i++) {
    const previousDate = new Date(filteredSessions[i - 1].date);
    const currentDate = new Date(filteredSessions[i].date);
    const daysDifference = (currentDate.getTime() - previousDate.getTime()) / (1000 * 60 * 60 * 24);

    if (daysDifference <= 1) {
      currentStreak++;
    } else {
      streaks.push(currentStreak);
      currentStreak = 1;
    }
  }

  streaks.push(currentStreak);
  return streaks.sort((a, b) => b - a); // Sortiere absteigend
}
