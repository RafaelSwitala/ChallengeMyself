export enum GoalTypeEnum {
  MoreThan = "more_than", // a) Mehr als...
  LessThan = "less_than", // b) Weniger als...
  Avoid = "avoid", // c) Ganz vermeiden
  FrequencyExact = "frequency_exact", // d) x-Mal pro Woche/Monat
  FrequencyMax = "frequency_max", // e) Maximal x mal in der Woche/Monat
  FrequencyMin = "frequency_min", // f) Mindestens x mal in der Woche/Monat
  Streak = "streak", // g) Streak (x mal in Folge Ziel erreicht)
  IncreaseDaily = "increase_daily", // h) Täglich x mehr bis zu bestimmtem Ziel
  DecreaseDaily = "decrease_daily", // i) Täglich x weniger bis zu bestimmtem Ziel
  AverageAbove = "average_above", // j) Durchschnitt soll über x sein
  AverageBelow = "average_below", // k) Durchschnitt soll unter x sein
  ConditionalTarget = "conditional_target", // l) x schaffen unter der Bedingung y
}
