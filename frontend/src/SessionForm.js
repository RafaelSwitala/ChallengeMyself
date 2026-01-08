import { useState } from "react";
import { Form, Button } from "react-bootstrap";

function SessionForm({ fields, onSubmit }) {
  // Initialwerte für alle Felder
  const initialValues = {};
  fields.forEach(f => (initialValues[f] = ""));
  
  const [values, setValues] = useState(initialValues);
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");

  const handleChange = (field, value) => {
    setValues(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ date, time, values });
    // Reset optional
    setValues(initialValues);
    setDate("");
    setTime("");
  };

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

      {fields.map(f => (
        <Form.Group className="mb-3" key={f}>
          <Form.Label>{f}</Form.Label>
          <Form.Control
            type="text"
            value={values[f]}
            onChange={(e) => handleChange(f, e.target.value)}
          />
        </Form.Group>
      ))}

      <Button type="submit">Session speichern</Button>
    </Form>
  );
}

export default SessionForm;
