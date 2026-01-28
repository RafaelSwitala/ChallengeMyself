import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { Container, Button, Form, Table } from "react-bootstrap";
import SessionForm from "./SessionForm";
import ChallengePlot from "./ChallengePlot";

function ChallengeDetail() {
  const { name } = useParams();
  const challengeName = decodeURIComponent(name);

  const [challenge, setChallenge] = useState(null);
  const [fields, setFields] = useState([]);
  const [goalDescription, setGoalDescription] = useState("");
  const [goalTarget, setGoalTarget] = useState("");
  const [goalPeriod, setGoalPeriod] = useState("");
  const [message, setMessage] = useState("");

  // Challenge laden
  const loadChallenge = async () => {
    try {
      const res = await fetch(
        `http://localhost:5000/challenges/${encodeURIComponent(challengeName)}`
      );
      if (!res.ok) throw new Error("Challenge nicht gefunden");
      const data = await res.json();
      setChallenge(data);

      // Goal-Felder initialisieren
      if (data.goal) {
        setGoalDescription(data.goal.description || "");
        setGoalTarget(data.goal.target || "");
        setGoalPeriod(data.goal.period || "");
      } else {
        setGoalDescription("");
        setGoalTarget("");
        setGoalPeriod("");
      }
    } catch (err) {
      console.error(err);
      setMessage("Fehler beim Laden der Challenge");
    }
  };

  // Meta-Felder laden
  const loadFields = async (activity) => {
    try {
      const res = await fetch(
        `http://localhost:5000/activities/${encodeURIComponent(activity)}`
      );
      if (!res.ok) throw new Error("Fehler beim Laden der Felder");
      const data = await res.json();
      const loadedFields = Array.isArray(data.fields) ? data.fields : [];
      setFields(loadedFields);
    } catch (err) {
      console.error(err);
      setFields([]);
    }
  };

  useEffect(() => {
    loadChallenge();
  }, [challengeName]);

  useEffect(() => {
    if (challenge?.activity_type) loadFields(challenge.activity_type);
  }, [challenge]);

  // Neue Session hinzufügen
  const addSession = async (sessionData) => {
    try {
      const res = await fetch(
        `http://localhost:5000/challenges/${encodeURIComponent(
          challengeName
        )}/sessions`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(sessionData),
        }
      );
      if (res.ok) loadChallenge();
    } catch (err) {
      console.error(err);
      setMessage("Fehler beim Hinzufügen der Session");
    }
  };

  // Goal speichern
  const saveGoal = async () => {
    try {
      const res = await fetch(
        `http://localhost:5000/challenges/${encodeURIComponent(
          challengeName
        )}/goal`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            description: goalDescription,
            target: goalTarget,
            period: goalPeriod,
          }),
        }
      );
      if (res.ok) loadChallenge();
    } catch (err) {
      console.error(err);
      setMessage("Fehler beim Speichern des Ziels");
    }
  };

  // Goal löschen
  const deleteGoal = async () => {
    try {
      const res = await fetch(
        `http://localhost:5000/challenges/${encodeURIComponent(
          challengeName
        )}/goal`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(null),
        }
      );
      if (res.ok) {
        setGoalDescription("");
        setGoalTarget("");
        setGoalPeriod("");
        loadChallenge();
      }
    } catch (err) {
      console.error(err);
      setMessage("Fehler beim Löschen des Ziels");
    }
  };

  if (!challenge) return <p>Lade Challenge…</p>;

  return (
    <Container className="mt-4">
      <Link to="/">Zurück</Link>
      <h2 className="mt-3">
        {challenge.name} ({challenge.activity_type})
      </h2>

      <h4 className="mt-4">Ziel</h4>
      {challenge.goal ? (
        <div className="mb-3">
          <p>
            <strong>{challenge.goal.description}</strong>
            <br />
            Ziel: {challenge.goal.target} – Zeitraum: {challenge.goal.period}
          </p>
          <Button variant="secondary" size="sm" onClick={deleteGoal}>
            Ziel bearbeiten / löschen
          </Button>
        </div>
      ) : (
        <Form className="mb-4">
          <Form.Group className="mb-2">
            <Form.Label>Beschreibung</Form.Label>
            <Form.Control
              value={goalDescription}
              onChange={(e) => setGoalDescription(e.target.value)}
            />
          </Form.Group>
          <Form.Group className="mb-2">
            <Form.Label>Zielwert</Form.Label>
            <Form.Control
              type="number"
              value={goalTarget}
              onChange={(e) => setGoalTarget(e.target.value)}
            />
          </Form.Group>
          <Form.Group className="mb-2">
            <Form.Label>Zeitraum</Form.Label>
            <Form.Control
              placeholder="z. B. pro Woche"
              value={goalPeriod}
              onChange={(e) => setGoalPeriod(e.target.value)}
            />
          </Form.Group>
          <Button onClick={saveGoal}>Ziel speichern</Button>
        </Form>
      )}

      <h4>Neue Session</h4>
      <SessionForm fields={fields} onSubmit={addSession} />

      <h4 className="mt-4">Bisherige Sessions</h4>
      {challenge.sessions.length === 0 ? (
        <p>Noch keine Sessions.</p>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Datum</th>
              <th>Zeit</th>
              {fields.map((f) => (
                <th key={f.name}>
                  {f.name} {f.unit ? `(${f.unit})` : ""}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {challenge.sessions.map((s, idx) => (
              <tr key={idx}>
                <td>{s.date}</td>
                <td>{s.time}</td>
                {fields.map((f) => (
                  <td key={f.name}>{String(s.values?.[f.name] ?? "")}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      <h4 className="mt-4">Visualisierung</h4>
      <ChallengePlot challengeName={challengeName} availableFields={fields} />

      {message && <p className="mt-3 text-danger">{message}</p>}
    </Container>
  );
}

export default ChallengeDetail;
