import logging
import pandas as pd
from typing import Optional, List
from datetime import datetime, timedelta

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


def filter_by_value_range(df: pd.DataFrame, field: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> pd.DataFrame:
    """Filter DataFrame by value range for a specific field."""
    try:
        if field not in df.columns:
            return df
        
        if min_val is not None:
            df = df[df[field] >= min_val]
        if max_val is not None:
            df = df[df[field] <= max_val]
        return df
    except Exception:
        logger.exception(f"Failed to filter by value range for {field}")
        return df


def filter_by_category(df: pd.DataFrame, category_field: str, value: str) -> pd.DataFrame:
    """Filter DataFrame by category field value."""
    try:
        if category_field not in df.columns:
            return df
        return df[df[category_field] == value]
    except Exception:
        logger.exception(f"Failed to filter by category {category_field}={value}")
        return df


def filter_every_nth_entry(df: pd.DataFrame, n: int) -> pd.DataFrame:
    """Keep only every nth entry in the DataFrame."""
    try:
        if n <= 1:
            return df
        return df.iloc[::n]
    except Exception:
        logger.exception(f"Failed to filter every {n}th entry")
        return df


def generate_grid_positions(dates: List[pd.Timestamp], grid_mode: str) -> List[dict]:
    """
    Generate grid line positions based on mode.
    
    Args:
        dates: List of date values
        grid_mode: "none", "daily", "weekly", or "monthly"
    
    Returns:
        List of grid line dictionaries with numeric x value and label
    """
    try:
        if grid_mode == "none" or not dates:
            return []
        
        positions = []
        
        if grid_mode == "daily":
            # Add grid line for each unique date
            unique_dates = sorted(set(d.date() if hasattr(d, 'date') else d for d in dates))
            # Find indices of first occurrence of each unique date
            for unique_date in unique_dates:
                for idx, d in enumerate(dates):
                    d_date = d.date() if hasattr(d, 'date') else d
                    if d_date == unique_date:
                        positions.append({"x": idx, "label": unique_date.isoformat()})
                        break
        
        elif grid_mode == "weekly":
            # Add grid line for each Monday
            min_date = min(d.date() if hasattr(d, 'date') else d for d in dates)
            max_date = max(d.date() if hasattr(d, 'date') else d for d in dates)
            
            # Find first Monday
            days_until_monday = (7 - min_date.weekday()) % 7
            current = min_date + timedelta(days=days_until_monday)
            
            while current <= max_date:
                # Find first index >= current date
                for idx, d in enumerate(dates):
                    d_date = d.date() if hasattr(d, 'date') else d
                    if d_date >= current:
                        positions.append({
                            "x": idx,
                            "label": f"Week of {current.isoformat()}"
                        })
                        break
                current += timedelta(days=7)
        
        elif grid_mode == "monthly":
            # Add grid line for first day of each month
            min_date = min(d.date() if hasattr(d, 'date') else d for d in dates)
            max_date = max(d.date() if hasattr(d, 'date') else d for d in dates)
            
            current = min_date.replace(day=1)
            while current <= max_date:
                # Find first index >= current date
                for idx, d in enumerate(dates):
                    d_date = d.date() if hasattr(d, 'date') else d
                    if d_date >= current:
                        positions.append({
                            "x": idx,
                            "label": f"{current.strftime('%B %Y')}"
                        })
                        break
                # Move to next month
                if current.month == 12:
                    current = current.replace(year=current.year + 1, month=1)
                else:
                    current = current.replace(month=current.month + 1)
        
        return positions
    except Exception:
        logger.exception(f"Failed to generate grid positions for mode {grid_mode}")
        return []


def format_x_axis_labels(dates: List[pd.Timestamp], show_every_nth: int = 1) -> tuple:
    """
    Format X-axis labels with day numbers and month labels below.
    
    Returns:
        Tuple of (day_labels, month_labels, month_positions)
    """
    try:
        if not dates or show_every_nth < 1:
            return [], {}, []
        
        formatted_dates = []
        month_ranges = {}  # Track month positions
        
        for i, date in enumerate(dates):
            if i % show_every_nth == 0:
                day = date.day
                month_key = date.strftime("%b")  # "Jan", "Feb", etc.
                
                formatted_dates.append(date.strftime("%Y-%m-%d"))
                
                # Track month positions
                if month_key not in month_ranges:
                    month_ranges[month_key] = {"start": i, "end": i}
                month_ranges[month_key]["end"] = i
            else:
                formatted_dates.append("")
        
        return formatted_dates, month_ranges
    except Exception:
        logger.exception("Failed to format X-axis labels")
        return [], {}


def format_x_axis_day_based(dates: List[pd.Timestamp], skip_every_n: int = 3) -> tuple:
    """
    Format X-axis with day-of-month labels at intervals and month/year labels below.
    
    Shows day numbers at every nth entry (e.g., every 3rd day) for readability,
    with month/year labels positioned below at the first day of each month.
    
    Args:
        dates: List of date values
        skip_every_n: Show day label every n entries (default: 3)
    
    Returns:
        Tuple of (tickvals, ticktext, monthyear_annotations)
    """
    try:
        if not dates:
            return [], [], []
        
        tickvals = []  # Positions where day labels should appear
        ticktext = []  # Day numbers as text
        month_annotations = []  # Month/year annotations
        
        prev_month = None
        
        for i, date in enumerate(dates):
            ts = pd.Timestamp(date)
            day = ts.day
            month = ts.month
            month_year = ts.strftime("%b %Y")  # "Jan 2026"
            
            # Show day label every nth entry
            if i % skip_every_n == 0:
                tickvals.append(i)
                ticktext.append(str(day))
            
            # Add month/year annotation at first day of each month
            if month != prev_month:
                month_annotations.append({
                    "x": i,
                    "y": -0.25,  # Below the chart and day labels
                    "xref": "x",
                    "yref": "paper",
                    "text": month_year,
                    "showarrow": False,
                    "xanchor": "center",
                    "yanchor": "top",
                    "font": {"size": 12, "color": "#666", "family": "Arial"},
                })
                prev_month = month
        
        return tickvals, ticktext, month_annotations
    except Exception:
        logger.exception("Failed to format X-axis day-based labels")
        return [], [], []


def create_line_bar_chart_json(
    df: pd.DataFrame,
    fields: List[str],
    field_types: dict = None,
    title: str = "",
    secondary_y_fields: Optional[List[str]] = None,
    show_every_nth: int = 1,
    grid_mode: str = "none",
) -> dict:
    """
    Create enhanced line chart JSON with improved formatting.
    
    Features:
    - Dual Y-axis support
    - Mixed chart types (line + bar)
    - Improved X-axis labels with day numbers and month below
    - Simplified tooltips (no duplicate dates)
    - Dark blue lines, orange/light orange bars, green secondary bars
    - Proper grid lines
    
    Args:
        df: DataFrame with session data
        fields: List of field names to plot
        field_types: Dict mapping field name to chart type ("line" or "bar")
        title: Chart title
        secondary_y_fields: Fields to display on secondary Y-axis
        show_every_nth: Show every nth entry on X-axis
        grid_mode: Grid line mode ("none", "daily", "weekly", "monthly")
    """
    try:
        if df.empty or not fields:
            return {"data": [], "layout": {}}
        
        # Filter to every nth entry
        df_filtered = filter_every_nth_entry(df, show_every_nth)
        if df_filtered.empty:
            return {"data": [], "layout": {}}
        
        data = []
        
        # Prepare X-axis data - Use numeric indices with day-of-month labels
        x_dates = df_filtered["date"].tolist()
        x_indices = list(range(len(x_dates)))  # Use 0, 1, 2, 3... as X values
        
        # Format X-axis with day numbers and month/year annotations
        tickvals, ticktext, annotations = format_x_axis_day_based(x_dates)
        
        # Create layout with improved X-axis
        layout = {
            "title": title or "Chart Analysis",
            "xaxis": {
                "title": "Date",
                # Use array mode to show all dates with custom labels
                "tickmode": "array",  # Manual tick positioning
                "tickvals": tickvals,  # Positions of ticks
                "ticktext": ticktext,  # Day-of-month labels (29, 30, 31, 1, 2, ...)
                "tickangle": -45,
            },
            "yaxis": {
                "title": "Value (Left)",
                "showgrid": True,
                "gridcolor": "#e0e0e0",
                "zeroline": False,
            },
            # Important for multiple bars to appear side-by-side
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
            "margin": {"l": 80, "r": 100, "t": 50, "b": 180},  # Increased for day + month labels
            "plot_bgcolor": "white",
            "annotations": annotations,  # Add month/year labels
        }
        
        secondary_y_fields = secondary_y_fields or []
        field_types = field_types or {}
        
        # Color palette
        colors = {
            "line": "darkblue",        # Dark blue for lines
            "bar_primary": "#FF9500",  # Orange for first bar
            "bar_secondary": "#90EE90", # Light green for second bar
        }
        
        # Track bar position for alternating colors
        bar_count = 0
        
        for i, field in enumerate(fields):
            if field not in df_filtered.columns:
                continue
            
            chart_type = field_types.get(field, "line")
            is_secondary = field in secondary_y_fields
            
            trace = {
                "x": x_indices,  # Use numeric indices
                "y": df_filtered[field].tolist(),
                "name": field,
                "hovertemplate": f"<b>{field}</b>: %{{y:.2f}}<extra></extra>",
                "hoverinfo": "y+name",
            }
            
            if chart_type == "bar":
                trace["type"] = "bar"
                # Alternate between orange and light green for multiple bar charts
                if bar_count % 2 == 0:
                    trace["marker"] = {"color": colors["bar_primary"], "opacity": 0.8}
                else:
                    trace["marker"] = {"color": colors["bar_secondary"], "opacity": 0.8}
                bar_count += 1
            else:
                trace["type"] = "scatter"
                trace["mode"] = "lines+markers"
                trace["line"] = {"color": colors["line"], "width": 2}
                trace["marker"] = {"size": 6, "color": colors["line"]}
            
            if is_secondary:
                trace["yaxis"] = "y2"
            
            data.append(trace)
        
        # Add secondary Y-axis if needed
        if secondary_y_fields and any(f in secondary_y_fields for f in fields):
            layout["yaxis2"] = {
                "title": "Value (Right)",
                "overlaying": "y",
                "side": "right",
                "showgrid": False,
            }
        
        # Add grid lines if requested
        if grid_mode != "none":
            grid_positions = generate_grid_positions(x_dates, grid_mode)
            if grid_positions:
                layout["shapes"] = [
                    {
                        "type": "line",
                        "x0": pos["x"],
                        "x1": pos["x"],
                        "y0": 0,
                        "y1": 1,
                        "yref": "paper",
                        "line": {"color": "#d0d0d0", "width": 1, "dash": "dash"},
                    }
                    for pos in grid_positions
                ]
        
        # Make axes bold and black
        layout["xaxis"]["showline"] = True
        layout["xaxis"]["linewidth"] = 2
        layout["xaxis"]["linecolor"] = "black"
        layout["yaxis"]["showline"] = True
        layout["yaxis"]["linewidth"] = 2
        layout["yaxis"]["linecolor"] = "black"
        
        if "yaxis2" in layout:
            layout["yaxis2"]["showline"] = True
            layout["yaxis2"]["linewidth"] = 2
            layout["yaxis2"]["linecolor"] = "black"
        
        return {"data": data, "layout": layout}
    
    except Exception:
        logger.exception("Failed to create enhanced line chart JSON")
        return {"data": [], "layout": {}}


# Backward compatibility alias
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
    return create_line_bar_chart_json(df, fields, field_types, title, secondary_y_fields)


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
                    "<b>" + f + "</b>: %{y:,.2f}<extra></extra>"
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
