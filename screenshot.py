"""
Challenge Model Module

Defines the Challenge class for representing personal challenges/goals.
Each challenge tracks:
- Name: Human-readable challenge identifier
- Activity type: Category of activity (Running, Reading, etc.)
- Sessions: List of recorded activity sessions
- Goal: Optional target with reference, value, and period
"""

import logging
from models.session import Session
from models.goal import Goal
from models.activities import get_fields

logger = logging.getLogger(__name__)











class Challenge:
    def __init__(self, name: str, activity_type: str):
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
        Set or update the challenge goal with reference field.
        
        Args:
            goal (Goal): Goal object with reference, target, and period
        """
        self.goal = goal

    def get_goal_progress(self, selected_date: str = None) -> dict:
        """
        Calculate current progress towards goal.
        
        Args:
            selected_date (str): Optional date filter in format:
                - YYYY-MM-DD for daily goals
                - YYYY-MM for monthly goals
        
        Returns goal progress with current value, status, and message.
        
        Returns:
            dict: Progress data if goal exists, None otherwise
        """
        if not self.goal or not self.goal.reference:
            return None
        
        try:
            from utils.goal_tracker import calculate_progress
            
            return calculate_progress(
                sessions=[s.to_dict() for s in self.sessions],
                goal_reference=self.goal.reference,
                goal_target=self.goal.target,
                goal_period=self.goal.period,
                activity_name=self.activity_type,
                selected_date=selected_date
            )
        except Exception:
            logger.exception("Failed to calculate goal progress")
            return None

    def to_dict(self):
        """
        Convert challenge to dictionary for JSON serialization.
        
        Returns:
            dict: Challenge data with name, activity type, goal, and sessions
            
        Raises:
            Exception: Caught and logged if serialization fails
        """
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
