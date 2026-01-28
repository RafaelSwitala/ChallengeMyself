import { useState, useEffect } from "react";
import { Form, Button } from "react-bootstrap";

function SessionForm({ fields, onSubmit }) {
  const [values, setValues] = useState({});
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");

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
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!date || !time) return;

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
  };

  if (fields.length === 0) {
    return <p>Keine Felder für diese Activity gefunden.</p>;
  }

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3">
        <Form.Label>Datum</Form.Label>
        <Form.Control
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
        />
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Uhrzeit</Form.Label>
        <Form.Control
          type="time"
          value={time}
          onChange={(e) => setTime(e.target.value)}
          required
        />
      </Form.Group>

      {fields.map((f) => (
        <Form.Group className="mb-3" key={f.name}>
          <Form.Label>
            {f.name} {f.unit ? `(${f.unit})` : ""}
          </Form.Label>

          {f.type === "enum" ? (
            <Form.Select
              value={values[f.name] || ""}
              onChange={(e) => handleChange(f.name, e.target.value)}
              required
            >
              <option value="">Bitte wählen</option>
              {f.values?.map((v) => (
                <option key={v} value={v}>
                  {v}
                </option>
              ))}
            </Form.Select>
          ) : (
            <Form.Control
              type={f.type === "number" ? "number" : "text"}
              value={values[f.name] || ""}
              onChange={(e) => handleChange(f.name, e.target.value)}
              required
            />
          )}
        </Form.Group>
      ))}

      <Button type="submit">Session speichern</Button>
    </Form>
  );
}

export default SessionForm;
