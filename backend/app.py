from flask import Flask, request, jsonify
from flask_cors import CORS

from models.challenge import Challenge
from models.session import Session
from models.goal import Goal
from models.activities import ACTIVITIES

from storage.json_storage import (
    save_challenge,
    load_challenge,
    list_challenges
)

app = Flask(__name__)
CORS(app)

# ---------------------------
# Health
# ---------------------------

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}


# ---------------------------
# Challenges (GET + POST)
# ---------------------------

@app.route("/challenges", methods=["GET", "POST"])
def challenges():
    # GET → Liste aller Challenges
    if request.method == "GET":
        return jsonify(list_challenges())

    # POST → neue Challenge erstellen
    data = request.json

    name = data.get("name")
    activity_type = data.get("activity")

    if not name or not activity_type:
        return {"error": "name and activity required"}, 400

    if activity_type not in ACTIVITIES:
        return {"error": "unknown activity"}, 400

    if load_challenge(name):
        return {"error": "challenge already exists"}, 400

    challenge = Challenge(name, activity_type)
    save_challenge(challenge)

    return jsonify(challenge.to_dict()), 201


# ---------------------------
# Single Challenge
# ---------------------------

@app.route("/challenges/<name>", methods=["GET"])
def get_challenge(name):
    challenge = load_challenge(name)
    if not challenge:
        return {"error": "challenge not found"}, 404

    return jsonify(challenge.to_dict())


# ---------------------------
# Sessions
# ---------------------------

@app.route("/challenges/<name>/sessions", methods=["POST"])
def add_session(name):
    challenge = load_challenge(name)
    if not challenge:
        return {"error": "challenge not found"}, 404

    data = request.json
    date = data.get("date")
    time = data.get("time")
    values = data.get("values")

    if not date or not time or not values:
        return {"error": "date, time and values required"}, 400

    session = Session(date, time, values)
    challenge.add_session(session)
    save_challenge(challenge)

    return jsonify(challenge.to_dict()), 200


# ---------------------------
# Goal
# ---------------------------

@app.route("/challenges/<name>/goal", methods=["POST"])
def set_goal(name):
    challenge = load_challenge(name)
    if not challenge:
        return {"error": "challenge not found"}, 404

    data = request.json
    description = data.get("description")
    target = data.get("target")
    period = data.get("period")

    if not description or target is None or not period:
        return {"error": "description, target and period required"}, 400

    goal = Goal(description, target, period)
    challenge.set_goal(goal)
    save_challenge(challenge)

    return jsonify(challenge.to_dict()), 200


# ---------------------------
# Activities
# ---------------------------

@app.route("/activities/<activity_name>", methods=["GET"])
def get_activity_fields(activity_name):
    if activity_name not in ACTIVITIES:
        return {"error": "unknown activity"}, 404

    return jsonify({
        "activity": activity_name,
        "fields": ACTIVITIES[activity_name]
    })


# ---------------------------
# App start (IMMER GANZ UNTEN)
# ---------------------------

if __name__ == "__main__":
    app.run(debug=True)
