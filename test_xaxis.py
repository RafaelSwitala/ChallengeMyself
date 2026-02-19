#!/usr/bin/env python
import sys
sys.path.insert(0, 'backend')

import pandas as pd
from backend.utils.plotly_utils import sessions_to_dataframe, create_line_bar_chart_json

# Create test data spanning multiple months
sessions = [
    {'date': '2026-01-28', 'time': '18:00', 'values': {'distanz_km': 1.6, 'dauer_min': 19.0}},
    {'date': '2026-01-29', 'time': '18:00', 'values': {'distanz_km': 2.0, 'dauer_min': 21.0}},
    {'date': '2026-01-30', 'time': '18:00', 'values': {'distanz_km': 1.8, 'dauer_min': 20.0}},
    {'date': '2026-01-31', 'time': '18:00', 'values': {'distanz_km': 2.2, 'dauer_min': 22.0}},
    {'date': '2026-02-01', 'time': '18:00', 'values': {'distanz_km': 1.9, 'dauer_min': 21.0}},
    {'date': '2026-02-02', 'time': '18:00', 'values': {'distanz_km': 2.1, 'dauer_min': 23.0}},
    {'date': '2026-02-15', 'time': '18:00', 'values': {'distanz_km': 1.7, 'dauer_min': 20.0}},
    {'date': '2026-03-01', 'time': '18:00', 'values': {'distanz_km': 2.3, 'dauer_min': 24.0}},
]

df = sessions_to_dataframe(sessions)
result = create_line_bar_chart_json(
    df, 
    ['distanz_km'], 
    field_types={'distanz_km': 'line'}
)

print("X-axis configuration:")
print("tickvals:", result['layout']['xaxis'].get('tickvals'))
print("ticktext:", result['layout']['xaxis'].get('ticktext'))
print("\nAnnotations (month/year labels):")
for ann in result['layout'].get('annotations', []):
    print(f"  Position {ann['x']}: {ann['text']}")


