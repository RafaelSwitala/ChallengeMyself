import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Plot from "react-plotly.js";
import "./ChallengeStats.css";

/**
 * ChallengeStats Component
 * 
 * Full-screen stats and chart analysis page with advanced filtering options:
 * - Value range filtering (min/max per variable)
 * - Category filtering (filter by field values)
 * - X-axis entry filtering (show every nth entry)
 * - Date range filtering
 * - Grid line control (daily, weekly, monthly)
 * - Multiple chart types (line + bar, dual bar charts)
 * - Secondary Y-axis for different scales
 */
function ChallengeStats() {
  const { name } = useParams();
  const challengeName = decodeURIComponent(name);
  const navigate = useNavigate();

  const [challenge, setChallenge] = useState(null);
  const [fields, setFields] = useState([]);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");

  // Chart configuration
  const [selectedFields, setSelectedFields] = useState([]);
  const [fieldTypes, setFieldTypes] = useState({});
  const [chartData, setChartData] = useState(null);
  const [chartLayout, setChartLayout] = useState(null);

  // Date range filtering
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");

  // Y-axis value range filters
  const [valueRangeFilters, setValueRangeFilters] = useState({});

  // X-axis entry filtering
  const [showEveryNthEntry, setShowEveryNthEntry] = useState(1);

  // Grid lines control
  const [gridLineMode, setGridLineMode] = useState("none"); // none, daily, weekly, monthly

  // Secondary Y-axis selection
  const [secondaryYFields, setSecondaryYFields] = useState([]);

  // Category filters
  const [categoryFilters, setCategoryFilters] = useState({});
  const [availableCategories, setAvailableCategories] = useState({});

  // Load challenge data
  useEffect(() => {
    const loadChallengeData = async () => {
      try {
        const res = await fetch(
          `http://localhost:5000/challenges/${encodeURIComponent(challengeName)}`
        );
        if (!res.ok) throw new Error("Challenge not found");
        const data = await res.json();
        setChallenge(data);

        // Load fields
        const fieldsRes = await fetch(
          `http://localhost:5000/activities/${encodeURIComponent(data.activity_type)}`
        );
        if (fieldsRes.ok) {
          const fieldsData = await fieldsRes.json();
          const numericFields = fieldsData.fields.filter(f => f.type === "number" && !f.hidden);
          setFields(numericFields);

          // Extract available categories for filters
          const categories = {};
          fieldsData.fields
            .filter(f => f.type === "enum" && !f.hidden)
            .forEach(f => {
              categories[f.name] = f.values || [];
            });
          setAvailableCategories(categories);
        }
      } catch (err) {
        console.error(err);
        setMessage("Error loading challenge data");
        setMessageType("error");
      }
    };

    loadChallengeData();
  }, [challengeName]);

  // Load chart when configuration changes
  useEffect(() => {
    if (!challenge || selectedFields.length === 0) {
      setChartData(null);
      return;
    }

    const loadChart = async () => {
      try {
        const queryParams = new URLSearchParams();
        queryParams.append("fields", selectedFields.join(","));

        if (dateFrom) queryParams.append("date_from", dateFrom);
        if (dateTo) queryParams.append("date_to", dateTo);
        if (showEveryNthEntry > 1) queryParams.append("show_every_nth", showEveryNthEntry);
        if (gridLineMode !== "none") queryParams.append("grid_mode", gridLineMode);
        if (secondaryYFields.length > 0) queryParams.append("secondary_y_fields", secondaryYFields.join(","));

        // Add field types
        selectedFields.forEach(field => {
          if (fieldTypes[field]) {
            queryParams.append(`field_type_${field}`, fieldTypes[field]);
          }
        });

        // Add value range filters
        Object.entries(valueRangeFilters).forEach(([field, range]) => {
          if (range.min !== "" && range.min !== null) {
            queryParams.append(`${field}_min`, range.min);
          }
          if (range.max !== "" && range.max !== null) {
            queryParams.append(`${field}_max`, range.max);
          }
        });

        // Add category filters
        Object.entries(categoryFilters).forEach(([category, value]) => {
          if (value) {
            queryParams.append(`filter_${category}`, value);
          }
        });

        const res = await fetch(
          `http://localhost:5000/challenges/${encodeURIComponent(challengeName)}/plot?${queryParams}`,
          {
            headers: { "Accept": "application/json" },
          }
        );

        if (!res.ok) {
          const errorData = await res.json();
          setMessage(`Chart error: ${errorData.error || "Unknown error"}`);
          setMessageType("error");
          return;
        }

        const data = await res.json();
        setChartData(data.data || []);
        setChartLayout(data.layout || {});
        setMessage("");
      } catch (err) {
        console.error("Chart loading error:", err);
        setMessage("Error loading chart data");
        setMessageType("error");
      }
    };

    loadChart();
  }, [challengeName, selectedFields, fieldTypes, dateFrom, dateTo, showEveryNthEntry, gridLineMode, secondaryYFields, valueRangeFilters, categoryFilters]);

  const handleFieldToggle = (fieldName, isSelected) => {
    if (isSelected) {
      setSelectedFields([...selectedFields, fieldName]);
      setFieldTypes({ ...fieldTypes, [fieldName]: "line" });
    } else {
      setSelectedFields(selectedFields.filter(f => f !== fieldName));
      const newFieldTypes = { ...fieldTypes };
      delete newFieldTypes[fieldName];
      setFieldTypes(newFieldTypes);
      setSecondaryYFields(secondaryYFields.filter(f => f !== fieldName));
    }
  };

  const handleFieldTypeChange = (fieldName, newType) => {
    setFieldTypes({ ...fieldTypes, [fieldName]: newType });
  };

  const handleSecondaryYToggle = (fieldName) => {
    if (secondaryYFields.includes(fieldName)) {
      setSecondaryYFields(secondaryYFields.filter(f => f !== fieldName));
    } else {
      setSecondaryYFields([...secondaryYFields, fieldName]);
    }
  };

  const handleValueRangeChange = (field, rangeType, value) => {
    setValueRangeFilters({
      ...valueRangeFilters,
      [field]: {
        ...valueRangeFilters[field],
        [rangeType]: value === "" ? null : parseFloat(value),
      },
    });
  };

  const handleCategoryFilterChange = (category, value) => {
    if (!value) {
      const newFilters = { ...categoryFilters };
      delete newFilters[category];
      setCategoryFilters(newFilters);
    } else {
      setCategoryFilters({ ...categoryFilters, [category]: value });
    }
  };

  if (!challenge) {
    return (
      <div className="stats-container">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="stats-container">
      <header className="stats-header">
        <div className="container">
          <button className="btn-back" onClick={() => navigate(`/challenge/${encodeURIComponent(challengeName)}`)}>
            ← Back
          </button>
          <div>
            <h1>{challenge.name} – Analytics & Charts</h1>
            <p className="stats-subtitle">{challenge.activity_type}</p>
          </div>
        </div>
      </header>

      <div className="container">
        <div className="stats-content">
          {message && (
            <div className={`alert alert-${messageType}`}>
              {message}
            </div>
          )}

          {/* Filter Panel */}
          <div className="filter-panel">
            <h2>Filters & Chart Configuration</h2>

            {/* Field Selection */}
            <section className="filter-section">
              <h3>Variables to Display</h3>
              <div className="field-selection">
                {fields.length === 0 ? (
                  <p className="no-data">No numeric fields available</p>
                ) : (
                  fields.map(field => (
                    <div key={field.name} className="field-control">
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={selectedFields.includes(field.name)}
                          onChange={(e) => handleFieldToggle(field.name, e.target.checked)}
                        />
                        <span>{field.name} {field.unit ? `(${field.unit})` : ""}</span>
                      </label>

                      {selectedFields.includes(field.name) && (
                        <div className="field-options">
                          <select
                            value={fieldTypes[field.name] || "line"}
                            onChange={(e) => handleFieldTypeChange(field.name, e.target.value)}
                            className="chart-type-select"
                          >
                            <option value="line">Line</option>
                            <option value="bar">Bar</option>
                          </select>

                          <label className="checkbox-label">
                            <input
                              type="checkbox"
                              checked={secondaryYFields.includes(field.name)}
                              onChange={() => handleSecondaryYToggle(field.name)}
                            />
                            <span>Right Y-Axis</span>
                          </label>

                          {/* Value Range Filter */}
                          <div className="range-filter">
                            <label>Value Range</label>
                            <input
                              type="number"
                              placeholder="Min"
                              value={valueRangeFilters[field.name]?.min ?? ""}
                              onChange={(e) => handleValueRangeChange(field.name, "min", e.target.value)}
                              className="range-input"
                            />
                            <span>–</span>
                            <input
                              type="number"
                              placeholder="Max"
                              value={valueRangeFilters[field.name]?.max ?? ""}
                              onChange={(e) => handleValueRangeChange(field.name, "max", e.target.value)}
                              className="range-input"
                            />
                          </div>
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            </section>

            {/* Date Range Filter */}
            <section className="filter-section">
              <h3>Date Range</h3>
              <div className="date-filter">
                <input
                  type="date"
                  value={dateFrom}
                  onChange={(e) => setDateFrom(e.target.value)}
                  placeholder="From"
                  className="date-input"
                />
                <span>to</span>
                <input
                  type="date"
                  value={dateTo}
                  onChange={(e) => setDateTo(e.target.value)}
                  placeholder="To"
                  className="date-input"
                />
              </div>
            </section>

            {/* Category Filters */}
            {Object.keys(availableCategories).length > 0 && (
              <section className="filter-section">
                <h3>Filter by Categories</h3>
                <div className="category-filters">
                  {Object.entries(availableCategories).map(([category, options]) => (
                    <div key={category} className="category-filter">
                      <label>{category}</label>
                      <select
                        value={categoryFilters[category] || ""}
                        onChange={(e) => handleCategoryFilterChange(category, e.target.value)}
                        className="category-select"
                      >
                        <option value="">All</option>
                        {options.map(option => (
                          <option key={option} value={option}>
                            {option}
                          </option>
                        ))}
                      </select>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {/* X-Axis Entry Filtering */}
            <section className="filter-section">
              <h3>X-Axis Display</h3>
              <label className="label-with-input">
                Show every
                <input
                  type="number"
                  min="1"
                  value={showEveryNthEntry}
                  onChange={(e) => setShowEveryNthEntry(Math.max(1, parseInt(e.target.value) || 1))}
                  className="nth-input"
                />
                entry
              </label>
            </section>

            {/* Grid Lines Control */}
            <section className="filter-section">
              <h3>Grid Lines</h3>
              <div className="grid-options">
                <label className="radio-label">
                  <input
                    type="radio"
                    value="none"
                    checked={gridLineMode === "none"}
                    onChange={(e) => setGridLineMode(e.target.value)}
                  />
                  <span>None</span>
                </label>
                <label className="radio-label">
                  <input
                    type="radio"
                    value="daily"
                    checked={gridLineMode === "daily"}
                    onChange={(e) => setGridLineMode(e.target.value)}
                  />
                  <span>Daily</span>
                </label>
                <label className="radio-label">
                  <input
                    type="radio"
                    value="weekly"
                    checked={gridLineMode === "weekly"}
                    onChange={(e) => setGridLineMode(e.target.value)}
                  />
                  <span>Weekly (Mondays)</span>
                </label>
                <label className="radio-label">
                  <input
                    type="radio"
                    value="monthly"
                    checked={gridLineMode === "monthly"}
                    onChange={(e) => setGridLineMode(e.target.value)}
                  />
                  <span>Monthly</span>
                </label>
              </div>
            </section>
          </div>

          {/* Chart Display */}
          <div className="chart-section">
            {selectedFields.length === 0 ? (
              <div className="empty-state">
                <p>Select at least one variable to display a chart</p>
              </div>
            ) : chartData ? (
              <Plot
                data={chartData}
                layout={{
                  ...chartLayout,
                  autosize: true,
                  responsive: true,
                  margin: { l: 80, r: 80, t: 50, b: 80 },
                }}
                style={{ width: "100%", height: "600px" }}
                useResizeHandler={true}
              />
            ) : (
              <div className="spinner"></div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChallengeStats;
