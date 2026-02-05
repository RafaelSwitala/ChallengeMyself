import { useState, useEffect } from "react";
import "./SessionForm.css";

function SessionForm({ fields, onSubmit }) {
  const [values, setValues] = useState({});
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [errors, setErrors] = useState({});

  // Initialisiere values bei Änderung von fields
  useEffect(() => {
    const initial = {};
    fields.forEach((f) => {
      initial[f.name] = "";
    });
    setValues(initial);
  }, [fields]);

  const handleChange = (fieldName, value) => {
    setValues((prev) => ({ ...prev, [fieldName]: value }));
    // Clear error for this field
    if (errors[fieldName]) {
      setErrors((prev) => ({ ...prev, [fieldName]: false }));
    }
  };

  const validate = () => {
    const newErrors = {};
    
    if (!date) newErrors.date = true;
    if (!time) newErrors.time = true;

    // Check required fields
    fields.forEach((f) => {
      if (f.required && !f.hidden && !values[f.name]) {
        newErrors[f.name] = true;
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }

    onSubmit({
      date,
      time,
      values,
    });

    // Formular zurücksetzen
    setDate("");
    setTime("");
    const cleared = {};
    fields.forEach((f) => {
      cleared[f.name] = "";
    });
    setValues(cleared);
    setErrors({});
  };

  if (fields.length === 0) {
    return <p>Keine Felder für diese Activity gefunden.</p>;
  }

  const userFields = fields.filter(f => !f.hidden); // Hide calculated fields from form

  return (
    <form className="session-form" onSubmit={handleSubmit}>
      <div className="form-row-2">
        <div className="form-group">
          <label htmlFor="date" className="required">Datum</label>
          <input
            id="date"
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className={errors.date ? "error" : ""}
          />
          {errors.date && <span className="error-text">Bitte Datum eingeben</span>}
        </div>

        <div className="form-group">
          <label htmlFor="time" className="required">Uhrzeit</label>
          <input
            id="time"
            type="time"
            value={time}
            onChange={(e) => setTime(e.target.value)}
            className={errors.time ? "error" : ""}
          />
          {errors.time && <span className="error-text">Bitte Uhrzeit eingeben</span>}
        </div>
      </div>

      <div className="fields-grid">
        {userFields.map((f) => (
          <div
            className="form-group"
            key={f.name}
            style={{ gridColumn: f.required ? "span 1" : "span 1" }}
          >
            <label htmlFor={f.name} className={f.required ? "required" : ""}>
              {f.name} {f.unit ? `(${f.unit})` : ""}
            </label>

            {f.type === "enum" ? (
              <>
                <select
                  id={f.name}
                  value={values[f.name] || ""}
                  onChange={(e) => handleChange(f.name, e.target.value)}
                  className={errors[f.name] ? "error" : ""}
                >
                  <option value="">-- Bitte wählen --</option>
                  {f.values?.map((v) => (
                    <option key={v} value={v}>
                      {v}
                    </option>
                  ))}
                </select>
                {errors[f.name] && <span className="error-text">Erforderlich</span>}
              </>
            ) : (
              <>
                <input
                  id={f.name}
                  type={f.type === "number" ? "number" : "text"}
                  step={f.type === "number" ? "0.01" : undefined}
                  value={values[f.name] || ""}
                  onChange={(e) => handleChange(f.name, e.target.value)}
                  className={errors[f.name] ? "error" : ""}
                  placeholder={f.required ? "Erforderlich" : "Optional"}
                />
                {errors[f.name] && <span className="error-text">Erforderlich</span>}
              </>
            )}
          </div>
        ))}
      </div>

      <div className="form-actions">
        <button type="submit" className="btn btn-primary">
          💾 Session speichern
        </button>
      </div>
    </form>
  );
}

export default SessionForm;
