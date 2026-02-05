from utils.logger import setup_logging, get_logger
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import pandas as pd
from models.challenge import Challenge
from models.session import Session
from models.goal import Goal
from models.activities import ACTIVITIES, get_activity_names, get_fields
from storage.json_storage import save_challenge, load_challenge, list_challenges
import plotly.graph_objects as go
import plotly.io as pio

# Logging
setup_logging()
logger = get_logger(__name__)

# App Setup
app = Flask(__name__, template_folder="templates")
CORS(app)

# Helper: Check if client wants JSON (based on Accept header or Content-Type)
def wants_json():
    """Prüfe ob Client JSON will oder HTML"""
    # Wenn Accept-Header application/json enthält -> JSON
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return True
    # Wenn Content-Type JSON ist -> wahrscheinlich AJAX -> JSON
    if "application/json" in request.content_type:
        return True
    # Wenn User-Agent wie eine API aussieht -> JSON
    ua = request.headers.get("User-Agent", "").lower()
    if "chrome" not in ua and "firefox" not in ua and "safari" not in ua:
        return True
    return False


# ============================================================
# HTML ROUTES (Haupt-Interface)
# ============================================================

@app.get("/debug/list-files")
def debug_list_files():
    """Debug: Zeige alle Dateien im data-Verzeichnis"""
    from config import DATA_DIR
    import os
    try:
        files = os.listdir(DATA_DIR) if os.path.exists(DATA_DIR) else []
        return {
            "DATA_DIR": DATA_DIR,
            "exists": os.path.exists(DATA_DIR),
            "files": files,
            "json_files": [f for f in files if f.endswith(".json")]
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/debug/challenges")
def debug_challenges():
    """Debug: Zeige alle Challenges"""
    try:
        challenges_list = list_challenges()
        logger.info(f"list_challenges() returned: {challenges_list}")
        
        result = {
            "list_challenges_output": challenges_list,
            "loaded_challenges": []
        }
        
        for ch in challenges_list:
            challenge = load_challenge(ch["name"])
            if challenge:
                result["loaded_challenges"].append({
                    "name": challenge.name,
                    "activity_type": challenge.activity_type,
                    "sessions_count": len(challenge.sessions) if challenge.sessions else 0
                })
            else:
                result["loaded_challenges"].append({
                    "name": ch["name"],
                    "error": "Failed to load"
                })
        
        return result
    except Exception as e:
        logger.exception("Debug error")
        return {"error": str(e)}
def index():
    """Hauptseite: Zeige alle Challenges und Formular zum Erstellen"""
    try:
        challenges = []
        challenge_list = list_challenges()
        logger.info(f"Found {len(challenge_list)} challenges from list_challenges()")
        
        for ch in challenge_list:
            logger.info(f"Loading challenge: {ch['name']}")
            challenge = load_challenge(ch["name"])
            if challenge:
                challenges.append({
                    "name": challenge.name,
                    "activity_type": challenge.activity_type,
                    "sessions": challenge.sessions if challenge.sessions else []
                })
                logger.info(f"Successfully loaded: {challenge.name} with {len(challenge.sessions)} sessions")
            else:
                logger.warning(f"Failed to load challenge: {ch['name']}")
        
        logger.info(f"Rendering index with {len(challenges)} challenges")
        message = request.args.get("message", "")
        activities = get_activity_names()
        
        return render_template(
            "index.html",
            challenges=challenges,
            activities=activities,
            message=message
        )
    except Exception as e:
        logger.exception("Failed to render index")
        return render_template("index.html", challenges=[], activities=[], message=f"Fehler: {str(e)}")


@app.post("/challenges")
def create_challenge_html():
    """POST: Neue Challenge erstellen (von HTML-Form)"""
    try:
        name = request.form.get("name", "").strip()
        activity = request.form.get("activity", "").strip()

        if not name or not activity:
            return redirect(url_for("index", message="Name und Activity sind erforderlich"))

        if activity not in ACTIVITIES:
            return redirect(url_for("index", message="Unbekannter Activity-Typ"))

        if load_challenge(name):
            return redirect(url_for("index", message="Challenge existiert bereits"))

        challenge = Challenge(name, activity)
        save_challenge(challenge)
        logger.info("Challenge erstellt (HTML): %s", name)
        
        return redirect(url_for("index", message=f"Challenge '{name}' erfolgreich erstellt"))
    except Exception as e:
        logger.exception("Failed to create challenge via HTML")
        return redirect(url_for("index", message=f"Fehler beim Erstellen: {str(e)}"))


@app.route("/challenges/<name>", methods=["GET", "POST"])
def challenge_detail(name):
    """Challenge-Detailseite mit Sessions und Goal"""
    try:
        challenge = load_challenge(name)
        if not challenge:
            return redirect(url_for("index", message="Challenge nicht gefunden"))

        # POST: Neue Session oder Goal hinzufügen
        if request.method == "POST":
            if "date" in request.form and "time" in request.form:
                # Session hinzufügen
                date = request.form.get("date", "")
                time = request.form.get("time", "")
                
                # Alle Formular-Values extrahieren
                values = {}
                fields = get_fields(challenge.activity_type)
                for field in fields:
                    field_name = field["name"] if isinstance(field, dict) else field.name
                    val = request.form.get(field_name, "")
                    if val:
                        field_type = field["type"] if isinstance(field, dict) else field.type
                        if field_type == "number":
                            try:
                                values[field_name] = float(val)
                            except ValueError:
                                values[field_name] = val
                        else:
                            values[field_name] = val

                session = Session(date, time, values)
                challenge.add_session(session)
                save_challenge(challenge)
                logger.info("Session hinzugefügt zu %s", name)

            elif "description" in request.form:
                # Goal speichern
                description = request.form.get("description", "")
                target = request.form.get("target", "")
                period = request.form.get("period", "")

                if description and target and period:
                    try:
                        goal = Goal(description, float(target), period)
                        challenge.set_goal(goal)
                        save_challenge(challenge)
                        logger.info("Goal gesetzt für %s", name)
                    except Exception as e:
                        logger.exception("Failed to set goal")

            # Goal löschen
            if request.args.get("delete_goal"):
                challenge.goal = None
                save_challenge(challenge)
                logger.info("Goal gelöscht für %s", name)

            return redirect(url_for("challenge_detail", name=name))

        # GET: Seite anzeigen
        fields_raw = get_fields(challenge.activity_type)
        fields = []
        for field in fields_raw:
            if isinstance(field, dict):
                fields.append(field)
            else:
                fields.append(field.to_dict())
        
        message = request.args.get("message", "")

        return render_template(
            "challenge_detail.html",
            challenge_name=challenge.name,
            activity_type=challenge.activity_type,
            fields=fields,
            goal=challenge.goal.to_dict() if challenge.goal else None,
            sessions=challenge.sessions,
            message=message
        )
    except Exception as e:
        logger.exception("Failed to render challenge detail")
        return redirect(url_for("index", message=f"Fehler: {str(e)}"))


@app.route("/challenges/<name>/plot", methods=["GET"])
def plot_challenge_html(name):
    """Visualisierungs-Seite mit interaktivem Plotly-Diagramm"""
    try:
        challenge = load_challenge(name)
        if not challenge:
            return redirect(url_for("index", message="Challenge nicht gefunden"))

        available_fields_raw = get_fields(challenge.activity_type)
        available_fields = []
        for field in available_fields_raw:
            if isinstance(field, dict):
                available_fields.append(field)
            else:
                available_fields.append(field.to_dict())

        if not challenge.sessions:
            return render_template(
                "plot.html",
                challenge_name=challenge.name,
                activity_type=challenge.activity_type,
                available_fields=available_fields,
                chart_html="",
                chart_type="line",
                selected_fields=[],
                selected_intensities=[],
                available_intensities=["gemuetlich", "mittel", "stark"]
            )

        # Get Parameter
        fields_param = request.args.get("fields", "")
        selected_fields = [f for f in fields_param.split(",") if f] if fields_param else []
        
        intensities_param = request.args.get("intensities", "")
        selected_intensities = [i for i in intensities_param.split(",") if i] if intensities_param else []
        
        chart_type = request.args.get("chart_type", "line")

        # DataFrame erzeugen
        sessions_data = [s.to_dict() for s in challenge.sessions]
        df = pd.DataFrame([{"date": s["date"], **s["values"]} for s in sessions_data])
        df["date"] = pd.to_datetime(df["date"])

        # Intensität filtern
        if selected_intensities and "intensitaet" in df.columns:
            df = df[df["intensitaet"].isin(selected_intensities)]

        # Plotly-Diagramm erzeugen
        chart_html = ""
        if selected_fields:
            fig = go.Figure()

            if chart_type == "bar":
                for f in selected_fields:
                    if f in df.columns and pd.api.types.is_numeric_dtype(df[f]):
                        agg = df.groupby("date")[f].sum().reset_index()
                        fig.add_trace(go.Bar(
                            x=agg["date"],
                            y=agg[f],
                            name=f
                        ))
            else:  # line
                for f in selected_fields:
                    if f in df.columns:
                        fig.add_trace(go.Scatter(
                            x=df["date"],
                            y=df[f],
                            mode="lines+markers",
                            name=f
                        ))

            fig.update_layout(
                title=f"{challenge.name} – Verlauf",
                xaxis_title="Datum",
                yaxis_title="Wert",
                hovermode="closest",
                height=500
            )

            chart_html = pio.to_html(fig, include_plotlyjs="cdn", div_id="chart")

        return render_template(
            "plot.html",
            challenge_name=challenge.name,
            activity_type=challenge.activity_type,
            available_fields=available_fields,
            chart_html=chart_html,
            chart_type=chart_type,
            selected_fields=selected_fields,
            selected_intensities=selected_intensities,
            available_intensities=["gemuetlich", "mittel", "stark"]
        )

    except Exception as e:
        logger.exception("Failed to render plot")
        return redirect(url_for("index", message=f"Fehler: {str(e)}"))


# Backward compatibility: Alte Endpoints ohne /api/ Prefix (für React Frontend)
@app.route("/challenges", methods=["GET", "POST"])
def challenges_json():
    """GET: Alle Challenges auflisten (JSON)
       POST: Neue Challenge erstellen (JSON)"""
    if request.method == "GET":
        try:
            logger.debug("Listing challenges (JSON API - backward compat)")
            return jsonify(list_challenges())
        except Exception:
            logger.exception("Failed to list challenges")
            return {"error": "internal server error"}, 500

    # POST - Neue Challenge erstellen
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
        logger.info("Challenge created (JSON API): %s (%s)", name, activity_type)
        return jsonify(challenge.to_dict()), 201

    except Exception:
        logger.exception("Failed to create challenge %s", name)
        return {"error": "internal server error"}, 500


@app.get("/activities")
def activities_json():
    """GET: Alle Activities auflisten (JSON) - Backward Compat"""
    try:
        logger.debug("Listing activities (JSON API - backward compat)")
        return {"activities": get_activity_names()}
    except Exception:
        logger.exception("Failed to list activities")
        return {"error": "internal server error"}, 500


@app.get("/activities/<activity_name>")
def activity_fields_json(activity_name):
    """GET: Activity-Felder - Backward Compat"""
    if activity_name not in ACTIVITIES:
        logger.warning("Unknown activity requested: %s", activity_name)
        return {"error": "unknown activity"}, 404

    try:
        fields_raw = get_fields(activity_name)
        fields = []
        for field in fields_raw:
            if isinstance(field, dict):
                fields.append(field)
            else:
                fields.append(field.to_dict())
        
        return {
            "activity": activity_name,
            "fields": fields
        }
    except Exception:
        logger.exception("Failed to get fields for activity %s", activity_name)
        return {"error": "internal server error"}, 500


@app.post("/challenges/<name>/sessions")
def add_session_json(name):
    """POST: Session hinzufügen - Backward Compat"""
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


@app.post("/challenges/<name>/goal")
def set_goal_json(name):
    """POST: Goal setzen - Backward Compat"""
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


@app.get("/challenges/<name>/plot")
def plot_json(name):
    """GET: Plot-Daten - Backward Compat"""
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


@app.get("/api/health")
def api_health():
    logger.debug("Health check called")
    return {"status": "ok"}

if __name__ == "__main__":
    logger.info("Starting Flask app")
    app.run(debug=True, host="127.0.0.1", port=5000)