from utils.logger import setup_logging, get_logger
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from models.challenge import Challenge
from models.session import Session
from models.goal import Goal
from models.activities import ACTIVITIES, get_activity_names, get_fields
from storage.json_storage import save_challenge, load_challenge, list_challenges

# Logging
setup_logging()
logger = get_logger(__name__)

# App Setup
app = Flask(__name__)
CORS(app)

# Health
@app.get("/health")
def health():
    logger.debug("Health check called")
    return {"status": "ok"}

# Challenges
@app.route("/challenges", methods=["GET", "POST"])
def challenges():
    if request.method == "GET":
        try:
            logger.debug("Listing challenges")
            return jsonify(list_challenges())
        except Exception:
            logger.exception("Failed to list challenges")
            return {"error": "internal server error"}, 500

    # POST
    try:
        data = request.get_json(force=True)
    except Exception:
        logger.warning("Invalid JSON in challenge creation")
        return {"error": "invalid JSON"}, 400

    name = data.get("name")
    activity_type = data.get("activity")

    if not name or not activity_type:
        logger.warning("Missing name or activity")
        return {"error": "name and activity required"}, 400

    if activity_type not in ACTIVITIES:
        logger.warning("Unknown activity type: %s", activity_type)
        return {"error": "unknown activity"}, 400

    if load_challenge(name):
        logger.warning("Challenge already exists: %s", name)
        return {"error": "challenge already exists"}, 400

    try:
        challenge = Challenge(name, activity_type)
        save_challenge(challenge)
        logger.info("Challenge created: %s (%s)", name, activity_type)
        return jsonify(challenge.to_dict()), 201

    except Exception:
        logger.exception("Failed to create challenge %s", name)
        return {"error": "internal server error"}, 500


@app.get("/challenges/<name>")
def get_challenge(name):
    try:
        challenge = load_challenge(name)
        if not challenge:
            logger.warning("Challenge not found: %s", name)
            return {"error": "challenge not found"}, 404

        logger.debug("Challenge loaded: %s", name)
        return jsonify(challenge.to_dict())

    except Exception:
        logger.exception("Failed to load challenge %s", name)
        return {"error": "internal server error"}, 500

# Sessions
@app.post("/challenges/<name>/sessions")
def add_session(name):
    try:
        challenge = load_challenge(name)
        if not challenge:
            logger.warning("Challenge not found (session): %s", name)
            return {"error": "challenge not found"}, 404

        data = request.get_json(force=True)

        if not all(k in data for k in ("date", "time", "values")):
            logger.warning("Incomplete session payload for %s", name)
            return {"error": "date, time and values required"}, 400

        session = Session(
            date=data["date"],
            time=data["time"],
            values=data["values"]
        )

        challenge.add_session(session)
        save_challenge(challenge)

        logger.info("Session added to challenge %s", name)
        return jsonify(challenge.to_dict()), 200

    except Exception:
        logger.exception("Failed to add session to challenge %s", name)
        return {"error": "internal server error"}, 500

# Goals
@app.post("/challenges/<name>/goal")
def set_goal(name):
    try:
        challenge = load_challenge(name)
        if not challenge:
            logger.warning("Challenge not found (goal): %s", name)
            return {"error": "challenge not found"}, 404

        data = request.get_json(force=True)

        description = data.get("description")
        target = data.get("target")
        period = data.get("period")

        if not description or target is None or not period:
            logger.warning("Invalid goal payload for %s", name)
            return {"error": "description, target and period required"}, 400

        goal = Goal(description, target, period)
        challenge.set_goal(goal)
        save_challenge(challenge)

        logger.info("Goal set for challenge %s", name)
        return jsonify(challenge.to_dict()), 200

    except Exception:
        logger.exception("Failed to set goal for %s", name)
        return {"error": "internal server error"}, 500

# Activities & Meta
@app.get("/activities")
def list_activities():
    try:
        logger.debug("Listing activities")
        return {"activities": get_activity_names()}
    except Exception:
        logger.exception("Failed to list activities")
        return {"error": "internal server error"}, 500


@app.get("/activities/<activity_name>")
def get_activity_fields(activity_name):
    if activity_name not in ACTIVITIES:
        logger.warning("Unknown activity requested: %s", activity_name)
        return {"error": "unknown activity"}, 404

    try:
        return {
            "activity": activity_name,
            "fields": get_fields(activity_name)
        }
    except Exception:
        logger.exception("Failed to get fields for activity %s", activity_name)
        return {"error": "internal server error"}, 500


@app.get("/challenges/<name>/meta")
def challenge_meta(name):
    try:
        challenge = load_challenge(name)
        if not challenge:
            logger.warning("Challenge not found (meta): %s", name)
            return {"error": "challenge not found"}, 404

        return {
            "activity": challenge.activity_type,
            "fields": get_fields(challenge.activity_type)
        }

    except Exception:
        logger.exception("Failed to load challenge meta for %s", name)
        return {"error": "internal server error"}, 500

# Plot
@app.get("/challenges/<name>/plot")
def plot_challenge(name):
    try:
        challenge = load_challenge(name)
        if not challenge:
            logger.warning("Challenge not found (plot): %s", name)
            return {"error": "challenge not found"}, 404

        fields_param = request.args.get("fields")
        if not fields_param:
            logger.warning("No fields specified for plot (%s)", name)
            return {"error": "no fields specified"}, 400

        fields = fields_param.split(",")

        intensities_param = request.args.get("intensities")
        intensities_filter = intensities_param.split(",") if intensities_param else None

        sessions = [s.to_dict() for s in challenge.sessions]
        if not sessions:
            logger.warning("No sessions found for plot (%s)", name)
            return {"error": "no sessions found"}, 400

        df = pd.DataFrame([{"date": s["date"], **s["values"]} for s in sessions])
        df["date"] = pd.to_datetime(df["date"])

        if intensities_filter and "intensitaet" in df.columns:
            df = df[df["intensitaet"].isin(intensities_filter)]

        chart_type = request.args.get("chart_type", "line")

        data = []
        layout = {
            "title": f"{challenge.name} – Verlauf",
            "xaxis": {"title": "Datum"},
            "yaxis": {"title": "Wert"},
            "hovermode": "closest"
        }

        if chart_type == "bar":
            logger.debug("Generating bar chart for %s", name)
            for f in fields:
                if f in df.columns and pd.api.types.is_numeric_dtype(df[f]):
                    agg = df.groupby("date")[f].sum().reset_index()
                    data.append({
                        "x": agg["date"].tolist(),
                        "y": agg[f].tolist(),
                        "type": "bar",
                        "name": f
                    })
            layout["barmode"] = "group"
        else:
            logger.debug("Generating line chart for %s", name)
            for f in fields:
                if f in df.columns:
                    data.append({
                        "x": df["date"].tolist(),
                        "y": df[f].tolist(),
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": f
                    })

        return jsonify({"data": data, "layout": layout})

    except Exception:
        logger.exception("Failed to generate plot for %s", name)
        return {"error": "internal server error"}, 500

if __name__ == "__main__":
    logger.info("Starting Flask app")
    app.run(debug=True)