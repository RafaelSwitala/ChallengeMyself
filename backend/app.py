"""
ChallengeMyself Flask REST API Server

This module implements the backend REST API for the ChallengeMyself application.
It provides endpoints for:
- Challenge management (create, list, retrieve)
- Session management (add, list)
- Goal management (set, delete)
- Activity definitions (list fields)
- Charting and data visualization

The API supports both HTML (for browser views) and JSON (for React frontend).
All endpoints include comprehensive error handling and logging.
"""

from utils.logger import setup_logging, get_logger
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import pandas as pd
from models.challenge import Challenge
from models.session import Session
from models.goal import Goal
from models.activities import (
    ACTIVITIES, get_activity_names, get_fields, get_field_objects,
    get_numeric_fields, get_category_fields, get_field_unit,
    get_comparison_features, calculate_hidden_fields
)
from storage.json_storage import save_challenge, load_challenge, list_challenges
import plotly.graph_objects as go
import plotly.io as pio
import os
import numpy as np

# Initialize logging configuration
setup_logging()
logger = get_logger(__name__)

# Initialize Flask app with CORS support for frontend communication
app = Flask(__name__, template_folder="templates")
CORS(app, resources={r"/*": {"origins": "*"}}, send_wildcard=True)



@app.after_request
def add_cors_headers(response):
    """
    Add CORS headers to all responses (even errors).
    
    This ensures that the React frontend can communicate with the Flask backend
    from different origins (localhost:3000 to localhost:5000).
    
    Returns:
        Flask Response: Response object with CORS headers attached
    """
    response.headers.setdefault("Access-Control-Allow-Origin", "*")
    response.headers.setdefault("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.setdefault("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response


@app.before_request
def handle_options():
    """
    Handle preflight OPTIONS requests from browsers.
    
    Browsers send an OPTIONS request before making actual requests to check CORS permissions.
    This function returns early with proper CORS headers for these requests.
    
    Returns:
        Tuple[str, int]: Empty response with status 204 No Content
    """
    if request.method == 'OPTIONS':
        from flask import make_response
        resp = make_response(('', 204))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return resp


@app.errorhandler(Exception)
def handle_exception(e):
    """
    Global error handler for unhandled exceptions.
    
    Catches any exception not caught by specific handlers, logs it with full traceback,
    and returns a JSON error response with CORS headers.
    
    Args:
        e (Exception): The exception that was raised
        
    Returns:
        Tuple[Dict, int]: JSON error response with status 500
    """
    from flask import make_response
    logger.exception("Unhandled exception: %s", e)
    body = {"error": "internal server error", "message": str(e)}
    resp = make_response(jsonify(body), 500)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return resp

def wants_json():
    """
    Determine if the client wants JSON response instead of HTML.
    
    Checks multiple indicators:
    - Accept header explicitly requests JSON
    - Content-Type indicates JSON
    - Origin header indicates CORS request (from frontend)
    
    Returns:
        bool: True if JSON is preferred, False if HTML is preferred
    """
    # Check if JSON is explicitly requested in Accept header
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return True
    # Check if Content-Type is JSON
    if request.content_type and "application/json" in request.content_type:
        return True
    # Check if this is a CORS request from a different origin (frontend)
    # CORS requests should always return JSON
    if request.headers.get('Origin'):
        return True
    # If Accept header is not set, check if application/json is in the accept_mimetypes
    # This handles cases where the client sends application/json with lower priority
    if 'application/json' in request.accept_mimetypes:
        return True
    return False

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

@app.route("/", methods=["GET"])
@app.route("/challenges", methods=["GET", "POST"])
def handle_challenges():
    """
    Smart Router für Challenges:
    - GET /challenges: Always returns JSON (for API/Frontend)
    - GET /: Returns HTML (for browser viewing)
    - POST /challenges: Creates challenge, returns JSON or redirects
    """
    logger.debug(f"handle_challenges: {request.method} path={request.path}")
    
    if request.method == "GET":
        try:
            challenge_list = list_challenges()
            challenges = []
            
            for ch in challenge_list:
                challenge = load_challenge(ch["name"])
                if challenge:
                    challenges.append(challenge.to_dict())
            
            # GET /challenges always returns JSON (it's the API endpoint)
            if request.path == "/challenges":
                logger.debug(f"GET /challenges -> JSON ({len(challenges)} challenges)")
                return jsonify(challenges), 200
            
            # GET / returns HTML (for browser)
            logger.debug(f"GET / -> HTML ({len(challenges)} challenges)")
            activities = get_activity_names()
            message = request.args.get("message", "")
            return render_template("index.html", challenges=challenges, activities=activities, message=message)
            
        except Exception as e:
            logger.exception("Error in GET /challenges")
            if request.path == "/challenges":
                return {"error": str(e)}, 500
            return render_template("index.html", challenges=[], activities=[], message=f"Fehler: {str(e)}")
    
    if request.method == "POST":
        try:
            if request.is_json:
                data = request.get_json()
                name = data.get("name", "").strip()
                activity = data.get("activity", "").strip()
                
                if not name or not activity:
                    return {"error": "name und activity erforderlich"}, 400
                if activity not in ACTIVITIES:
                    return {"error": f"Unknown activity: {activity}"}, 400
                if load_challenge(name):
                    return {"error": f"Challenge mit dem Namen '{name}' existiert bereits. Bitte wählen Sie einen anderen Namen."}, 400
                
                challenge = Challenge(name, activity)
                save_challenge(challenge)
                logger.info(f"Challenge created (JSON): {name}")
                return jsonify(challenge.to_dict()), 201
            
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
        
        if request.method == "GET":
            if wants_json():
                logger.debug(f"GET /challenges/{name} -> JSON")
                return jsonify(challenge.to_dict()), 200
            else:
                logger.debug(f"GET /challenges/{name} -> HTML")
                fields = get_fields(challenge.activity_type)
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
        
        if request.method == "POST":
            logger.debug(f"POST /challenges/{name}")
            payload = request.get_json() if request.is_json else request.form
            
            if "date" in payload and "time" in payload:
                date = payload.get("date", "")
                time = payload.get("time", "")
                
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
                
                hidden_values = calculate_hidden_fields(challenge.activity_type, values)
                values.update(hidden_values)
                
                session = Session(date, time, values)
                challenge.add_session(session)
                save_challenge(challenge)
                logger.info(f"Session added to {name}")
                
                if wants_json():
                    return jsonify(challenge.to_dict()), 200
                return redirect(url_for("handle_challenge_detail", name=name))
            
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



@app.delete("/challenge/<name>")
def delete_challenge(name):
    """
    DELETE /challenge/<name>
    
    Deletes a challenge completely, including removing the associated JSON file.
    
    Args:
        name (str): Challenge name to delete
        
    Returns:
        Tuple[Dict, int]: JSON response with success message or error
    """
    try:
        from storage.json_storage import _path
        
        logger.debug(f"DELETE /challenge/{name}")
        
        # Load challenge first to verify it exists
        challenge = load_challenge(name)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        
        # Remove the JSON file
        file_path = _path(name)
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Challenge deleted: {name} (file removed)")
        
        return {"message": f"Challenge '{name}' successfully deleted"}, 200
        
    except Exception as e:
        logger.exception(f"Error deleting challenge {name}")
        return {"error": str(e)}, 500


@app.put("/challenge/<old_name>")
def rename_challenge(old_name):
    """
    PUT /challenge/<old_name>
    
    Renames a challenge. Accepts JSON payload with new_name field.
    Updates the JSON filename and the name field within the file.
    
    Payload:
        {
            "new_name": "New Challenge Name"
        }
    
    Args:
        old_name (str): Current challenge name
        
    Returns:
        Tuple[Dict, int]: JSON response with updated challenge or error
    """
    try:
        from storage.json_storage import _path
        
        logger.debug(f"PUT /challenge/{old_name}")
        
        # Get payload
        if not request.is_json:
            return {"error": "Request body must be JSON"}, 400
        
        payload = request.get_json()
        new_name = payload.get("new_name", "").strip()
        
        if not new_name:
            return {"error": "new_name is required"}, 400
        
        # Load old challenge
        old_challenge = load_challenge(old_name)
        if not old_challenge:
            return {"error": "Challenge not found"}, 404
        
        # Check if new name already exists
        if new_name != old_name and load_challenge(new_name):
            return {"error": f"Challenge with name '{new_name}' already exists"}, 409
        
        # Delete old file first if names differ
        if old_name != new_name:
            old_path = _path(old_name)
            if os.path.exists(old_path):
                os.remove(old_path)
                logger.debug(f"Old file removed: {old_path}")
        
        # Update challenge name in the object
        old_challenge.name = new_name
        
        # Save with new name (will create file with new name)
        save_challenge(old_challenge)
        logger.info(f"Challenge renamed: {old_name} → {new_name}")
        
        return jsonify(old_challenge.to_dict()), 200
        
    except Exception as e:
        logger.exception(f"Error renaming challenge {old_name}")
        return {"error": str(e)}, 500



@app.route("/challenges/<name>/plot", methods=["GET"])
def handle_challenge_plot(name):
    """
    Enhanced plot handler with comprehensive filtering and chart options.
    
    Query parameters:
    - fields: Comma-separated field names to plot
    - field_type_<field>: "line" or "bar" for each field
    - secondary_y_fields: Comma-separated fields for right Y-axis
    - date_from, date_to: Date range filtering
    - show_every_nth: Show every nth entry on X-axis
    - grid_mode: "none", "daily", "weekly", or "monthly"
    - <field>_min, <field>_max: Value range filters
    - filter_<category>: Category filter (e.g., filter_weather=sunny)
    
    Returns:
        JSON with plotly chart data and layout
    """
    try:
        from utils.plotly_utils import (
            sessions_to_dataframe, filter_by_date_range,
            filter_by_value_range, filter_by_category,
            create_line_bar_chart_json, create_enum_bar_chart_json
        )
        
        challenge = load_challenge(name)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        
        if not challenge.sessions:
            return {"error": "No sessions available"}, 400
        
        try:
            # Get basic parameters
            fields_param = request.args.get("fields", "")
            enum_field = request.args.get("enum_field", "")
            date_from = request.args.get("date_from", "")
            date_to = request.args.get("date_to", "")
            secondary_y_fields_param = request.args.get("secondary_y_fields", "")
            show_every_nth = int(request.args.get("show_every_nth", 1))
            grid_mode = request.args.get("grid_mode", "none")
            
            selected_fields = [f.strip() for f in fields_param.split(",") if f.strip()] if fields_param else []
            secondary_y_fields = [f.strip() for f in secondary_y_fields_param.split(",") if f.strip()] if secondary_y_fields_param else []
            
            # Get field types
            field_types = {}
            for field in selected_fields:
                chart_type_param = request.args.get(f"field_type_{field}", "line")
                field_types[field] = chart_type_param
            
            # Convert sessions to DataFrame
            df = sessions_to_dataframe([s.to_dict() for s in challenge.sessions])
            if df.empty:
                return {"error": "No valid session data"}, 400
            
            # Apply date range filter
            df = filter_by_date_range(df, date_from, date_to)
            if df.empty:
                return {"error": "No sessions in date range"}, 400
            
            # Apply value range filters for each field
            for field in selected_fields:
                min_val_param = request.args.get(f"{field}_min")
                max_val_param = request.args.get(f"{field}_max")
                min_val = float(min_val_param) if min_val_param else None
                max_val = float(max_val_param) if max_val_param else None
                df = filter_by_value_range(df, field, min_val, max_val)
            
            # Apply category filters
            for key, value in request.args.items():
                if key.startswith("filter_"):
                    category_field = key[7:]  # Remove "filter_" prefix
                    df = filter_by_category(df, category_field, value)
            
            if df.empty:
                return {"error": "No data matching the filters"}, 400
            
            # Create chart
            if enum_field and enum_field in df.columns:
                result = create_enum_bar_chart_json(df, enum_field, title=f"{challenge.name} – {enum_field}")
            else:
                result = create_line_bar_chart_json(
                    df, 
                    selected_fields, 
                    field_types=field_types,
                    title=f"{challenge.name} – Analysis",
                    secondary_y_fields=secondary_y_fields if secondary_y_fields else None,
                    show_every_nth=show_every_nth,
                    grid_mode=grid_mode
                )
            
            return jsonify(result), 200
        
        except ValueError as e:
            logger.error(f"Invalid parameter value: {e}")
            return {"error": f"Invalid parameter: {str(e)}"}, 400
        except Exception as e:
            logger.exception(f"Error processing chart request")
            return {"error": str(e)}, 500
    
    except Exception as e:
        logger.exception(f"Error in handle_challenge_plot for {name}")
        return {"error": str(e)}, 500


@app.post("/challenges/<name>/sessions")
def handle_add_session(name):
    """POST API: Neue Session hinzufügen (für React Frontend)"""
    try:
        challenge = load_challenge(name)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        
        payload = request.get_json() if request.is_json else request.form
        date = payload.get("date", "")
        time = payload.get("time", "")
        
        if not date or not time:
            return {"error": "date und time erforderlich"}, 400
        
        field_values = payload.get("values", {}) if isinstance(payload.get("values"), dict) else {}
        
        values = {}
        fields = get_fields(challenge.activity_type)
        for field in fields:
            field_name = field["name"]
            val = field_values.get(field_name) or payload.get(field_name)
            if val is not None and val != "":
                field_type = field["type"]
                if field_type == "number":
                    try:
                        values[field_name] = float(val)
                    except (ValueError, TypeError):
                        values[field_name] = val
                else:
                    values[field_name] = val
        
        hidden_values = calculate_hidden_fields(challenge.activity_type, values)
        values.update(hidden_values)
        
        session = Session(date, time, values)
        challenge.add_session(session)
        save_challenge(challenge)
        logger.info(f"Session added to {name}")
        
        return jsonify(challenge.to_dict()), 201
        
    except Exception as e:
        logger.exception(f"Error adding session to {name}")
        return {"error": str(e)}, 500


@app.post("/challenges/<name>/goal")
def handle_set_goal(name):
    """
    POST API: Set or delete goal for a challenge (for React Frontend).
    
    New goal structure includes:
    - description: Human-readable goal description
    - reference: Field to track (e.g., 'distance_km')
    - target: Target value
    - period: Time period (daily, weekly, monthly, date range, etc.)
    """
    try:
        challenge = load_challenge(name)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        
        if request.args.get("delete"):
            challenge.goal = None
            save_challenge(challenge)
            logger.info(f"Goal deleted for {name}")
            return jsonify(challenge.to_dict()), 200
        
        payload = request.get_json() if request.is_json else request.form
        description = payload.get("description", "")
        reference = payload.get("reference")
        target = payload.get("target", "")
        period = payload.get("period", "")
        
        if not description or not target or not period:
            return {"error": "description, target, period erforderlich"}, 400
        
        try:
            goal = Goal(
                description=description,
                target=float(target),
                period=period,
                reference=reference
            )
            challenge.set_goal(goal)
            save_challenge(challenge)
            logger.info(f"Goal set for {name} with reference {reference}")
            return jsonify(challenge.to_dict()), 200
        except Exception as e:
            logger.exception(f"Error creating goal")
            return {"error": str(e)}, 400
            
    except Exception as e:
        logger.exception(f"Error in handle_set_goal for {name}")
        return {"error": str(e)}, 500


@app.get("/activities")
def handle_activities():
    """Alle Activities auflisten (JSON für React)"""
    try:
        logger.debug("GET /activities")
        activities = get_activity_names()
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


@app.get("/activities/<activity_name>/goals")
def handle_activity_goals(activity_name):
    """
    Get goal configuration for an activity.
    
    Returns allowed references, periods, and status types for goal creation.
    """
    try:
        from utils.goal_tracker import get_goal_definition, supports_goals
        
        logger.debug(f"GET /activities/{activity_name}/goals")
        
        if not supports_goals(activity_name):
            return {"error": f"Activity '{activity_name}' does not support goals"}, 400
        
        goal_def = get_goal_definition(activity_name)
        if not goal_def:
            return {"error": f"Goal definition not found for {activity_name}"}, 404
        
        return jsonify({
            "activity": activity_name,
            "allowed_references": goal_def.allowed_references,
            "reference_units": goal_def.reference_units,
            "allowed_periods": goal_def.allowed_periods,
            "status_types": goal_def.status_types
        }), 200
    except Exception as e:
        logger.exception(f"Error in GET /activities/{activity_name}/goals")
        return {"error": str(e)}, 500


@app.get("/challenges/<name>/goal/progress")
def handle_goal_progress(name):
    """
    Get current progress towards goal.
    
    Query parameters:
    - selected_date: For daily goals, use format YYYY-MM-DD; for monthly, use YYYY-MM
    
    Returns current value, target, status, and progress message.
    """
    try:
        from flask import request
        
        logger.debug(f"GET /challenges/{name}/goal/progress")
        challenge = load_challenge(name)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        
        if not challenge.goal:
            return {"error": "No goal set for this challenge"}, 400
        
        # Get optional selected_date query parameter
        selected_date = request.args.get('selected_date', None)
        
        progress = challenge.get_goal_progress(selected_date=selected_date)
        
        return jsonify({
            "challenge": name,
            "goal": challenge.goal.to_dict(),
            "progress": progress
        }), 200
    except Exception as e:
        logger.exception(f"Error in GET /challenges/{name}/goal/progress")
        return {"error": str(e)}, 500


if __name__ == "__main__":
    logger.info("Starting Flask app on http://127.0.0.1:5000")
    app.run(debug=False, host="127.0.0.1", port=5000, use_reloader=False, threaded=True)
