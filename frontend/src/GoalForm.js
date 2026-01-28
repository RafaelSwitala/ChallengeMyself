import { useState, useEffect } from "react";
import { Form, Button } from "react-bootstrap";

function GoalForm({ challengeName, goal, onSaved }) {
  const [description, setDescription] = useState("");
  const [target, setTarget] = useState("");
  const [period, setPeriod] = useState("");

  useEffect(() => {
    if (goal) {
      setDescription(goal.description);
      setTarget(goal.target);
      setPeriod(goal.period);
    }
  }, [goal]);

  const saveGoal = async () => {
    const res = await fetch(
      `http://localhost:5000/challenges/${challengeName}/goal`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          description,
          target,
          period,
        }),
      }
    );

    if (res.ok && onSaved) onSaved();
  };

  const clearForm = () => {
    setDescription("");
    setTarget("");
    setPeriod("");
  };

  return (
    <Form className="mb-4">
      <Form.Group className="mb-2">
        <Form.Label>Beschreibung</Form.Label>
        <Form.Control
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </Form.Group>

      <Form.Group className="mb-2">
        <Form.Label>Zielwert</Form.Label>
        <Form.Control
          type="number"
          value={target}
          onChange={(e) => setTarget(e.target.value)}
        />
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Zeitraum</Form.Label>
        <Form.Control
          placeholder="z. B. pro Woche"
          value={period}
          onChange={(e) => setPeriod(e.target.value)}
        />
      </Form.Group>

      <Button onClick={saveGoal} className="me-2">
        Ziel speichern
      </Button>

      <Button variant="secondary" onClick={clearForm}>
        Löschen
      </Button>
    </Form>
  );
}

export default GoalForm;
