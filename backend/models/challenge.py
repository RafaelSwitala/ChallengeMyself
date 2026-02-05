"""
Challenge Model Module

Defines the Challenge class for representing personal challenges/goals.
Each challenge tracks:
- Name: Human-readable challenge identifier
- Activity type: Category of activity (Running, Reading, etc.)
- Sessions: List of recorded activity sessions
- Goal: Optional target and motivation for the challenge
"""

import logging
from models.session import Session
from models.goal import Goal
from models.activities import get_fields

logger = logging.getLogger(__name__)


class Challenge:
    """
    Represents a personal challenge or goal.
    
    A challenge is a collection of sessions (activity records) for a specific
    activity type with an optional goal/target.
    
    Attributes:
        name (str): Unique challenge identifier
        activity_type (str): Type of activity (e.g., 'Laufen', 'Lernen')
        sessions (List[Session]): Recorded activity sessions
        goal (Optional[Goal]): Target for the challenge
        allowed_keys (List[str]): Valid field names for this activity type
    """
    
    def __init__(self, name: str, activity_type: str):
        """
        Initialize a new Challenge.
        
        Args:
            name (str): Unique challenge name
            activity_type (str): Activity type from ACTIVITIES registry
            
        Raises:
            Exception: Caught and logged if activity type is invalid
        """
        self.name = name
        self.activity_type = activity_type
        self.sessions: list[Session] = []
        self.goal: Goal | None = None

        # Get allowed field names for this activity type
        try:
            fields = get_fields(activity_type)
            self.allowed_keys = [f.name if hasattr(f, 'name') else f["name"] for f in fields]
        except Exception:
            logger.exception("Failed to initialize allowed keys")
            self.allowed_keys = []

    def add_session(self, session: Session):
        """
        Add a new session to the challenge.
        
        Validates that all session fields are allowed for this activity type,
        then sorts sessions chronologically by date and time.
        
        Args:
            session (Session): Session object to add
            
        Raises:
            Exception: Caught and logged if session addition fails
        """
        try:
            # Filter session values to only include allowed fields
            session.values = {
                k: v for k, v in session.values.items()
                if k in self.allowed_keys
            }
            self.sessions.append(session)
            # Keep sessions sorted by date and time for consistent ordering
            self.sessions.sort(key=lambda s: (s.date, s.time))
        except Exception:
            logger.exception("Failed to add session")

    def set_goal(self, goal: Goal):
        """
        Set or update the challenge goal.
        
        Args:
            goal (Goal): Goal object defining target and period
        """
        self.goal = goal

    def to_dict(self):
        try:
            return {
                "name": self.name,
                "activity_type": self.activity_type,
                "goal": self.goal.to_dict() if self.goal else None,
                "sessions": [s.to_dict() for s in self.sessions],
            }
        except Exception:
            logger.exception("Failed to serialize Challenge")
            return {}
