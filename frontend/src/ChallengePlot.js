import { useState, useEffect } from "react";
import Plot from "react-plotly.js";
import "./ChallengePlot.css";

function ChallengePlot({ challengeName, availableFields }) {
  const [selectedFields, setSelectedFields] = useState([]);
  const [fieldChartTypes, setFieldChartTypes] = useState({});
  const [selectedEnumField, setSelectedEnumField] = useState("");
  const [dateRangeStart, setDateRangeStart] = useState("");
  const [dateRangeEnd, setDateRangeEnd] = useState("");
  const [useDualYAxis, setUseDualYAxis] = useState(false);
  const [secondYAxisFields, setSecondYAxisFields] = useState([]);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [yAxisMin, setYAxisMin] = useState("");
  const [yAxisMax, setYAxisMax] = useState("");
  const [yAxisStep, setYAxisStep] = useState("");
  const [xAxisStep, setXAxisStep] = useState(1);
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
      selectedFields.forEach((field) => {
        params.append(`field_type_${field}`, fieldChartTypes[field] || "line");
      });
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

      if (data.layout) {
        if (yAxisMin || yAxisMax) {
          data.layout.yaxis = data.layout.yaxis || {};
          if (yAxisMin) data.layout.yaxis.range = [parseFloat(yAxisMin), data.layout.yaxis.range?.[1] || null];
          if (yAxisMax) {
            const minVal = yAxisMin ? parseFloat(yAxisMin) : (data.layout.yaxis.range?.[0] || null);
            data.layout.yaxis.range = [minVal, parseFloat(yAxisMax)];
          }
          if (yAxisStep) {
            data.layout.yaxis.dtick = parseFloat(yAxisStep);
          }
        }

        if (xAxisStep > 1 && data.data.length > 0) {
          data.data = data.data.map((trace) => ({
            ...trace,
            x: trace.x ? trace.x.map((v, i) => (i % xAxisStep === 0 ? v : "")) : [],
          }));
        }

        data.layout.height = 700;
        data.layout.hovermode = "x unified";
        data.layout.showlegend = true;
        data.layout.legend = {
          orientation: "h",
          x: 0,
          y: -0.15,
          xanchor: "left",
          yanchor: "top",
        };
        data.layout.margin = { l: 80, r: 100, t: 50, b: 150 };

        data.data = data.data.map((trace) => {
          const chartType = fieldChartTypes[trace.name] || "line";
          
          if (selectedEnumField) {
            return { ...trace, type: "bar" };
          }

          if (chartType === "bar") {
            return {
              ...trace,
              type: "bar",
              hovertemplate: "<b>%{x|%Y-%m-%d}</b><br>" + 
                            "<b>" + trace.name + "</b><br>" +
                            "%{y:,.2f}<extra></extra>",
            };
          } else {
            return {
              ...trace,
              type: "scatter",
              mode: "lines+markers",
              hovertemplate: "<b>%{x|%Y-%m-%d}</b><br>" +
                            "<b>" + trace.name + "</b><br>" +
                            "%{y:,.2f}<extra></extra>",
            };
          }
        });
      }

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
    fieldChartTypes,
    selectedEnumField,
    dateRangeStart,
    dateRangeEnd,
    useDualYAxis,
    secondYAxisFields,
    yAxisMin,
    yAxisMax,
    yAxisStep,
    xAxisStep,
  ]);

  useEffect(() => {
    if (selectedFields.length > 1 && !selectedEnumField) {
      setUseDualYAxis(true);
    } else if (selectedFields.length <= 1) {
      setUseDualYAxis(false);
      setSecondYAxisFields([]);
    }
  }, [selectedFields, selectedEnumField]);

  const toggleField = (fieldName) => {
    setSelectedFields((prev) =>
      prev.includes(fieldName)
        ? prev.filter((f) => f !== fieldName)
        : [...prev, fieldName]
    );
    if (!fieldChartTypes[fieldName]) {
      setFieldChartTypes((prev) => ({ ...prev, [fieldName]: "line" }));
    }
    setSelectedEnumField("");
  };

  const toggleSecondYAxis = (fieldName) => {
    setSecondYAxisFields((prev) =>
      prev.includes(fieldName)
        ? prev.filter((f) => f !== fieldName)
        : [...prev, fieldName]
    );
  };

  const changeFieldChartType = (fieldName, chartType) => {
    setFieldChartTypes((prev) => ({ ...prev, [fieldName]: chartType }));
  };

  return (
    <div className="challenge-plot-container">
      <div className="plot-filters">
        <h3>Diagramm-Einstellungen</h3>

        {numericFields.length > 0 && !selectedEnumField && (
          <div className="filter-group">
            <label>Messwerte ({selectedFields.length} ausgewählt)</label>
            <div className="field-checkbox-group">
              {numericFields.map((f) => (
                <div key={f.name} className="field-with-type">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={selectedFields.includes(f.name)}
                      onChange={() => toggleField(f.name)}
                    />
                    <span>
                      {f.name} {f.unit && `(${f.unit})`}
                    </span>
                  </label>
                  {selectedFields.includes(f.name) && (
                    <select
                      className="chart-type-select"
                      value={fieldChartTypes[f.name] || "line"}
                      onChange={(e) => changeFieldChartType(f.name, e.target.value)}
                    >
                      <option value="line">Linie</option>
                      <option value="bar">Säule</option>
                    </select>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {enumFields.length > 0 && (
          <div className="filter-group">
            <label htmlFor="enumField">Nach Kategorie gruppieren</label>
            <select
              id="enumField"
              value={selectedEnumField}
              onChange={(e) => {
                setSelectedEnumField(e.target.value);
                setSelectedFields([]);
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

        {selectedFields.length > 1 && !selectedEnumField && useDualYAxis && (
          <div className="filter-group">
            <p className="small-text">
              Dual-Y-Axis active (automatically enabled with multiple metrics)
            </p>
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
          </div>
        )}

        {(selectedFields.length > 0 || selectedEnumField) && (
          <div className="filter-group scaling-controls">
            <h4>Achsen-Skalierung</h4>

            {selectedFields.length > 0 && (
              <div className="scaling-section">
                <label>Y-Achse (Werte)</label>
                <div className="scaling-inputs">
                  <div className="scaling-input">
                    <label htmlFor="yMin">Min:</label>
                    <input
                      id="yMin"
                      type="number"
                      value={yAxisMin}
                      onChange={(e) => setYAxisMin(e.target.value)}
                      placeholder="Auto"
                    />
                  </div>
                  <div className="scaling-input">
                    <label htmlFor="yMax">Max:</label>
                    <input
                      id="yMax"
                      type="number"
                      value={yAxisMax}
                      onChange={(e) => setYAxisMax(e.target.value)}
                      placeholder="Auto"
                    />
                  </div>
                  <div className="scaling-input">
                    <label htmlFor="yStep">Schritte:</label>
                    <input
                      id="yStep"
                      type="number"
                      step="0.1"
                      value={yAxisStep}
                      onChange={(e) => setYAxisStep(e.target.value)}
                      placeholder="Auto"
                    />
                  </div>
                </div>
              </div>
            )}

            <div className="scaling-section">
              <label htmlFor="xStep">X-Achse: Jeden n-ten Eintrag anzeigen</label>
              <input
                id="xStep"
                type="number"
                min="1"
                value={xAxisStep}
                onChange={(e) => setXAxisStep(Math.max(1, parseInt(e.target.value) || 1))}
                className="x-step-input"
              />
            </div>
          </div>
        )}
      </div>

      <div className="plot-chart-container">
        {loading && <div className="loading-spinner">Lädt...</div>}
        {chartData && selectedFields.length === 0 && !selectedEnumField && (
          <div className="empty-chart-message">
            <p>Bitte mindestens ein Messwert oder eine Kategorie auswählen</p>
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