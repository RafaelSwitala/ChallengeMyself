/**
 * Validiert, ob ein Wert innerhalb eines bestimmten Bereichs liegt
 */
export const isInRange = (value: number, min: number, max: number): boolean => {
  return value >= min && value <= max;
};

/**
 * Begrenzt einen Wert auf einen bestimmten Bereich
 */
export const clampValue = (value: number, min: number, max: number): number => {
  return Math.min(Math.max(value, min), max);
};

/**
 * Validiert, ob ein Wert auf einer Skala von 1 bis 10 liegt (Ganzzahl)
 */
export const validateScale1To10 = (value: number): boolean => {
  return Number.isInteger(value) && isInRange(value, 1, 10);
};

/**
 * Konvertiert einen Wert zu einer Ganzzahl auf einer Skala von 1 bis 10
 */
export const ensureIntegerScale1To10 = (value: number): number => {
  return clampValue(Math.round(value), 1, 10);
};

/**
 * Gibt alle Felder zurück, die eine Range-Skala (1-10) haben sollten
 */
export const getScaleFields = (): string[] => {
  return [
    "anxiety_level",
    "concentration_level",
    "conflict_level",
    "craving_intensity",
    "focus_level",
    "harmony_level",
    "hunger_level",
    "intensity_level",
    "main_mood",
    "mood_after",
    "mood_before",
    "mood_level",
    "motivation_level",
    "movement_intensity",
    "physical_discomfort",
    "physical_energy",
    "quality_level",
    "satiety_level",
    "satisfaction_level",
    "self_confidence",
    "sleep_quality",
    "stress_level",
    "success_level",
  ];
};

/**
 * Prüft, ob ein Field eine Range-Skala haben soll
 */
export const isScaleField = (fieldKey: string): boolean => {
  return getScaleFields().includes(fieldKey);
};
