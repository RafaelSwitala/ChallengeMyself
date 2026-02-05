import { useState, useEffect } from "react";
import Plot from "react-plotly.js";
import "./ChallengePlot.css";

function ChallengePlot({ challengeName, availableFields }) {
  const [selectedFields, setSelectedFields] = useState([]);
  const [selectedChartType, setSelectedChartType] = useState("line");
  const [selectedEnumField, setSelectedEnumField] = useState("");
  const [dateRangeStart, setDateRangeStart] = useState("");
  const [dateRangeEnd, setDateRangeEnd] = useState("");
  const [useDualYAxis, setUseDualYAxis] = useState(false);
  const [secondYAxisFields, setSecondYAxisFields] = useState([]);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);

  // Separate numeric and enum fields
  const numericFields = availableFields.filter(
    (f) => f.type === "number" && f.chart_type !== "none" && !f.hidden
  );
  const enumFields = availableFields.filter(
    (f) => f.type === "enum" && f.chart_type === "enum_bar" && !f.hidden
  );

  const loadData = async () => {
    if (selectedFields.length === 0 && !selectedEnumField) {
      setChartData(null);
      return;
    }

    setLoading(true);

    const params = new URLSearchParams();

    if (selectedEnumField) {
      params.append("enum_field", selectedEnumField);
      params.append("chart_type", "enum_bar");
    } else {
      params.append("fields", selectedFields.join(","));
      params.append("chart_type", selectedChartType);
    }

    if (dateRangeStart) params.append("date_from", dateRangeStart);
    if (dateRangeEnd) params.append("date_to", dateRangeEnd);
    if (useDualYAxis && secondYAxisFields.length > 0) {
      params.append("secondary_y_fields", secondYAxisFields.join(","));
    }

    try {
      const res = await fetch(
        `http://localhost:5000/challenges/${encodeURIComponent(challengeName)}/plot?${params.toString()}`
      );
      const data = await res.json();

      // Configure chart type
      if (selectedEnumField || selectedChartType === "bar") {
        data.layout.barmode = "group";
        data.data = data.data.map((d) => ({ ...d, type: "bar" }));
      } else {
        data.data = data.data.map((d) => ({
          ...d,
          type: "scatter",
          mode: "lines+markers",
          hovertemplate: "%{x}<br>%{y:,.2f}<extra></extra>",
        }));
      }

      // Make chart responsive and larger
      data.layout.height = 600;
      data.layout.hovermode = "x unified";
      data.layout.showlegend = true;
      data.layout.margin = { l: 80, r: 100, t: 50, b: 80 };

      setChartData(data);
    } catch (error) {
      console.error("Error loading chart data:", error);
      setChartData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [
    selectedFields,
    selectedEnumField,
    selectedChartType,
    dateRangeStart,
    dateRangeEnd,
    useDualYAxis,
    secondYAxisFields,
  ]);

  const toggleField = (fieldName) => {
    setSelectedFields((prev) =>
      prev.includes(fieldName)
        ? prev.filter((f) => f !== fieldName)
        : [...prev, fieldName]
    );
    setSelectedEnumField(""); // Clear enum when switching to numeric
  };

  const toggleSecondYAxis = (fieldName) => {
    setSecondYAxisFields((prev) =>
      prev.includes(fieldName)
        ? prev.filter((f) => f !== fieldName)
        : [...prev, fieldName]
    );
  };

  return (
    <div className="challenge-plot-container">
      {/* Filters Section */}
      <div className="plot-filters">
        <h3>📊 Diagramm-Einstellungen</h3>

        {/* Chart Type Selection */}
        <div className="filter-group">
          <label htmlFor="chartType">Diagramm-Typ</label>
          <select
            id="chartType"
            value={selectedChartType}
            onChange={(e) => {
              setSelectedChartType(e.target.value);
              setSelectedEnumField("");
              setSelectedFields([]); // Reset fields on type change
            }}
          >
            <option value="line">📈 Liniendiagramm</option>
            <option value="bar">📊 Säulendiagramm</option>
          </select>
        </div>

        {/* Numeric Fields */}
        {numericFields.length > 0 && !selectedEnumField && (
          <div className="filter-group">
            <label>Messwerte ({selectedFields.length} ausgewählt)</label>
            <div className="field-checkbox-group">
              {numericFields.map((f) => (
                <label key={f.name} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={selectedFields.includes(f.name)}
                    onChange={() => toggleField(f.name)}
                  />
                  <span>{f.name}</span>
                  {f.unit && <small>({f.unit})</small>}
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Enum Fields */}
        {enumFields.length > 0 && (
          <div className="filter-group">
            <label htmlFor="enumField">Nach Kategorie gruppieren</label>
            <select
              id="enumField"
              value={selectedEnumField}
              onChange={(e) => {
                setSelectedEnumField(e.target.value);
                setSelectedFields([]); // Clear numeric fields
              }}
            >
              <option value="">-- Keine --</option>
              {enumFields.map((f) => (
                <option key={f.name} value={f.name}>
                  {f.name}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Date Range Filter */}
        <div className="filter-group date-range">
          <label htmlFor="dateStart">Zeitraum</label>
          <div className="date-inputs">
            <input
              id="dateStart"
              type="date"
              value={dateRangeStart}
              onChange={(e) => setDateRangeStart(e.target.value)}
              placeholder="Von"
            />
            <span className="dash">–</span>
            <input
              id="dateEnd"
              type="date"
              value={dateRangeEnd}
              onChange={(e) => setDateRangeEnd(e.target.value)}
              placeholder="Bis"
            />
          </div>
        </div>

        {/* Dual Y-Axis Option */}
        {selectedFields.length > 1 && !selectedEnumField && selectedChartType === "line" && (
          <div className="filter-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={useDualYAxis}
                onChange={(e) => {
                  setUseDualYAxis(e.target.checked);
                  if (!e.target.checked) setSecondYAxisFields([]);
                }}
              />
              <span>Dual-Y-Achse aktivieren</span>
            </label>

            {useDualYAxis && (
              <div className="secondary-y-fields">
                <p className="small-text">Felder auf rechter Y-Achse:</p>
                {selectedFields.map((fieldName) => (
                  <label key={fieldName} className="checkbox-label small">
                    <input
                      type="checkbox"
                      checked={secondYAxisFields.includes(fieldName)}
                      onChange={() => toggleSecondYAxis(fieldName)}
                    />
                    <span>{fieldName}</span>
                  </label>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Chart Display */}
      <div className="plot-chart-container">
        {loading && <div className="loading-spinner">Lädt...</div>}
        {chartData && !selectedEnumField && selectedFields.length === 0 && (
          <div className="empty-chart-message">
            <p>👈 Bitte mindestens ein Messwert oder eine Kategorie auswählen</p>
          </div>
        )}
        {chartData && (
          <Plot
            data={chartData.data}
            layout={chartData.layout}
            config={{ responsive: true, displayModeBar: true }}
          />
        )}
      </div>
    </div>
  );
}

export default ChallengePlot;