from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import plotly.express as px
import pandas as pd
import io
from models.challenge import Challenge
from models.session import Session
from models.goal import Goal
from models.activities import ACTIVITIES

from utils.plotly_utils import create_line_chart_json

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

@app.route("/challenges/<name>/plot", methods=["GET"])
def plot_challenge(name):
    """
    Erwartet Query-Parameter:
    - fields: kommagetrennte Liste der zu plottenden Felder, z.B. ?fields=distanz_km,dauer_min
    - intensities: optional, kommagetrennte Filterwerte für 'intensitaet', z.B. ?intensities=gemuetlich,stark
    """
    challenge = load_challenge(name)
    if not challenge:
        return {"error": "Challenge not found"}, 404

    fields_param = request.args.get("fields", "")
    if not fields_param:
        return {"error": "No fields specified"}, 400

    fields = fields_param.split(",")

    intensities_param = request.args.get("intensities", "")
    intensities_filter = intensities_param.split(",") if intensities_param else None

    sessions = [s.to_dict() for s in challenge.sessions]
    if not sessions:
        return {"error": "No sessions found"}, 400

    df = pd.DataFrame([{"date": s["date"], **s["values"]} for s in sessions])
    df["date"] = pd.to_datetime(df["date"])

    if intensities_filter and "intensitaet" in df.columns:
        df = df[df["intensitaet"].isin(intensities_filter)]

    existing_fields = [f for f in fields if f in df.columns]
    if not existing_fields:
        return {"error": "No valid fields to plot"}, 400

    chart_json = create_line_chart_json(df, existing_fields, title=f"{challenge.name} - Verlauf")
    return jsonify(chart_json)



# ---------------------------
# App start (IMMER GANZ UNTEN)
# ---------------------------

if __name__ == "__main__":
    app.run(debug=True)
