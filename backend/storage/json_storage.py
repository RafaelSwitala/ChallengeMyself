import json, os
from models.challenge import Challenge
from models.session import Session
from models.goal import Goal
from config import DATA_DIR

def _path(name: str):
    return os.path.join(DATA_DIR, f"{name}.json")

def save_challenge(challenge: Challenge):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(_path(challenge.name), "w", encoding="utf-8") as f:
        json.dump(challenge.to_dict(), f, indent=4)

def load_challenge(name: str) -> Challenge | None:
    path = _path(name)
    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    c = Challenge(data["name"], data["activity_type"])

    if data["goal"]:
        g = data["goal"]
        c.set_goal(Goal(g["description"], g["target"], g["period"]))

    for s in data["sessions"]:
        c.add_session(Session(s["date"], s["time"], s["values"]))

    return c

def list_challenges() -> list[dict]:
    if not os.path.exists(DATA_DIR):
        return []

    challenges = []

    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".json"):
            continue

        with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
            data = json.load(f)

        challenges.append({
            "id": filename.replace(".json", ""),
            "name": data.get("name", "Unbenannt"),
            "activity_type": data.get("activity_type", "Unbekannt")
        })

    return challenges



