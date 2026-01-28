from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

from models.challenge import Challenge
from models.session import Session
from models.goal import Goal
from models.activities import ACTIVITIES, get_activity_names, get_fields

from storage.json_storage import (
    save_challenge,
    load_challenge,
    list_challenges
)

from utils.plotly_utils import create_line_chart_json


app = Flask(__name__)
CORS(app)


# --------------------------------------------------
# Health
# --------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# --------------------------------------------------
# Challenges
# --------------------------------------------------

@app.route("/challenges", methods=["GET", "POST"])
def challenges():
    if request.method == "GET":
        return jsonify(list_challenges())

    data = request.get_json(force=True)

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


@app.get("/challenges/<name>")
def get_challenge(name):
    challenge = load_challenge(name)
    if not challenge:
        return {"error": "challenge not found"}, 404

    return jsonify(challenge.to_dict())


# --------------------------------------------------
# Sessions
# --------------------------------------------------

@app.post("/challenges/<name>/sessions")
def add_session(name):
    challenge = load_challenge(name)
    if not challenge:
        return {"error": "challenge not found"}, 404

    data = request.get_json(force=True)

    date = data.get("date")
    time = data.get("time")
    values = data.get("values")

    if not date or not time or not isinstance(values, dict):
        return {"error": "date, time and values required"}, 400

    session = Session(date, time, values)
    challenge.add_session(session)
    save_challenge(challenge)

    return jsonify(challenge.to_dict()), 200


# --------------------------------------------------
# Goals
# --------------------------------------------------

@app.post("/challenges/<name>/goal")
def set_goal(name):
    challenge = load_challenge(name)
    if not challenge:
        return {"error": "challenge not found"}, 404

    data = request.get_json(force=True)

    description = data.get("description")
    target = data.get("target")
    period = data.get("period")

    if not description or target is None or not period:
        return {"error": "description, target and period required"}, 400

    goal = Goal(description, target, period)
    challenge.set_goal(goal)
    save_challenge(challenge)

    return jsonify(challenge.to_dict()), 200


# --------------------------------------------------
# Activities & Meta
# --------------------------------------------------

@app.get("/activities")
def list_activities():
    return {"activities": get_activity_names()}


@app.get("/activities/<activity_name>")
def get_activity_fields(activity_name):
    if activity_name not in ACTIVITIES:
        return {"error": "unknown activity"}, 404

    return {
        "activity": activity_name,
        "fields": get_fields(activity_name)
    }


@app.get("/challenges/<name>/meta")
def challenge_meta(name):
    challenge = load_challenge(name)
    if not challenge:
        return {"error": "challenge not found"}, 404

    return {
        "activity": challenge.activity_type,
        "fields": get_fields(challenge.activity_type)
    }


# --------------------------------------------------
# Plot
# --------------------------------------------------

@app.get("/challenges/<name>/plot")
def plot_challenge(name):
    """
    Query-Parameter:
    - fields=distanz_km,dauer_min
    - intensities=gemuetlich,stark (optional)
    """
    challenge = load_challenge(name)
    if not challenge:
        return {"error": "challenge not found"}, 404

    fields_param = request.args.get("fields")
    if not fields_param:
        return {"error": "no fields specified"}, 400

    fields = fields_param.split(",")

    intensities_param = request.args.get("intensities")
    intensities_filter = intensities_param.split(",") if intensities_param else None

    sessions = [s.to_dict() for s in challenge.sessions]
    if not sessions:
        return {"error": "no sessions found"}, 400

    df = pd.DataFrame([{"date": s["date"], **s["values"]} for s in sessions])
    df["date"] = pd.to_datetime(df["date"])

    if intensities_filter and "intensitaet" in df.columns:
        df = df[df["intensitaet"].isin(intensities_filter)]

    valid_fields = [f for f in fields if f in df.columns]
    if not valid_fields:
        return {"error": "no valid fields to plot"}, 400

    chart_json = create_line_chart_json(
        df,
        valid_fields,
        title=f"{challenge.name} – Verlauf"
    )

    return jsonify(chart_json)


# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
