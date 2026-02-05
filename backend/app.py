from utils.logger import setup_logging, get_logger
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import pandas as pd
from models.challenge import Challenge
from models.session import Session
from models.goal import Goal
from models.activities import (
    ACTIVITIES, get_activity_names, get_fields,
    get_numeric_fields, get_category_fields, get_field_unit,
    get_comparison_features
)
from storage.json_storage import save_challenge, load_challenge, list_challenges
import plotly.graph_objects as go
import plotly.io as pio
import os
import numpy as np

# Logging
setup_logging()
logger = get_logger(__name__)

# App Setup
app = Flask(__name__, template_folder="templates")
# Erlaube CORS für alle Routen/Origins (Development-friendly)
CORS(app, resources={r"/*": {"origins": "*"}}, send_wildcard=True)


@app.after_request
def add_cors_headers(response):
    """Stelle sicher, dass auch bei Fehlern CORS-Header vorhanden sind."""
    response.headers.setdefault("Access-Control-Allow-Origin", "*")
    response.headers.setdefault("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.setdefault("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response


@app.before_request
def handle_options():
    """Return early for preflight OPTIONS requests with proper headers."""
    if request.method == 'OPTIONS':
        from flask import make_response
        resp = make_response(('', 204))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return resp


@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON error with CORS headers for unexpected exceptions."""
    from flask import make_response
    logger.exception("Unhandled exception: %s", e)
    body = {"error": "internal server error", "message": str(e)}
    resp = make_response(jsonify(body), 500)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return resp


# ============================================================
# HELPER: Content Negotiation
# ============================================================

def wants_json():
    """Prüfe ob Client JSON will basierend auf Accept-Header"""
    # Wenn Accept-Header application/json enthält -> JSON
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return True
    # Wenn Content-Type JSON ist -> AJAX -> JSON
    if request.content_type and "application/json" in request.content_type:
        return True
    # If request contains an Origin header (likely CORS fetch), treat as JSON/AJAX
    if request.headers.get('Origin'):
        return True
    return False


# ============================================================
# DEBUG ROUTES
# ============================================================

@app.get("/debug/list-files")
def debug_list_files():
    """Debug: Zeige alle Dateien im data-Verzeichnis"""
    from config import DATA_DIR
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


# ============================================================
# MAIN ROUTES: Smart Content-Negotiation
# ============================================================

@app.route("/", methods=["GET"])
@app.route("/challenges", methods=["GET", "POST"])
def handle_challenges():
    """
    Smart Router für Challenges:
    - GET /: HTML für Browser
    - GET /challenges (AJAX): JSON für React
    - POST /challenges (Form): Redirect
    - POST /challenges (JSON): JSON Response
    """
    logger.debug(f"handle_challenges: {request.method} | wants_json={wants_json()}")
    
    # GET Request
    if request.method == "GET":
        try:
            challenge_list = list_challenges()
            challenges = []
            
            for ch in challenge_list:
                challenge = load_challenge(ch["name"])
                if challenge:
                    challenges.append(challenge.to_dict())
            
            # JSON Response für AJAX
            if wants_json():
                logger.debug(f"GET /challenges -> JSON ({len(challenges)} challenges)")
                return jsonify(challenges), 200
            
            # HTML Response für Browser
            logger.debug(f"GET / -> HTML ({len(challenges)} challenges)")
            activities = get_activity_names()
            message = request.args.get("message", "")
            return render_template("index.html", challenges=challenges, activities=activities, message=message)
            
        except Exception as e:
            logger.exception("Error in GET /challenges")
            if wants_json():
                return {"error": str(e)}, 500
            return render_template("index.html", challenges=[], activities=[], message=f"Fehler: {str(e)}")
    
    # POST Request
    if request.method == "POST":
        try:
            # JSON POST (von React/AJAX)
            if request.is_json:
                data = request.get_json()
                name = data.get("name", "").strip()
                activity = data.get("activity", "").strip()
                
                if not name or not activity:
                    return {"error": "name und activity erforderlich"}, 400
                if activity not in ACTIVITIES:
                    return {"error": f"Unknown activity: {activity}"}, 400
                if load_challenge(name):
                    return {"error": "Challenge already exists"}, 400
                
                challenge = Challenge(name, activity)
                save_challenge(challenge)
                logger.info(f"Challenge created (JSON): {name}")
                return jsonify(challenge.to_dict()), 201
            
            # Form POST (von HTML-Form)
            else:
                name = request.form.get("name", "").strip()
                activity = request.form.get("activity", "").strip()
                
                if not name or not activity:
                    return redirect(url_for("handle_challenges", message="Name und Activity erforderlich"))
                if activity not in ACTIVITIES:
                    return redirect(url_for("handle_challenges", message="Unbekannter Activity-Typ"))
                if load_challenge(name):
                    return redirect(url_for("handle_challenges", message="Challenge existiert bereits"))
                
                challenge = Challenge(name, activity)
                save_challenge(challenge)
                logger.info(f"Challenge created (HTML): {name}")
                return redirect(url_for("handle_challenges", message=f"Challenge '{name}' erfolgreich erstellt"))
                
        except Exception as e:
            logger.exception("Error in POST /challenges")
            if wants_json():
                return {"error": str(e)}, 500
            return redirect(url_for("handle_challenges", message=f"Fehler: {str(e)}"))


@app.route("/challenges/<name>", methods=["GET", "POST"])
def handle_challenge_detail(name):
    """
    Smart Router für Challenge-Details:
    - GET /challenges/<name> (AJAX): JSON
    - GET /challenges/<name> (Browser): HTML
    - POST /challenges/<name> (Form/JSON): Beide
    """
    logger.debug(f"handle_challenge_detail: {request.method} {name} | wants_json={wants_json()}")
    
    try:
        challenge = load_challenge(name)
        if not challenge:
            if wants_json():
                return {"error": "Challenge not found"}, 404
            return redirect(url_for("handle_challenges", message="Challenge nicht gefunden"))
        
        # GET Request
        if request.method == "GET":
            if wants_json():
                # JSON für AJAX
                logger.debug(f"GET /challenges/{name} -> JSON")
                return jsonify(challenge.to_dict()), 200
            else:
                # HTML für Browser
                logger.debug(f"GET /challenges/{name} -> HTML")
                fields_raw = get_fields(challenge.activity_type)
                fields = [f.to_dict() if hasattr(f, "to_dict") else f for f in fields_raw]
                goal_dict = challenge.goal.to_dict() if challenge.goal else None
                message = request.args.get("message", "")
                return render_template(
                    "challenge_detail.html",
                    challenge_name=name,
                    activity_type=challenge.activity_type,
                    fields=fields,
                    goal=goal_dict,
                    sessions=challenge.sessions,
                    message=message
                )
        
        # POST Request
        if request.method == "POST":
            logger.debug(f"POST /challenges/{name}")
            payload = request.get_json() if request.is_json else request.form
            
            # Session hinzufügen
            if "date" in payload and "time" in payload:
                date = payload.get("date", "")
                time = payload.get("time", "")
                
                # Values extrahieren
                values = {}
                fields = get_fields(challenge.activity_type)
                for field in fields:
                    field_name = field["name"] if isinstance(field, dict) else field.name
                    val = payload.get(field_name)
                    if val is not None:
                        field_type = field["type"] if isinstance(field, dict) else field.type
                        if field_type == "number":
                            try:
                                values[field_name] = float(val)
                            except (ValueError, TypeError):
                                values[field_name] = val
                        else:
                            values[field_name] = val
                
                session = Session(date, time, values)
                challenge.add_session(session)
                save_challenge(challenge)
                logger.info(f"Session added to {name}")
                
                if wants_json():
                    return jsonify(challenge.to_dict()), 200
                return redirect(url_for("handle_challenge_detail", name=name))
            
            # Goal speichern oder löschen
            elif "description" in payload or request.args.get("delete_goal"):
                if request.args.get("delete_goal"):
                    challenge.goal = None
                    logger.info(f"Goal deleted for {name}")
                else:
                    description = payload.get("description", "")
                    target = payload.get("target", "")
                    period = payload.get("period", "")
                    
                    if description and target and period:
                        try:
                            goal = Goal(description, float(target), period)
                            challenge.set_goal(goal)
                            logger.info(f"Goal set for {name}")
                        except Exception as e:
                            logger.exception("Error setting goal")
                
                save_challenge(challenge)
                if wants_json():
                    return jsonify(challenge.to_dict()), 200
                return redirect(url_for("handle_challenge_detail", name=name))
            
            # Fallback
            if wants_json():
                return jsonify(challenge.to_dict()), 200
            return redirect(url_for("handle_challenge_detail", name=name))
    
    except Exception as e:
        logger.exception(f"Error in handle_challenge_detail for {name}")
        if wants_json():
            return {"error": str(e)}, 500
        return redirect(url_for("handle_challenges", message=f"Fehler: {str(e)}"))


@app.route("/challenges/<name>/plot", methods=["GET"])
def handle_challenge_plot(name):
    """
    Enhanced Plot-Handler mit Filter, Vergleiche, und Anpassungen:
    - Mehrere Felder auf einer Y-Achse (mit Einheiten)
    - Bar + Line kombinierbar
    - Vergleiche nach Kategorien (z.B. Laufstrecke: mix vs asphalt)
    - Dynamische Achsen-Skalierung
    """
    try:
        challenge = load_challenge(name)
        if not challenge:
            if wants_json():
                return {"error": "Challenge not found"}, 404
            return redirect(url_for("handle_challenges", message="Challenge nicht gefunden"))
        
        # Lade verfügbare Felder
        available_fields_raw = get_fields(challenge.activity_type)
        available_fields = [f.to_dict() if hasattr(f, "to_dict") else f for f in available_fields_raw]
        
        numeric_fields = get_numeric_fields(challenge.activity_type)
        category_fields = get_category_fields(challenge.activity_type)
        comparison_features = get_comparison_features(challenge.activity_type)
        
        # Wenn keine Sessions -> leeres Chart
        if not challenge.sessions:
            if wants_json():
                return {"error": "No sessions found"}, 400
            return render_template("plot.html",
                                 challenge_name=name,
                                 activity_type=challenge.activity_type,
                                 available_fields=available_fields,
                                 numeric_fields=numeric_fields,
                                 category_fields=category_fields,
                                 comparison_features=comparison_features,
                                 chart_html="",
                                 chart_data={},
                                 chart_type="line",
                                 selected_fields=[],
                                 selected_intensities=[],
                                 available_intensities=["gemütlich", "mittel", "stark"],
                                 comparison_field="",
                                 comparison_values=[])
        
        # Parameter laden
        fields_param = request.args.get("fields", "")
        selected_fields = [f.strip() for f in fields_param.split(",") if f.strip()] if fields_param else []
        
        intensities_param = request.args.get("intensities", "")
        selected_intensities = [i.strip() for i in intensities_param.split(",") if i.strip()] if intensities_param else []
        
        chart_type = request.args.get("chart_type", "line")  # 'line', 'bar', 'scatter'
        
        # Vergleichsfeld (z.B. strecke_typ, intensitaet)
        comparison_field = request.args.get("comparison_field", "")
        
        # DataFrame erzeugen mit allen Daten
        sessions_data = [s.to_dict() for s in challenge.sessions]
        df = pd.DataFrame([{"date": s["date"], **s["values"]} for s in sessions_data])
        df["date"] = pd.to_datetime(df["date"])
        
        # Filter nach Intensität
        if selected_intensities and "intensitaet" in df.columns:
            df = df[df["intensitaet"].isin(selected_intensities)]
        
        # Wenn keine Felder ausgewählt, nutze Default (erste numerische Felder)
        if not selected_fields and numeric_fields:
            selected_fields = numeric_fields[:2]  # Max 2 default
        
        # ========== PLOTLY GENERIERUNG ==========
        data = []
        layout = {
            "title": f"{challenge.name} – Verlauf",
            "xaxis": {"title": "Datum"},
            "yaxis": {"title": "Wert"},
            "hovermode": "x unified",
            "height": 600,
            "plot_bgcolor": "#fbfcfe",
            "paper_bgcolor": "#ffffff",
        }
        
        # Wenn Vergleichsfeld aktiviert, erstelle gruppierte Daten pro Kategorie
        if comparison_field and comparison_field in df.columns:
            comparison_values = sorted(df[comparison_field].unique())
            layout["title"] = f"{challenge.name} – Vergleich nach {comparison_field}"
            
            if chart_type == "bar":
                layout["barmode"] = "group"
            
            # Für jede Vergleich-Kategorie und jedes Feld eine Spur
            for comp_val in comparison_values:
                df_subset = df[df[comparison_field] == comp_val]
                
                for field in selected_fields:
                    if field not in df_subset.columns or not pd.api.types.is_numeric_dtype(df_subset[field]):
                        continue
                    
                    unit = get_field_unit(challenge.activity_type, field)
                    field_label = f"{field}" + (f" ({unit})" if unit else "")
                    trace_name = f"{field} - {comp_val}"
                    
                    if chart_type == "bar":
                        agg = df_subset.groupby("date")[field].sum().reset_index()
                        data.append({
                            "x": [str(d.date()) for d in agg["date"]],
                            "y": agg[field].tolist(),
                            "type": "bar",
                            "name": trace_name,
                            "hovertemplate": f"<b>{trace_name}</b><br>Datum: %{{x}}<br>Wert: %{{y}}{' ' + unit if unit else ''}<extra></extra>",
                        })
                    else:  # line/scatter
                        data.append({
                            "x": [str(d.date()) for d in df_subset["date"]],
                            "y": df_subset[field].tolist(),
                            "type": "scatter",
                            "mode": "lines+markers",
                            "name": trace_name,
                            "hovertemplate": f"<b>{trace_name}</b><br>Datum: %{{x}}<br>Wert: %{{y}}{' ' + unit if unit else ''}<extra></extra>",
                        })
        
        else:
            # Normales Diagramm ohne Vergleich
            if chart_type == "bar":
                layout["barmode"] = "group"
                
                for field in selected_fields:
                    if field not in df.columns or not pd.api.types.is_numeric_dtype(df[field]):
                        continue
                    
                    agg = df.groupby("date")[field].sum().reset_index()
                    unit = get_field_unit(challenge.activity_type, field)
                    
                    data.append({
                        "x": [str(d.date()) for d in agg["date"]],
                        "y": agg[field].tolist(),
                        "type": "bar",
                        "name": field,
                        "hovertemplate": f"<b>{field}</b><br>Datum: %{{x}}<br>Wert: %{{y}}{' ' + unit if unit else ''}<extra></extra>",
                    })
            else:  # line
                for field in selected_fields:
                    if field not in df.columns:
                        continue
                    
                    unit = get_field_unit(challenge.activity_type, field)
                    
                    data.append({
                        "x": [str(d.date()) for d in df["date"]],
                        "y": df[field].tolist(),
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": field,
                        "hovertemplate": f"<b>{field}</b><br>Datum: %{{x}}<br>Wert: %{{y}}{' ' + unit if unit else ''}<extra></extra>",
                    })
        
        # Y-Achse optimieren (auto-range)
        if data:
            all_y = []
            for trace in data:
                all_y.extend([y for y in trace["y"] if y is not None and not pd.isna(y)])
            
            if all_y:
                y_min = min(all_y)
                y_max = max(all_y)
                y_range = y_max - y_min
                
                # 10% Puffer auf beiden Seiten
                layout["yaxis"]["range"] = [y_min - 0.1 * y_range, y_max + 0.1 * y_range]
        
        # JSON Response
        if wants_json():
            return jsonify({"data": data, "layout": layout}), 200
        
        # HTML Response mit eingebettetem Chart
        chart_html = pio.to_html(
            go.Figure(data=data, layout=layout),
            include_plotlyjs="inline",
            config={"responsive": True, "displayModeBar": True, "displaylogo": False}
        )
        
        comparison_values = sorted(df[comparison_field].unique()) if comparison_field and comparison_field in df.columns else []
        
        return render_template("plot.html",
                             challenge_name=name,
                             activity_type=challenge.activity_type,
                             available_fields=available_fields,
                             numeric_fields=numeric_fields,
                             category_fields=category_fields,
                             comparison_features=comparison_features,
                             chart_html=chart_html,
                             chart_data={"data": data, "layout": layout},
                             chart_type=chart_type,
                             selected_fields=selected_fields,
                             selected_intensities=selected_intensities,
                             available_intensities=["gemütlich", "mittel", "stark"],
                             comparison_field=comparison_field,
                             comparison_values=comparison_values)
    
    except Exception as e:
        logger.exception(f"Error in handle_challenge_plot for {name}")
        if wants_json():
            return {"error": str(e)}, 500
        return redirect(url_for("handle_challenges", message=f"Fehler: {str(e)}"))


@app.get("/activities")
def handle_activities():
    """Alle Activities auflisten (JSON für React)"""
    try:
        logger.debug("GET /activities")
        activities = get_activity_names()
        # React erwartet {activities: [...]} Format
        return jsonify({"activities": activities}), 200
    except Exception as e:
        logger.exception("Error in GET /activities")
        return {"error": str(e)}, 500


@app.get("/activities/<activity_name>")
def handle_activity_fields(activity_name):
    """Felder für eine Activity auflisten (JSON für React)"""
    try:
        logger.debug(f"GET /activities/{activity_name}")
        if activity_name not in ACTIVITIES:
            return {"error": f"Unknown activity: {activity_name}"}, 404
        
        fields_raw = get_fields(activity_name)
        fields = [f.to_dict() if hasattr(f, "to_dict") else f for f in fields_raw]
        
        return jsonify({
            "activity": activity_name,
            "fields": fields
        }), 200
    except Exception as e:
        logger.exception(f"Error in GET /activities/{activity_name}")
        return {"error": str(e)}, 500


# ============================================================
# APP ENTRY POINT
# ============================================================

if __name__ == "__main__":
    logger.info("Starting Flask app on http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
