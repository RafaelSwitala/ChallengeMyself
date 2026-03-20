import logging
from typing import Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class Goal:    
    def __init__(
        self,
        description: str,
        target: float,
        period: str,
        reference: Optional[str] = None
    ):
        self.description = description
        self.target = target
        self.period = period
        self.reference = reference

    def to_dict(self):
        try:
            result = {
                "description": self.description,
                "target": self.target,
                "period": self.period
            }
            if self.reference:
                result["reference"] = self.reference
            return result
        except Exception:
            logger.exception("Failed to serialize Goal")
            return {}

    @staticmethod
    def from_dict(data: dict):
        try:
            return Goal(
                description=data.get("description", ""),
                target=data.get("target"),
                period=data.get("period", ""),
                reference=data.get("reference")
            )
        except Exception:
            logger.exception("Failed to deserialize Goal from dict")
            return None
            return {}
