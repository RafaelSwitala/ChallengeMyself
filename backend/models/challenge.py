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
            self.allowed_keys = [f["name"] for f in get_fields(activity_type)]
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
