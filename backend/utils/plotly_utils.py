import plotly.express as px
import pandas as pd

def sessions_to_dataframe(sessions):
    """
    Wandelt eine Liste von Session-Objekten in ein DataFrame um.
    sessions: List[Session] oder List[dict]
    """
    data = []
    for s in sessions:
        row = {"date": s["date"], "time": s["time"], **s["values"]}
        data.append(row)
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df

def create_line_chart(sessions, y_field, title=None):
    df = sessions_to_dataframe(sessions)
    if y_field not in df.columns:
        return None

    fig = px.line(df, x="date", y=y_field, markers=True, title=title or y_field)
    return fig.to_json()

def create_line_chart_json(df: pd.DataFrame, fields: list[str], title: str = "") -> dict:
    """
    Erstellt ein Plotly-kompatibles JSON aus einem DataFrame für mehrere Linien.
    df: DataFrame mit Spalten 'date' + die zu plottenden Felder
    fields: Liste der Spaltennamen, die geplottet werden sollen
    """
    data = []

    for f in fields:
        if f not in df.columns:
            continue
        y_vals = df[f].tolist() if hasattr(df[f], "tolist") else list(df[f])
        x_vals = df["date"].tolist() if hasattr(df["date"], "tolist") else list(df["date"])
        data.append({
            "x": x_vals,
            "y": y_vals,
            "type": "scatter",
            "mode": "lines+markers",
            "name": f
        })

    layout = {
        "title": title,
        "xaxis": {"title": "Datum"},
        "yaxis": {"title": "Wert"},
        "hovermode": "closest"
    }

    return {"data": data, "layout": layout}
