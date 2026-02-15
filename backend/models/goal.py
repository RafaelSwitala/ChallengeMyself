"""
Defines the Goal class for representing challenge targets and motivation.
Enhanced with reference field to track specific metrics and time periods.
"""

import logging
from typing import Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class Goal:
    """
    Represents a target or goal for a challenge.
    
    """
    
    def __init__(
        self,
        description: str,
        target: float,
        period: str,
        reference: Optional[str] = None
    ):
        """
        Initialize a new Goal.
        
        """
        self.description = description
        self.target = target
        self.period = period
        self.reference = reference

    def to_dict(self):
        """
        Convert goal to dictionary for JSON serialization.
        
        """
        try:
            result = {
                "description": self.description,
                "target": self.target,
                "period": self.period
            }
            if self.reference:
                result["reference"] = self.reference
            return result
        except Exception:
            logger.exception("Failed to serialize Goal")
            return {}

    @staticmethod
    def from_dict(data: dict):
        """
        Create Goal from dictionary (for JSON deserialization).

        """
        try:
            return Goal(
                description=data.get("description", ""),
                target=data.get("target"),
                period=data.get("period", ""),
                reference=data.get("reference")
            )
        except Exception:
            logger.exception("Failed to deserialize Goal from dict")
            return None
            return {}
