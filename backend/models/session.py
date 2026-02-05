"""
Session Model Module

Defines the Session class for representing individual activity records.
Each session captures a date, time, and measurement values for a specific activity.
"""

import logging

logger = logging.getLogger(__name__)


class Session:
    """
    Represents a single activity session record.
    
    A session records:
    - When the activity occurred (date and time)
    - What was measured (values dictionary)
    
    Attributes:
        date (str): Session date in YYYY-MM-DD format
        time (str): Session time in HH:MM format
        values (Dict): Measured values (e.g., {"distance_km": 5.2, "duration_min": 45})
    """
    
    def __init__(self, date: str, time: str, values: dict | None = None):
        """
        Initialize a new Session.
        
        Args:
            date (str): Date in YYYY-MM-DD format
            time (str): Time in HH:MM format
            values (Optional[Dict]): Measurement values, defaults to empty dict
        """
        self.date = date
        self.time = time
        self.values = values or {}

    def to_dict(self):
        """
        Convert session to dictionary for JSON serialization.
        
        Returns:
            Dict: Session data with date, time, and values
            
        Raises:
            Exception: Caught and logged if serialization fails
        """
        try:
            return {
                "date": self.date,
                "time": self.time,
                "values": self.values,
            }
        except Exception:
            logger.exception("Failed to serialize Session")
            return {}
