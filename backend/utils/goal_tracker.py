"""
Goal Tracking Module

Provides goal definition schemas and progress calculation logic for each activity.
Handles goal validation, progress calculation, and status determination.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class GoalDefinition:
    """
    Defines allowed goal configurations for a specific activity.
    
    Attributes:
        activity_name (str): Name of the activity
        allowed_references (List[str]): Field references that can be tracked
        reference_units (Dict[str, str]): Units for each reference
        allowed_periods (List[str]): Valid period types
        status_types (List[str]): Possible status values
    """
    
    def __init__(
        self,
        activity_name: str,
        allowed_references: List[str],
        reference_units: Dict[str, str],
        allowed_periods: List[str],
        status_types: List[str]
    ):
        self.activity_name = activity_name
        self.allowed_references = allowed_references
        self.reference_units = reference_units
        self.allowed_periods = allowed_periods
        self.status_types = status_types

    def validate_goal(self, reference: str, period: str) -> bool:
        """
        Validate if goal configuration is allowed for this activity.
        
        Args:
            reference (str): Field reference to track
            period (str): Time period
            
        Returns:
            bool: True if valid, False otherwise
        """
        return (
            reference in self.allowed_references and
            period in self.allowed_periods
        )


# Goal definitions for each activity
GOAL_DEFINITIONS = {
    "Laufen": GoalDefinition(
        activity_name="Laufen",
        allowed_references=["distanz_km", "dauer_min"],
        reference_units={"distanz_km": "km", "dauer_min": "min"},
        allowed_periods=["daily", "weekly", "monthly", "date_range", "yearly"],
        status_types=["in_progress", "completed", "not_completed", "consecutive_days"]
    ),
    # "Radfahren": GoalDefinition(
    #     activity_name="Radfahren",
    #     allowed_references=["distanz_km", "dauer_min"],
    #     reference_units={"distanz_km": "km", "dauer_min": "min"},
    #     allowed_periods=["daily", "weekly", "monthly", "date_range", "yearly"],
    #     status_types=["in_progress", "completed", "not_completed", "consecutive_days"]
    # ),
    # "Spazieren": GoalDefinition(
    #     activity_name="Spazieren",
    #     allowed_references=["distanz_km", "dauer_min"],
    #     reference_units={"distanz_km": "km", "dauer_min": "min"},
    #     allowed_periods=["daily", "weekly", "monthly", "date_range", "yearly"],
    #     status_types=["in_progress", "completed", "not_completed", "consecutive_days"]
    # ),
    # "Schwimmen": GoalDefinition(
    #     activity_name="Schwimmen",
    #     allowed_references=["distanz_m", "dauer_min"],
    #     reference_units={"distanz_m": "m", "dauer_min": "min"},
    #     allowed_periods=["daily", "weekly", "monthly", "date_range", "yearly"],
    #     status_types=["in_progress", "completed", "not_completed", "consecutive_days"]
    # ),
    # "Workout": GoalDefinition(
    #     activity_name="Workout",
    #     allowed_references=["dauer_min", "uebungen_anzahl"],
    #     reference_units={"dauer_min": "min", "uebungen_anzahl": "reps"},
    #     allowed_periods=["daily", "weekly", "monthly", "date_range", "yearly"],
    #     status_types=["in_progress", "completed", "not_completed", "consecutive_days"]
    # ),
    # "Liegestutze": GoalDefinition(
    #     activity_name="Liegestutze",
    #     allowed_references=["dauer_min", "uebungen_anzahl"],
    #     reference_units={"dauer_min": "min", "uebungen_anzahl": "reps"},
    #     allowed_periods=["daily", "weekly", "monthly", "date_range", "yearly"],
    #     status_types=["in_progress", "completed", "not_completed", "consecutive_days"]
    # ),
    # "Lesen": GoalDefinition(
    #     activity_name="Lesen",
    #     allowed_references=["dauer_min", "seiten_anzahl"],
    #     reference_units={"dauer_min": "min", "seiten_anzahl": "pages"},
    #     allowed_periods=["daily", "weekly", "monthly", "date_range", "yearly"],
    #     status_types=["in_progress", "completed", "not_completed", "consecutive_days"]
    # ),
    # "Lernen": GoalDefinition(
    #     activity_name="Lernen",
    #     allowed_references=["dauer_min"],
    #     reference_units={"dauer_min": "min"},
    #     allowed_periods=["daily", "weekly", "monthly", "date_range", "yearly"],
    #     status_types=["in_progress", "completed", "not_completed", "consecutive_days"]
    # ),
    # "Schlaf": GoalDefinition(
    #     activity_name="Schlaf",
    #     allowed_references=["dauer_stunden"],
    #     reference_units={"dauer_stunden": "hours"},
    #     allowed_periods=["daily", "weekly"],
    #     status_types=["too_short", "too_long", "in_range"]
    # ),
    # "Bildschirmzeit": GoalDefinition(
    #     activity_name="Bildschirmzeit",
    #     allowed_references=["dauer_min", "dauer_min_average"],
    #     reference_units={"dauer_min": "min", "dauer_min_average": "min"},
    #     allowed_periods=["daily", "weekly"],
    #     status_types=["too_high", "in_range"]
    # ),
    # "Wasser": GoalDefinition(
    #     activity_name="Wasser",
    #     allowed_references=["menge_ml"],
    #     reference_units={"menge_ml": "ml"},
    #     allowed_periods=["daily", "weekly"],
    #     status_types=["too_low", "sufficient"]
    # ),
    # "Alkohol": GoalDefinition(
    #     activity_name="Alkohol",
    #     allowed_references=["menge_ml"],
    #     reference_units={"menge_ml": "ml"},
    #     allowed_periods=["weekly", "monthly", "yearly"],
    #     status_types=["too_high", "within_goal"]
    # ),
    # "Rauchen": GoalDefinition(
    #     activity_name="Rauchen",
    #     allowed_references=["anzahl_pro_tag", "abstand_min"],
    #     reference_units={"anzahl_pro_tag": "cigs", "abstand_min": "min"},
    #     allowed_periods=["daily", "weekly"],
    #     status_types=["too_high", "within_goal"]
    # ),
    # "Events": GoalDefinition(
    #     activity_name="Events",
    #     allowed_references=["kosten"],
    #     reference_units={"kosten": "EUR"},
    #     allowed_periods=["monthly", "yearly"],
    #     status_types=["too_high", "within_goal"]
    # ),
}

# Activities with no goals
NO_GOAL_ACTIVITIES = ["Stimmung", "Stress", "Energielevel", "Motivation"]


def get_goal_definition(activity_name: str) -> Optional[GoalDefinition]:
    """
    Get goal definition for an activity.
    
    Args:
        activity_name (str): Name of activity
        
    Returns:
        Optional[GoalDefinition]: Goal definition or None if activity has no goals
    """
    return GOAL_DEFINITIONS.get(activity_name)


def supports_goals(activity_name: str) -> bool:
    """
    Check if activity supports goals.
    
    Args:
        activity_name (str): Name of activity
        
    Returns:
        bool: True if activity supports goals
    """
    if activity_name in NO_GOAL_ACTIVITIES:
        return False
    return activity_name in GOAL_DEFINITIONS


def calculate_progress(
    sessions: List[Dict[str, Any]],
    goal_reference: str,
    goal_target: float,
    goal_period: str,
    activity_name: str,
    selected_date: str = None
) -> Dict[str, Any]:
    """
    Calculate progress towards a goal based on sessions with period filtering.
    
    Args:
        sessions (List[Dict]): List of session dictionaries with 'date' and 'values'
        goal_reference (str): Field reference to track (e.g., 'distance_km')
        goal_target (float): Target value
        goal_period (str): Period type (daily, weekly, monthly, yearly, date_range)
        activity_name (str): Activity name
        selected_date (str): Optional date for filtering (YYYY-MM-DD for daily, YYYY-MM for monthly)
        
    Returns:
        Dict: Progress data including current value, status, message, consecutive_days
    """
    try:
        from datetime import datetime, timedelta
        
        if not sessions:
            goal_def = GOAL_DEFINITIONS.get(activity_name, {})
            unit = goal_def.reference_units.get(goal_reference, "") if goal_def else ""
            return {
                "current": 0,
                "target": goal_target,
                "status": "in_progress",
                "message": "Noch keine Daten",
                "unit": unit,
                "consecutive_days": 0,
                "period_label": goal_period
            }
        
        # Get goal definition for units
        goal_def = GOAL_DEFINITIONS.get(activity_name, {})
        unit = goal_def.reference_units.get(goal_reference, "") if goal_def else ""
        
        # Filter sessions by period
        filtered_sessions = _filter_sessions_by_period(sessions, goal_period, selected_date)
        
        if not filtered_sessions:
            return {
                "current": 0,
                "target": goal_target,
                "status": "in_progress",
                "message": f"Keine Daten für diesen Zeitraum",
                "unit": unit,
                "consecutive_days": 0,
                "period_label": goal_period,
                "selected_period": selected_date or _get_current_period_label(goal_period)
            }
        
        # Sum up values for the reference field
        total = 0
        for session in filtered_sessions:
            values = session.get("values", {})
            if goal_reference in values:
                try:
                    val = float(values[goal_reference])
                    total += val
                except (ValueError, TypeError):
                    continue
        
        # Calculate consecutive days if period is daily
        consecutive_days = 0
        if goal_period == "daily":
            consecutive_days = _count_consecutive_goal_days(sessions, goal_reference, goal_target)
        
        # Determine status
        remaining = goal_target - total
        
        if total >= goal_target:
            status = "completed"
            message = f"Ziel erreicht: {total:.1f} {unit} von {goal_target:.1f} {unit}"
        elif total >= goal_target * 0.85:
            status = "in_progress"
            message = f"Noch {remaining:.1f} {unit} bis zum Ziel ({total:.1f} von {goal_target:.1f} {unit})"
        else:
            status = "in_progress"
            message = f"Aktueller Fortschritt: {total:.1f} {unit} von {goal_target:.1f} {unit}"
        
        period_label = _get_period_label(goal_period, selected_date)
        
        result = {
            "current": round(total, 1),
            "target": goal_target,
            "status": status,
            "message": message,
            "unit": unit,
            "consecutive_days": consecutive_days,
            "period_label": period_label
        }
        
        if selected_date:
            result["selected_period"] = selected_date
        
        return result
        
    except Exception as e:
        logger.exception(f"Error calculating progress: {e}")
        return {
            "current": 0,
            "target": goal_target,
            "status": "error",
            "message": "Fehler bei Fortschrittsberechnung",
            "unit": "",
            "consecutive_days": 0,
            "period_label": goal_period
        }


def _filter_sessions_by_period(
    sessions: List[Dict[str, Any]],
    period: str,
    selected_date: str = None
) -> List[Dict[str, Any]]:
    """
    Filter sessions based on period type.
    
    Args:
        sessions: List of sessions with 'date' field
        period: Period type (daily, weekly, monthly, yearly, date_range)
        selected_date: For daily/monthly - the selected date (YYYY-MM-DD or YYYY-MM)
        
    Returns:
        List of filtered sessions
    """
    from datetime import datetime, timedelta
    
    if not sessions:
        return []
    
    today = datetime.now().date()
    
    if period == "daily":
        # Filter for today or selected date
        target_date = selected_date
        if not target_date:
            target_date = today.strftime("%Y-%m-%d")
        return [s for s in sessions if s.get("date") == target_date]
    
    elif period == "weekly":
        # Filter for current week (Monday to Sunday)
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        filtered = []
        for s in sessions:
            try:
                session_date = datetime.strptime(s.get("date", ""), "%Y-%m-%d").date()
                if start_of_week <= session_date <= end_of_week:
                    filtered.append(s)
            except ValueError:
                continue
        return filtered
    
    elif period == "monthly":
        # Filter for selected month or current month
        if not selected_date:
            selected_date = today.strftime("%Y-%m")
        # selected_date should be YYYY-MM
        filtered = []
        for s in sessions:
            session_month = s.get("date", "")[:7]  # Extract YYYY-MM
            if session_month == selected_date:
                filtered.append(s)
        return filtered
    
    elif period == "yearly":
        # Filter for current year
        target_year = today.strftime("%Y")
        filtered = []
        for s in sessions:
            session_year = s.get("date", "")[:4]  # Extract YYYY
            if session_year == target_year:
                filtered.append(s)
        return filtered
    
    else:
        # date_range or unknown - return all sessions
        return sessions


def _count_consecutive_goal_days(
    sessions: List[Dict[str, Any]],
    goal_reference: str,
    goal_target: float
) -> int:
    """
    Count consecutive days where goal was achieved.
    
    Args:
        sessions: List of sessions
        goal_reference: Field to track
        goal_target: Target value for goal
        
    Returns:
        Number of consecutive days ending today where goal was met
    """
    from datetime import datetime, timedelta
    
    if not sessions:
        return 0
    
    # Group sessions by date
    sessions_by_date = {}
    for session in sessions:
        date_str = session.get("date", "")
        if date_str:
            if date_str not in sessions_by_date:
                sessions_by_date[date_str] = []
            sessions_by_date[date_str].append(session)
    
    # Check which dates met the goal
    goal_dates = set()
    for date_str, day_sessions in sessions_by_date.items():
        daily_total = 0
        for s in day_sessions:
            values = s.get("values", {})
            if goal_reference in values:
                try:
                    daily_total += float(values[goal_reference])
                except (ValueError, TypeError):
                    continue
        
        if daily_total >= goal_target:
            goal_dates.add(date_str)
    
    if not goal_dates:
        return 0
    
    # Sort dates and count consecutive days from today backwards
    sorted_dates = sorted(goal_dates)
    today = datetime.now().date()
    
    consecutive_count = 0
    current_date = today
    
    # Check backwards from today
    while True:
        date_str = current_date.strftime("%Y-%m-%d")
        if date_str in goal_dates:
            consecutive_count += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return consecutive_count


def _get_period_label(period: str, selected_date: str = None) -> str:
    """Get a human-readable label for the period."""
    from datetime import datetime
    
    if period == "daily":
        if selected_date:
            return f"Tag: {selected_date}"
        return f"Heute: {datetime.now().strftime('%Y-%m-%d')}"
    
    elif period == "weekly":
        return f"Diese Woche"
    
    elif period == "monthly":
        if selected_date:
            try:
                dt = datetime.strptime(selected_date, "%Y-%m")
                month_names = ["", "Januar", "Februar", "März", "April", "Mai", "Juni",
                              "Juli", "August", "September", "Oktober", "November", "Dezember"]
                return f"{month_names[dt.month]} {dt.year}"
            except:
                return selected_date
        return f"Dieser Monat ({datetime.now().strftime('%Y-%m')})"
    
    elif period == "yearly":
        return f"Dieses Jahr"
    
    return period


def _get_current_period_label(period: str) -> str:
    """Get the current period identifier."""
    from datetime import datetime
    
    today = datetime.now().date()
    
    if period == "daily":
        return today.strftime("%Y-%m-%d")
    elif period == "monthly":
        return today.strftime("%Y-%m")
    elif period == "yearly":
        return today.strftime("%Y")
    
    return None
