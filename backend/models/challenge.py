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

        try:
            fields = get_fields(activity_type)
            self.allowed_keys = [f.name if hasattr(f, 'name') else f["name"] for f in fields]
        except Exception:
            logger.exception("Failed to initialize allowed keys")
            self.allowed_keys = []

    def add_session(self, session: Session):
        try:
            session.values = {
                k: v for k, v in session.values.items()
                if k in self.allowed_keys
            }
            self.sessions.append(session)
            self.sessions.sort(key=lambda s: (s.date, s.time))
        except Exception:
            logger.exception("Failed to add session")

    def set_goal(self, goal: Goal):
        self.goal = goal

    def get_goal_progress(self, selected_date: str = None) -> dict:
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
