"""
Goal Model Module

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
    
    Goals provide motivation by defining:
    - Description: Human-readable goal description
    - Reference: Which metric to track (e.g., 'distance_km', 'duration_min')
    - Target: Target value to achieve
    - Period: Time period for goal (daily, weekly, monthly, date range, etc.)
    
    Attributes:
        description (str): Human-readable goal description
        reference (str): Field reference to track (e.g., 'distance_km')
        target (float): Target value to achieve
        period (str): Time period (daily, weekly, monthly, from_to, yearly, etc.)
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
        
        Args:
            description (str): Goal description (e.g., "Run 10km daily")
            target (float): Target value
            period (str): Time period (e.g., "daily", "weekly", "monthly", "2026-01-01_2026-01-31")
            reference (Optional[str]): Field reference to track (e.g., 'distance_km')
        """
        self.description = description
        self.target = target
        self.period = period
        self.reference = reference

    def to_dict(self):
        """
        Convert goal to dictionary for JSON serialization.
        
        Returns:
            Dict: Goal data with description, reference, target, and period
            
        Raises:
            Exception: Caught and logged if serialization fails
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
        
        Args:
            data (dict): Dictionary with goal data
            
        Returns:
            Goal: Goal object constructed from dictionary
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
