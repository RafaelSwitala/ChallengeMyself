import logging
import pandas as pd
from typing import Optional, List

logger = logging.getLogger(__name__)


def sessions_to_dataframe(sessions):
    """Convert sessions list to pandas DataFrame."""
    try:
        data = []
        for s in sessions:
            row = {"date": s["date"], "time": s["time"], **s["values"]}
            data.append(row)

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        return df

    except Exception:
        logger.exception("Failed to convert sessions to DataFrame")
        return pd.DataFrame()


def filter_by_date_range(df: pd.DataFrame, date_from: Optional[str] = None, date_to: Optional[str] = None) -> pd.DataFrame:
    """Filter DataFrame by date range."""
    try:
        if date_from:
            df = df[df["date"] >= pd.to_datetime(date_from)]
        if date_to:
            df = df[df["date"] <= pd.to_datetime(date_to)]
        return df
    except Exception:
        logger.exception("Failed to filter by date range")
        return df


def create_line_chart_json(
    df: pd.DataFrame,
    fields: List[str],
    field_types: dict = None,
    title: str = "",
    secondary_y_fields: Optional[List[str]] = None,
) -> dict:
    """Create line chart JSON with support for dual Y-axis and mixed chart types.
    
    Args:
        df: DataFrame with session data
        fields: List of field names to plot
        field_types: Dict mapping field name to chart type ("line" or "bar")
        title: Chart title
        secondary_y_fields: Fields to display on secondary Y-axis
    """
    try:
        data = []
        layout = {
            "title": title or "Liniendiagramm",
            "xaxis": {"title": "Datum"},
            "yaxis": {"title": "Wert (links)"},
            "hovermode": "x unified",
            "height": 700,
            "legend": {
                "orientation": "h",
                "x": 0,
                "y": -0.15,
                "xanchor": "left",
                "yanchor": "top",
            },
            "margin": {"l": 80, "r": 100, "t": 50, "b": 150},
        }

        secondary_y_fields = secondary_y_fields or []
        field_types = field_types or {}

        for f in fields:
            if f not in df.columns:
                continue

            chart_type = field_types.get(f, "line")

            x_data = [pd.Timestamp(date).strftime("%Y-%m-%d") for date in df["date"].tolist()]

            trace = {
                "x": x_data,
                "y": df[f].tolist(),
                "name": f,
                "hovertemplate": (
                    f"<b>{f}</b>: %{y:,.2f}<extra></extra>"
                ),
                "hoverinfo": "y+name",
            }

            if chart_type == "bar":
                trace["type"] = "bar"
            else:
                trace["type"] = "scatter"
                trace["mode"] = "lines+markers"

            if f in secondary_y_fields:
                trace["yaxis"] = "y2"

            data.append(trace)

        if secondary_y_fields and any(f in secondary_y_fields for f in fields):
            layout["yaxis2"] = {
                "title": "Wert (rechts)",
                "overlaying": "y",
                "side": "right",
            }

        return {"data": data, "layout": layout}

    except Exception:
        logger.exception("Failed to create line chart JSON")
        return {"data": [], "layout": {}}


def create_bar_chart_json(df: pd.DataFrame, fields: List[str], field_types: dict = None, title: str = "") -> dict:
    """Create bar chart JSON with legend below."""
    try:
        data = []
        layout = {
            "title": title or "Säulendiagramm",
            "xaxis": {"title": "Datum"},
            "yaxis": {"title": "Wert"},
            "barmode": "group",
            "hovermode": "x unified",
            "height": 700,
            "legend": {
                "orientation": "h",
                "x": 0,
                "y": -0.15,
                "xanchor": "left",
                "yanchor": "top",
            },
            "margin": {"l": 80, "r": 100, "t": 50, "b": 150},
        }

        field_types = field_types or {}

        for f in fields:
            if f not in df.columns:
                continue

            x_data = [pd.Timestamp(date).strftime("%Y-%m-%d") for date in df["date"].tolist()]

            data.append({
                "x": x_data,
                "y": df[f].tolist(),
                "type": "bar",
                "name": f,
                "hovertemplate": (
                    f"<b>{f}</b>: %{y:,.2f}<extra></extra>"
                ),
                "hoverinfo": "y+name",
            })

        return {"data": data, "layout": layout}

    except Exception:
        logger.exception("Failed to create bar chart JSON")
        return {"data": [], "layout": {}}


def create_enum_bar_chart_json(df: pd.DataFrame, enum_field: str, title: str = "") -> dict:
    """Create bar chart counting occurrences of enum field values with legend below."""
    try:
        if enum_field not in df.columns:
            return {"data": [], "layout": {}}

        counts = df[enum_field].value_counts().sort_index()

        data = [{
            "x": counts.index.tolist(),
            "y": counts.values.tolist(),
            "type": "bar",
            "name": enum_field,
            "marker": {"color": "rgba(13, 110, 253, 0.7)"},
            "hovertemplate": "<b>%{x}</b>: %{y}<extra></extra>",
            "hoverinfo": "x+y",
        }]

        layout = {
            "title": title or f"Häufigkeitsverteilung: {enum_field}",
            "xaxis": {"title": enum_field},
            "yaxis": {"title": "Anzahl"},
            "hovermode": "x unified",
            "height": 700,
            "legend": {
                "orientation": "h",
                "x": 0,
                "y": -0.15,
                "xanchor": "left",
                "yanchor": "top",
            },
            "margin": {"l": 80, "r": 100, "t": 50, "b": 150},
        }

        return {"data": data, "layout": layout}

    except Exception:
        logger.exception(f"Failed to create enum bar chart for {enum_field}")
        return {"data": [], "layout": {}}
