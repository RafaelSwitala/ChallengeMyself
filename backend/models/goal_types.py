"""
GoalType Implementierungen für verschiedene Aktivitäten
Jeder GoalType definiert die Struktur und Validierung für ein spezifisches Ziel
"""

import logging
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DayOfWeek(Enum):
    MONDAY = "Montag"
    TUESDAY = "Dienstag"
    WEDNESDAY = "Mittwoch"
    THURSDAY = "Donnerstag"
    FRIDAY = "Freitag"
    SATURDAY = "Samstag"
    SUNDAY = "Sonntag"


@dataclass
class GoalType:
    """Basis-Klasse für GoalTypes"""
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialisiert den GoalType zu einem Dictionary"""
        raise NotImplementedError
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GoalType':
        """Deserialisiert einen GoalType aus einem Dictionary"""
        raise NotImplementedError
    
    def is_valid(self) -> bool:
        """Prüft, ob dieser GoalType gültig ist"""
        raise NotImplementedError


@dataclass
class MoreThanGoal(GoalType):
    """
    MORE_THAN Goal: Gesamtkumulativ über Periode
    Beispiel: 120 km joggen in einem Monat (aufsummiert)
    """
    target_value: float
    period: str  # "daily", "weekly", "monthly", "yearly"
    unit: str  # z.B. "km", "minutes"
    metric: str  # z.B. "distance", "duration" - welche Metrik aus der Session
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "MORE_THAN",
            "target_value": self.target_value,
            "period": self.period,
            "unit": self.unit,
            "metric": self.metric,
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'MoreThanGoal':
        return MoreThanGoal(
            target_value=data.get("target_value", 0),
            period=data.get("period", "monthly"),
            unit=data.get("unit", ""),
            metric=data.get("metric", ""),
        )
    
    def is_valid(self) -> bool:
        return (
            self.target_value > 0
            and self.period in ["daily", "weekly", "monthly", "yearly"]
            and self.unit != ""
            and self.metric != ""
        )


@dataclass
class FrequencyMinGoal(GoalType):
    """
    FREQUENCY_MIN Goal: Mindestens X Sessions pro Periode
    Beispiel: Mindestens 3 Sessions pro Woche oder 20 Sessions pro Monat
    """
    min_sessions: int
    period: str  # "daily", "weekly", "monthly", "yearly"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "FREQUENCY_MIN",
            "min_sessions": self.min_sessions,
            "period": self.period,
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'FrequencyMinGoal':
        return FrequencyMinGoal(
            min_sessions=data.get("min_sessions", 0),
            period=data.get("period", "weekly"),
        )
    
    def is_valid(self) -> bool:
        return (
            self.min_sessions > 0
            and self.period in ["daily", "weekly", "monthly", "yearly"]
        )


@dataclass
class AverageAboveGoal(GoalType):
    """
    AVERAGE_ABOVE Goal: Durchschnittswert pro Session muss über Wert sein
    Beispiel: Durchschnittliche Duration pro Session über 30 min
    """
    target_average: float
    metric: str  # z.B. "duration", "distance", "speed"
    unit: str  # z.B. "minutes", "km", "km/h"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "AVERAGE_ABOVE",
            "target_average": self.target_average,
            "metric": self.metric,
            "unit": self.unit,
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AverageAboveGoal':
        return AverageAboveGoal(
            target_average=data.get("target_average", 0),
            metric=data.get("metric", ""),
            unit=data.get("unit", ""),
        )
    
    def is_valid(self) -> bool:
        return (
            self.target_average > 0
            and self.metric != ""
            and self.unit != ""
        )


@dataclass
class RecurrencePatternGoal(GoalType):
    """
    RECURRENCE_PATTERN Goal: An bestimmten Wochentagen trainieren
    Beispiel: Jeden Dienstag, Mittwoch und Samstag joggen
    """
    days_of_week: List[str]  # z.B. ["Dienstag", "Mittwoch", "Samstag"]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "RECURRENCE_PATTERN",
            "days_of_week": self.days_of_week,
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'RecurrencePatternGoal':
        return RecurrencePatternGoal(
            days_of_week=data.get("days_of_week", []),
        )
    
    def is_valid(self) -> bool:
        valid_days = [day.value for day in DayOfWeek]
        return (
            len(self.days_of_week) > 0
            and all(day in valid_days for day in self.days_of_week)
        )


def deserialize_goal_type(data: Dict[str, Any]) -> Optional[GoalType]:
    """
    Deserialisiert einen GoalType basierend auf dem 'type' Feld
    """
    if not data or "type" not in data:
        return None
    
    goal_type = data.get("type")
    
    try:
        if goal_type == "MORE_THAN":
            return MoreThanGoal.from_dict(data)
        elif goal_type == "FREQUENCY_MIN":
            return FrequencyMinGoal.from_dict(data)
        elif goal_type == "AVERAGE_ABOVE":
            return AverageAboveGoal.from_dict(data)
        elif goal_type == "RECURRENCE_PATTERN":
            return RecurrencePatternGoal.from_dict(data)
        else:
            logger.warning(f"Unknown goal type: {goal_type}")
            return None
    except Exception:
        logger.exception(f"Failed to deserialize goal type: {goal_type}")
        return None
