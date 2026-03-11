"""
JSON Storage Module

Provides persistence layer for Challenge data.
Handles saving and loading challenges from JSON files in the local filesystem.
Each challenge is stored as an individual JSON file.
"""

import json
import os
import logging
from models.challenge import Challenge
from models.session import Session
from models.goal import Goal
from config import DATA_DIR

logger = logging.getLogger(__name__)


def _path(name: str):
    """
    Generate full file path for a challenge JSON file.
    
    Args:
        name (str): Challenge name
        
    Returns:
        str: Full path to JSON file
    """
    return os.path.join(DATA_DIR, f"{name}.json")


def save_challenge(challenge: Challenge):
    """
    Save a challenge to JSON file.
    
    Creates the data directory if it doesn't exist, then writes the challenge
    as formatted JSON with UTF-8 encoding.
    
    Args:
        challenge (Challenge): Challenge object to save
        
    Raises:
        Exception: Caught and logged if file write fails
    """
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(_path(challenge.name), "w", encoding="utf-8") as f:
            json.dump(challenge.to_dict(), f, indent=4, ensure_ascii=False)
    except Exception:
        logger.exception("Failed to save challenge %s", challenge.name)


def load_challenge(name: str) -> Challenge | None:
    """
    Load a challenge from JSON file.
    
    Reconstructs the Challenge object with all sessions and goal information.
    Uses try-except-finally pattern for robust error handling.
    
    Args:
        name (str): Challenge name to load
        
    Returns:
        Optional[Challenge]: Loaded challenge or None if not found/error
        
    Raises:
        Exception: Caught and logged if file read or parsing fails
    """
    try:
        path = _path(name)
        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Reconstruct Challenge object from JSON
        c = Challenge(data["name"], data["activity_type"])

        # Restore goal if it exists
        if data.get("goal"):
            g = data["goal"]
            # Handle both old format (without reference) and new format (with reference)
            c.set_goal(Goal(
                description=g["description"],
                target=g.get("target"),
                period=g.get("period", ""),
                reference=g.get("reference")
            ))

        # Restore all sessions
        for s in data.get("sessions", []):
            c.add_session(Session(s["date"], s["time"], s["values"]))

        return c

    except Exception:
        logger.exception("Failed to load challenge %s", name)
        return None


def list_challenges() -> list[dict]:
    """
    List all available challenges.
    
    Scans the data directory and returns metadata for each challenge JSON file.
    
    Returns:
        List[Dict]: List of challenge metadata dicts with name and activity_type
    """
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
