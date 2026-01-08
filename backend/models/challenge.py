from models.session import Session
from models.goal import Goal

class Challenge:
    def __init__(self, name: str):
        self.name = name
        self.sessions: list[Session] = []
        self.goal: Goal | None = None

    def add_session(self, session: Session):
        self.sessions.append(session)

    def set_goal(self, goal: Goal):
        self.goal = goal

    def to_dict(self):
        return {
            "name": self.name,
            "goal": self.goal.to_dict() if self.goal else None,
            "sessions": [s.to_dict() for s in self.sessions]
        }
