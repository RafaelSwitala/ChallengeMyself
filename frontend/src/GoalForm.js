import { useState, useEffect } from "react";
import { Form, Button } from "react-bootstrap";

function GoalForm({ challengeName, activityType, goal, onSaved }) {
  const [description, setDescription] = useState("");
  const [reference, setReference] = useState("");
  const [target, setTarget] = useState("");
  const [period, setPeriod] = useState("");
  const [goalDef, setGoalDef] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (goal) {
      setDescription(goal.description);
      setReference(goal.reference || "");
      setTarget(goal.target);
      setPeriod(goal.period);
    } else {
      setDescription("");
      setReference("");
      setTarget("");
      setPeriod("");
    }
  }, [goal]);

  useEffect(() => {
    loadGoalDefinition();
  }, [activityType]);

  const loadGoalDefinition = async () => {
    if (!activityType) return;
    try {
      setLoading(true);
      const res = await fetch(
        `http://localhost:5000/activities/${encodeURIComponent(activityType)}/goals`
      );
      if (res.ok) {
        const data = await res.json();
        setGoalDef(data);
        if (!reference && data.allowed_references?.length > 0) {
          setReference(data.allowed_references[0]);
        }
      }
    } catch (err) {
      console.error("Error loading goal definition:", err);
    } finally {
      setLoading(false);
    }
  };

  const saveGoal = async () => {
    const res = await fetch(
      `http://localhost:5000/challenges/${challengeName}/goal`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          description,
          reference,
          target,
          period,
        }),
      }
    );

    if (res.ok && onSaved) onSaved();
  };

  const clearForm = () => {
    setDescription("");
    setReference("");
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
          placeholder="z.B. neue Fremdsprache lernen"
        />
      </Form.Group>

      {goalDef?.allowed_references && goalDef.allowed_references.length > 0 && (
        <Form.Group className="mb-2">
          <Form.Label>Messkriterium</Form.Label>
          <Form.Select
            value={reference}
            onChange={(e) => setReference(e.target.value)}
          >
            <option value="">-- Bitte wählen --</option>
            {goalDef.allowed_references.map((ref) => (
              <option key={ref} value={ref}>
                {ref}
                {goalDef.reference_units?.[ref] ? ` (${goalDef.reference_units[ref]})` : ""}
              </option>
            ))}
          </Form.Select>
        </Form.Group>
      )}

      <Form.Group className="mb-2">
        <Form.Label>Zielwert</Form.Label>
        <Form.Control
          type="number"
          step="0.1"
          value={target}
          onChange={(e) => setTarget(e.target.value)}
          placeholder="z.B. 100"
        />
      </Form.Group>

      {goalDef?.allowed_periods && goalDef.allowed_periods.length > 0 && (
        <Form.Group className="mb-3">
          <Form.Label>Zeitraum</Form.Label>
          <Form.Select
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
          >
            <option value="">-- Bitte wählen --</option>
            {goalDef.allowed_periods.map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </Form.Select>
        </Form.Group>
      )}

      <Button onClick={saveGoal} className="me-2" disabled={loading}>
        Ziel speichern
      </Button>

      <Button variant="secondary" onClick={clearForm} disabled={loading}>
        Löschen
      </Button>
    </Form>
  );
}

export default GoalForm;
