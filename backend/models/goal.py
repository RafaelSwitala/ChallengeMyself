class Goal:
    def __init__(self, description: str, target: float, period: str):
        self.description = description
        self.target = target
        self.period = period  # "daily", "weekly", "monthly"

    def to_dict(self):
        return {
            "description": self.description,
            "target": self.target,
            "period": self.period
        }
