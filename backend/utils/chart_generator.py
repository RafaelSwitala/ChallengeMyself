import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import logging
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)


def create_mixed_chart(
    df: pd.DataFrame,
    fields: List[str],
    field_types: Dict[str, str],
    secondary_y_fields: Optional[List[str]] = None,
    title: str = "",
    show_spines: bool = True
) -> go.Figure:
    try:
        secondary_y_fields = secondary_y_fields or []
        
        if secondary_y_fields:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
        else:
            fig = go.Figure()
        
        for field_name in fields:
            if field_name not in df.columns:
                continue
            
            chart_type = field_types.get(field_name, "line")
            is_secondary = field_name in secondary_y_fields
            
            x_data = [pd.Timestamp(date).strftime("%Y-%m-%d") for date in df["date"].tolist()]
            y_data = df[field_name].tolist()
            
            if chart_type == "bar":
                trace = go.Bar(
                    x=x_data,
                    y=y_data,
                    name=field_name,
                    hovertemplate="<b>%{x}</b><br><b>" + field_name + "</b><br>%{y:,.2f}<extra></extra>",
                    secondary_y=is_secondary
                )
            else:  # line
                trace = go.Scatter(
                    x=x_data,
                    y=y_data,
                    name=field_name,
                    mode="lines+markers",
                    hovertemplate="<b>%{x}</b><br><b>" + field_name + "</b><br>%{y:,.2f}<extra></extra>",
                    secondary_y=is_secondary
                )
            
            if secondary_y_fields:
                fig.add_trace(trace, secondary_y=is_secondary)
            else:
                fig.add_trace(trace)
        
        layout_update = {
            "title": title or "Chart",
            "height": 700,
            "hovermode": "x unified",
            "showlegend": True,
            "legend": {
                "orientation": "h",
                "x": 0,
                "y": -0.15,
                "xanchor": "left",
                "yanchor": "top"
            },
            "margin": {"l": 80, "r": 100, "t": 50, "b": 150}
        }
        
        if show_spines:
            layout_update["xaxis"] = {
                "title": "Date",
                "showgrid": True,
                "showline": True,
                "linewidth": 2,
                "linecolor": "black"
            }
            layout_update["yaxis"] = {
                "title": "Value (left)",
                "showgrid": True,
                "showline": True,
                "linewidth": 2,
                "linecolor": "black"
            }
            if secondary_y_fields:
                layout_update["yaxis2"] = {
                    "title": "Value (right)",
                    "showgrid": False,
                    "showline": True,
                    "linewidth": 2,
                    "linecolor": "black"
                }
        else:
            layout_update["xaxis"] = {"title": "Date"}
            layout_update["yaxis"] = {"title": "Value (left)"}
            if secondary_y_fields:
                layout_update["yaxis2"] = {"title": "Value (right)"}
        
        fig.update_layout(**layout_update)
        
        return fig
    
    except Exception as e:
        logger.exception("Error creating mixed chart: %s", e)
        raise


def create_enum_chart(
    df: pd.DataFrame,
    enum_field: str,
    title: str = "",
    show_spines: bool = True
) -> go.Figure:
    try:
        if enum_field not in df.columns:
            raise ValueError(f"Field '{enum_field}' not found in DataFrame")
        
        counts = df[enum_field].value_counts().sort_index()
        
        fig = go.Figure(data=[
            go.Bar(
                x=counts.index.tolist(),
                y=counts.values.tolist(),
                name=enum_field,
                marker={"color": "rgba(13, 110, 253, 0.7)"},
                hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>"
            )
        ])
        
        layout_update = {
            "title": title or f"Distribution: {enum_field}",
            "xaxis": {"title": enum_field},
            "yaxis": {"title": "Count"},
            "height": 700,
            "hovermode": "x unified",
            "showlegend": True,
            "legend": {
                "orientation": "h",
                "x": 0,
                "y": -0.15,
                "xanchor": "left",
                "yanchor": "top"
            },
            "margin": {"l": 80, "r": 100, "t": 50, "b": 150}
        }
        
        # Configure axes with spines
        if show_spines:
            layout_update["xaxis"].update({
                "showline": True,
                "linewidth": 2,
                "linecolor": "black"
            })
            layout_update["yaxis"].update({
                "showline": True,
                "linewidth": 2,
                "linecolor": "black"
            })
        
        fig.update_layout(**layout_update)
        
        return fig
    
    except Exception as e:
        logger.exception("Error creating enum chart: %s", e)
        raise


def apply_axis_scaling(
    fig: go.Figure,
    y_min: Optional[float] = None,
    y_max: Optional[float] = None,
    y_step: Optional[float] = None,
    x_step: int = 1
) -> go.Figure:
    try:
        # Apply Y-axis scaling
        if y_min is not None or y_max is not None or y_step is not None:
            y_range = None
            if y_min is not None and y_max is not None:
                y_range = [y_min, y_max]
            elif y_min is not None:
                y_range = [y_min, None]
            elif y_max is not None:
                y_range = [None, y_max]
            
            y_update = {}
            if y_range:
                y_update["range"] = y_range
            if y_step is not None:
                y_update["dtick"] = y_step
            
            if y_update:
                fig.update_yaxes(y_update)
        
        if x_step > 1:
            for i, trace in enumerate(fig.data):
                if hasattr(trace, 'x') and trace.x:
                    new_x = [x if j % x_step == 0 else "" for j, x in enumerate(trace.x)]
                    fig.data[i].x = new_x
        
        return fig
    
    except Exception as e:
        logger.exception("Error applying axis scaling: %s", e)
        raise
