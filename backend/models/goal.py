"""
Goal Model Module

Defines the Goal class for representing challenge targets and motivation.
"""

import logging

logger = logging.getLogger(__name__)


class Goal:
    """
    Represents a target or goal for a challenge.
    
    Goals provide motivation by defining:
    - What should be achieved (description)
    - How much (target value)
    - When to achieve it (period)
    
    Attributes:
        description (str): Human-readable goal description
        target (float): Target value to achieve
        period (str): Time period for goal (daily, weekly, monthly, etc.)
    """
    
    def __init__(self, description: str, target: float, period: str):
        """
        Initialize a new Goal.
        
        Args:
            description (str): Goal description (e.g., "Run 10km daily")
            target (float): Target value
            period (str): Time period (e.g., "daily", "weekly", "monthly")
        """
        self.description = description
        self.target = target
        self.period = period

    def to_dict(self):
        """
        Convert goal to dictionary for JSON serialization.
        
        Returns:
            Dict: Goal data with description, target, and period
            
        Raises:
            Exception: Caught and logged if serialization fails
        """
        try:
            return {
                "description": self.description,
                "target": self.target,
                "period": self.period
            }
        except Exception:
            logger.exception("Failed to serialize Goal")
            return {}
