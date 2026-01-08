from models.session import Session
from models.goal import Goal
from models.activities import ACTIVITIES

class Challenge:
    def __init__(self, name: str):
        if name not in ACTIVITIES:
            raise ValueError(f"Unknown activity {name}")
        
        self.name = name
        self.sessions: list[Session] = []
        self.goal: Goal | None = None
        self.allowed_keys = ACTIVITIES[name]

    def add_session(self, session: Session):
        filtered_values = {k: v for k, v in session.values.items() if k in self.allowed_keys}
        session.values = filtered_values
        self.sessions.append(session)

    def set_goal(self, goal: Goal):
        self.goal = goal

    def to_dict(self):
        return {
            "name": self.name,
            "goal": self.goal.to_dict() if self.goal else None,
            "sessions": [s.to_dict() for s in self.sessions]
        }
