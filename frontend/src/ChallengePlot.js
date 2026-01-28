import { useState, useEffect } from "react";
import Plot from "react-plotly.js";

function ChallengePlot({ challengeName, availableFields }) {
  const [selectedFields, setSelectedFields] = useState([]);
  const [selectedIntensities, setSelectedIntensities] = useState([]);
  const [chartData, setChartData] = useState(null);

  const intensities = ["gemuetlich", "stark"];

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

    const res = await fetch(`http://localhost:5000/challenges/${encodeURIComponent(challengeName)}/plot?${params.toString()}`);
    const data = await res.json();
    setChartData(data);
  };

  useEffect(() => {
    loadData();
  }, [selectedFields, selectedIntensities]);

  const toggleField = (field) => {
    setSelectedFields(prev =>
      prev.includes(field) ? prev.filter(f => f !== field) : [...prev, field]
    );
  };

  const toggleIntensity = (intensity) => {
    setSelectedIntensities(prev =>
      prev.includes(intensity) ? prev.filter(i => i !== intensity) : [...prev, intensity]
    );
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <h4>Filter</h4>
      <div>
        <strong>Felder:</strong>
        {availableFields.map(f => (
          <label key={f} style={{ marginLeft: "10px" }}>
            <input
              type="checkbox"
              checked={selectedFields.includes(f)}
              onChange={() => toggleField(f)}
            /> {f}
          </label>
        ))}
      </div>

      <div style={{ marginTop: "10px" }}>
        <strong>Intensität:</strong>
        {intensities.map(i => (
          <label key={i} style={{ marginLeft: "10px" }}>
            <input
              type="checkbox"
              checked={selectedIntensities.includes(i)}
              onChange={() => toggleIntensity(i)}
            /> {i}
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
