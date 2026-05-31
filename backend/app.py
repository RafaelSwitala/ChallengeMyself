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
    get_comparison_features, calculate_hidden_fields, get_available_goal_types
)
from storage.json_storage import save_challenge, load_challenge, list_challenges
import plotly.graph_objects as go
import plotly.io as pio
import os
import numpy as np

setup_logging()
logger = get_logger(__name__)

app = Flask(__name__, template_folder="templates")
CORS(app, resources={r"/*": {"origins": "*"}}, send_wildcard=True)



@app.after_request
def add_cors_headers(response):
    response.headers.setdefault("Access-Control-Allow-Origin", "*")
    response.headers.setdefault("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.setdefault("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response


@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        from flask import make_response
        resp = make_response(('', 204))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return resp


@app.errorhandler(Exception)
def handle_exception(e):
    from flask import make_response
    logger.exception("Unhandled exception: %s", e)
    body = {"error": "internal server error", "message": str(e)}
    resp = make_response(jsonify(body), 500)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return resp

def wants_json():
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return True
    if request.content_type and "application/json" in request.content_type:
        return True
    if request.headers.get('Origin'):
        return True
    if 'application/json' in request.accept_mimetypes:
        return True
    return False

@app.get("/debug/list-files")
def debug_list_files():
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
    logger.debug(f"handle_challenges: {request.method} path={request.path}")
    
    if request.method == "GET":
        try:
            challenge_list = list_challenges()
            challenges = []
            
            for ch in challenge_list:
                challenge = load_challenge(ch["name"])
                if challenge:
                    challenges.append(challenge.to_dict())
            
            if request.path == "/challenges":
                logger.debug(f"GET /challenges -> JSON ({len(challenges)} challenges)")
                return jsonify(challenges), 200
            
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
    try:
        from storage.json_storage import _path
        
        logger.debug(f"DELETE /challenge/{name}")
        
        challenge = load_challenge(name)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        
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
    try:
        from storage.json_storage import _path
        
        logger.debug(f"PUT /challenge/{old_name}")
        
        if not request.is_json:
            return {"error": "Request body must be JSON"}, 400
        
        payload = request.get_json()
        new_name = payload.get("new_name", "").strip()
        
        if not new_name:
            return {"error": "new_name is required"}, 400
        
        old_challenge = load_challenge(old_name)
        if not old_challenge:
            return {"error": "Challenge not found"}, 404
        
        if new_name != old_name and load_challenge(new_name):
            return {"error": f"Challenge with name '{new_name}' already exists"}, 409
        
        if old_name != new_name:
            old_path = _path(old_name)
            if os.path.exists(old_path):
                os.remove(old_path)
                logger.debug(f"Old file removed: {old_path}")
        
        old_challenge.name = new_name
        
        save_challenge(old_challenge)
        logger.info(f"Challenge renamed: {old_name} → {new_name}")
        
        return jsonify(old_challenge.to_dict()), 200
        
    except Exception as e:
        logger.exception(f"Error renaming challenge {old_name}")
        return {"error": str(e)}, 500



@app.route("/challenges/<name>/plot", methods=["GET"])
def handle_challenge_plot(name):
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
            fields_param = request.args.get("fields", "")
            enum_field = request.args.get("enum_field", "")
            date_from = request.args.get("date_from", "")
            date_to = request.args.get("date_to", "")
            secondary_y_fields_param = request.args.get("secondary_y_fields", "")
            show_every_nth = int(request.args.get("show_every_nth", 1))
            grid_mode = request.args.get("grid_mode", "none")
            selected_fields = [f.strip() for f in fields_param.split(",") if f.strip()] if fields_param else []
            secondary_y_fields = [f.strip() for f in secondary_y_fields_param.split(",") if f.strip()] if secondary_y_fields_param else []
            
            field_types = {}
            for field in selected_fields:
                chart_type_param = request.args.get(f"field_type_{field}", "line")
                field_types[field] = chart_type_param
            
            df = sessions_to_dataframe([s.to_dict() for s in challenge.sessions])
            if df.empty:
                return {"error": "No valid session data"}, 400
            
            df = filter_by_date_range(df, date_from, date_to)
            if df.empty:
                return {"error": "No sessions in date range"}, 400
            
            for field in selected_fields:
                min_val_param = request.args.get(f"{field}_min")
                max_val_param = request.args.get(f"{field}_max")
                min_val = float(min_val_param) if min_val_param else None
                max_val = float(max_val_param) if max_val_param else None
                df = filter_by_value_range(df, field, min_val, max_val)
            
            for key, value in request.args.items():
                if key.startswith("filter_"):
                    category_field = key[7:]
                    df = filter_by_category(df, category_field, value)
            
            if df.empty:
                return {"error": "No data matching the filters"}, 400
            
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
    try:
        challenge = load_challenge(name)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        
        payload = request.get_json() if request.is_json else request.form
        logger.info(f"DEBUG: Received payload for session: {payload}")
        
        date = payload.get("date", "")
        time = payload.get("time", "")
        
        if not date or not time:
            return {"error": "date und time erforderlich"}, 400
        
        field_values = payload.get("values", {}) if isinstance(payload.get("values"), dict) else {}
        
        values = {}
        fields = get_fields(challenge.activity_type)
        logger.info(f"DEBUG: Available fields for {challenge.activity_type}: {[f['name'] if isinstance(f, dict) else f.key for f in fields]}")
        
        for field in fields:
            field_name = field["name"] if isinstance(field, dict) else field.key
            # Try multiple possible names for the same field
            val = field_values.get(field_name) or payload.get(field_name)
            
            if val is not None and val != "":
                field_type = field["type"] if isinstance(field, dict) else field.field_type.value
                if field_type == "number":
                    try:
                        values[field_name] = float(val)
                    except (ValueError, TypeError):
                        values[field_name] = val
                else:
                    values[field_name] = val
        
        logger.info(f"DEBUG: Collected values: {values}")
        
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
    try:
        print("DEBUG ACTIVITIES:", get_activity_names())
        logger.debug("GET /activities")
        activities = get_activity_names()
        return jsonify({"activities": activities}), 200
    except Exception as e:
        logger.exception("Error in GET /activities")
        return {"error": str(e)}, 500


@app.get("/activities/<activity_name>")
def handle_activity_fields(activity_name):
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
    try:
        from flask import request
        
        logger.debug(f"GET /challenges/{name}/goal/progress")
        challenge = load_challenge(name)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        
        if not challenge.goal:
            return {"error": "No goal set for this challenge"}, 400
        
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



@app.get("/activities/<activity>/goal-types")
def handle_activity_goal_types(activity):
    """Get alle verfügbaren GoalTypes für eine Aktivität"""
    try:
        logger.debug(f"GET /activities/{activity}/goal-types")
        
        if activity not in ACTIVITIES:
            return {"error": f"Unknown activity: {activity}"}, 404
        
        available_types = get_available_goal_types(activity)
        
        return jsonify({
            "activity": activity,
            "available_goal_types": available_types
        }), 200
    except Exception as e:
        logger.exception(f"Error in GET /activities/{activity}/goal-types")
        return {"error": str(e)}, 500


@app.get("/challenges/<name>/goal-types")
def handle_get_challenge_goal_types(name):
    """Get alle GoalTypes für eine Challenge"""
    try:
        logger.debug(f"GET /challenges/{name}/goal-types")
        
        challenge = load_challenge(name)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        
        goal_types = [gt.to_dict() for gt in challenge.goal_types]
        
        return jsonify({
            "challenge": name,
            "goal_types": goal_types
        }), 200
    except Exception as e:
        logger.exception(f"Error in GET /challenges/{name}/goal-types")
        return {"error": str(e)}, 500


@app.post("/challenges/<name>/goal-types")
def handle_add_goal_type(name):
    """Add einen GoalType zu einer Challenge"""
    try:
        logger.debug(f"POST /challenges/{name}/goal-types")
        
        challenge = load_challenge(name)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        
        payload = request.get_json()
        if not payload or "type" not in payload:
            return {"error": "Goal type data required"}, 400
        
        from models.goal_types import (
            MoreThanGoal, FrequencyMinGoal, AverageAboveGoal, 
            RecurrencePatternGoal
        )
        
        goal_type_name = payload.get("type")
        
        try:
            if goal_type_name == "MORE_THAN":
                goal_type = MoreThanGoal(
                    target_value=float(payload.get("target_value", 0)),
                    period=payload.get("period", "monthly"),
                    unit=payload.get("unit", "km"),
                    metric=payload.get("metric", "distance")
                )
            elif goal_type_name == "FREQUENCY_MIN":
                goal_type = FrequencyMinGoal(
                    min_sessions=int(payload.get("min_sessions", 0)),
                    period=payload.get("period", "weekly")
                )
            elif goal_type_name == "AVERAGE_ABOVE":
                goal_type = AverageAboveGoal(
                    target_average=float(payload.get("target_average", 0)),
                    metric=payload.get("metric", "duration"),
                    unit=payload.get("unit", "minutes")
                )
            elif goal_type_name == "RECURRENCE_PATTERN":
                goal_type = RecurrencePatternGoal(
                    days_of_week=payload.get("days_of_week", [])
                )
            else:
                return {"error": f"Unknown goal type: {goal_type_name}"}, 400
            
            if not goal_type.is_valid():
                return {"error": f"Invalid goal type data for {goal_type_name}"}, 400
            
            challenge.add_goal_type(goal_type)
            save_challenge(challenge)
            
            logger.info(f"Goal type {goal_type_name} added to {name}")
            return jsonify(challenge.to_dict()), 201
        
        except Exception as e:
            logger.exception(f"Error creating goal type")
            return {"error": str(e)}, 400
    
    except Exception as e:
        logger.exception(f"Error in POST /challenges/{name}/goal-types")
        return {"error": str(e)}, 500


@app.delete("/challenges/<name>/goal-types/<goal_type_name>")
def handle_delete_goal_type(name, goal_type_name):
    """Remove einen GoalType aus einer Challenge"""
    try:
        logger.debug(f"DELETE /challenges/{name}/goal-types/{goal_type_name}")
        
        challenge = load_challenge(name)
        if not challenge:
            return {"error": "Challenge not found"}, 404
        
        from models.goal_types import (
            MoreThanGoal, FrequencyMinGoal, AverageAboveGoal, 
            RecurrencePatternGoal
        )
        
        goal_type_map = {
            "MORE_THAN": MoreThanGoal,
            "FREQUENCY_MIN": FrequencyMinGoal,
            "AVERAGE_ABOVE": AverageAboveGoal,
            "RECURRENCE_PATTERN": RecurrencePatternGoal
        }
        
        if goal_type_name not in goal_type_map:
            return {"error": f"Unknown goal type: {goal_type_name}"}, 400
        
        challenge.remove_goal_type(goal_type_map[goal_type_name])
        save_challenge(challenge)
        
        logger.info(f"Goal type {goal_type_name} removed from {name}")
        return jsonify(challenge.to_dict()), 200
    
    except Exception as e:
        logger.exception(f"Error in DELETE /challenges/{name}/goal-types/{goal_type_name}")
        return {"error": str(e)}, 500


if __name__ == "__main__":
    logger.info("Starting Flask app on http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000, use_reloader=False, threaded=True)