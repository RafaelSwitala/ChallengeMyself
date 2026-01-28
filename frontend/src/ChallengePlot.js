import { useState, useEffect } from "react";
import Plot from "react-plotly.js";

function ChallengePlot({ challengeName, availableFields }) {
  const [selectedFields, setSelectedFields] = useState([]);
  const [selectedChartType, setSelectedChartType] = useState("line"); // line oder bar
  const [selectedIntensities, setSelectedIntensities] = useState([]);
  const [chartData, setChartData] = useState(null);

  const intensities = ["gemuetlich", "mittel", "stark"];

  const loadData = async () => {
    if (selectedFields.length === 0) {
      setChartData(null);
      return;
    }

    const params = new URLSearchParams();
    params.append("fields", selectedFields.join(","));
    if (selectedIntensities.length > 0) {
      params.append("intensities", selectedIntensities.join(","));
    }

    const res = await fetch(
      `http://localhost:5000/challenges/${encodeURIComponent(
        challengeName
      )}/plot?${params.toString()}`
    );
    const data = await res.json();

    // Bei Säulen: barmode auf 'group' setzen
    if (selectedChartType === "bar") {
      data.layout.barmode = "group";
      data.data = data.data.map((d) => ({ ...d, type: "bar" }));
    } else {
      data.data = data.data.map((d) => ({ ...d, type: "scatter", mode: "lines+markers" }));
    }

    setChartData(data);
  };

  useEffect(() => {
    loadData();
  }, [selectedFields, selectedIntensities, selectedChartType]);

  const toggleField = (fieldName) => {
    setSelectedFields((prev) =>
      prev.includes(fieldName)
        ? prev.filter((f) => f !== fieldName)
        : [...prev, fieldName]
    );
  };

  const toggleIntensity = (intensity) => {
    setSelectedIntensities((prev) =>
      prev.includes(intensity)
        ? prev.filter((i) => i !== intensity)
        : [...prev, intensity]
    );
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <h4>Filter</h4>
      <div>
        <strong>Chart-Typ:</strong>
        <select value={selectedChartType} onChange={(e) => setSelectedChartType(e.target.value)} style={{ marginLeft: "10px" }}>
          <option value="line">Liniendiagramm</option>
          <option value="bar">Säulendiagramm</option>
        </select>
      </div>

      <div style={{ marginTop: "10px" }}>
        <strong>Felder:</strong>
        {availableFields.map((f) => (
          <label key={f.name} style={{ marginLeft: "10px" }}>
            <input
              type="checkbox"
              checked={selectedFields.includes(f.name)}
              onChange={() => toggleField(f.name)}
              disabled={f.chart_type && f.chart_type !== selectedChartType && selectedChartType !== "line"}
            />{" "}
            {f.name} {f.unit ? `(${f.unit})` : ""}
          </label>
        ))}
      </div>

      <div style={{ marginTop: "10px" }}>
        <strong>Intensität:</strong>
        {intensities.map((i) => (
          <label key={i} style={{ marginLeft: "10px" }}>
            <input
              type="checkbox"
              checked={selectedIntensities.includes(i)}
              onChange={() => toggleIntensity(i)}
            />{" "}
            {i}
          </label>
        ))}
      </div>

      <div style={{ marginTop: "20px" }}>
        {chartData && <Plot data={chartData.data} layout={chartData.layout} />}
      </div>
    </div>
  );
}

export default ChallengePlot;