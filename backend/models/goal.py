import logging

logger = logging.getLogger(__name__)


class Goal:
    def __init__(self, description: str, target: float, period: str):
        self.description = description
        self.target = target
        self.period = period

    def to_dict(self):
        try:
            return {
                "description": self.description,
                "target": self.target,
                "period": self.period
            }
        except Exception:
            logger.exception("Failed to serialize Goal")
            return {}
