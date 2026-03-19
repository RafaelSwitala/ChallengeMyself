import json
import os
import logging
from models.challenge import Challenge
from models.session import Session
from models.goal import Goal
from config import DATA_DIR

logger = logging.getLogger(__name__)


def _path(name: str):
    return os.path.join(DATA_DIR, f"{name}.json")


def save_challenge(challenge: Challenge):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(_path(challenge.name), "w", encoding="utf-8") as f:
            json.dump(challenge.to_dict(), f, indent=4, ensure_ascii=False)
    except Exception:
        logger.exception("Failed to save challenge %s", challenge.name)


def load_challenge(name: str) -> Challenge | None:
    try:
        path = _path(name)
        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        c = Challenge(data["name"], data["activity_type"])

        if data.get("goal"):
            g = data["goal"]
            c.set_goal(Goal(
                description=g["description"],
                target=g.get("target"),
                period=g.get("period", ""),
                reference=g.get("reference")
            ))

        for s in data.get("sessions", []):
            c.add_session(Session(s["date"], s["time"], s["values"]))

        return c

    except Exception:
        logger.exception("Failed to load challenge %s", name)
        return None


def list_challenges() -> list[dict]:
    challenges = []
    try:
        if not os.path.exists(DATA_DIR):
            return challenges

        for filename in os.listdir(DATA_DIR):
            if not filename.endswith(".json"):
                continue

            try:
                with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    challenges.append({
                        "id": filename.replace(".json", ""),
                        "name": data.get("name", "Unnamed"),
                        "activity_type": data.get("activity_type", "Unknown")
                    })
            except Exception:
                logger.warning(f"Failed to read challenge file: {filename}")
                continue

    except Exception:
        logger.exception("Failed to list challenges")

    return challenges
