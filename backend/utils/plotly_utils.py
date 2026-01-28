import logging
import pandas as pd

logger = logging.getLogger(__name__)


def sessions_to_dataframe(sessions):
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


def create_line_chart_json(df: pd.DataFrame, fields: list[str], title: str = "") -> dict:
    try:
        data = []

        for f in fields:
            if f not in df.columns:
                continue

            data.append({
                "x": df["date"].tolist(),
                "y": df[f].tolist(),
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

    except Exception:
        logger.exception("Failed to create line chart JSON")
        return {"data": [], "layout": {}}
