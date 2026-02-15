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
    """
    
    def __init__(self, date: str, time: str, values: dict | None = None):
        """
        Initialize a new Session.
        
        """
        self.date = date
        self.time = time
        self.values = values or {}

    def to_dict(self):
        """
        Convert session to dictionary for JSON serialization.
        
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
