from models.session import Session
from models.goal import Goal
from models.activities import ACTIVITIES


class Challenge:
    def __init__(self, name: str, activity_type: str):
        if activity_type not in ACTIVITIES:
            raise ValueError(f"Unknown activity type {activity_type}")

        self.name = name
        self.activity_type = activity_type
        self.sessions: list[Session] = []
        self.goal: Goal | None = None
        self.allowed_keys = ACTIVITIES[activity_type]

    def add_session(self, session: Session):
        filtered = {k: session.values.get(k) for k in self.allowed_keys}
        session.values = filtered
        self.sessions.append(session)
        self.sessions.sort(key=lambda s: (s.date, s.time))

    def set_goal(self, goal: Goal):
        self.goal = goal

    def to_dict(self):
        return {
            "name": self.name,
            "activity_type": self.activity_type,
            "goal": self.goal.to_dict() if self.goal else None,
            "sessions": [s.to_dict() for s in self.sessions],
        }
