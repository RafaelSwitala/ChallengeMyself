"""
Field Model Module

Defines the Field dataclass for describing activity data fields.
Fields define what data can be recorded for each session of an activity.
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Field:
    """
    Represents a data field in an activity session.
    
    Fields describe:
    - Name: The field identifier (e.g., "distance_km")
    - Type: Data type (number, text, enum, date)
    - Unit: Display unit (km, minutes, etc.)
    - Values: For enum fields, list of allowed values
    
    """
    
    name: str
    type: str
    unit: Optional[str] = None
    values: Optional[List[str]] = None
