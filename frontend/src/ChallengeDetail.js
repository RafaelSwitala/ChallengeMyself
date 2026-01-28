import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { Container, Button, Form } from "react-bootstrap";
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
const loadChallenge = async () => {
  try {
    const res = await fetch(
      `http://localhost:5000/challenges/${encodeURIComponent(challengeName)}`
    );

    if (!res.ok) throw new Error("Challenge nicht gefunden");

    const data = await res.json();
    setChallenge(data);

    if (data.goal) {
      setGoalDescription(data.goal.description);
      setGoalTarget(data.goal.target);
      setGoalPeriod(data.goal.period);
    }
  } catch (err) {
    console.error(err);
  }
};

  const loadFields = async (activity) => {
    const res = await fetch(`http://localhost:5000/activities/${encodeURIComponent(activity)}`);
    const data = await res.json();
    setFields(data.fields);
  };

  useEffect(() => {
    loadChallenge();
  }, [challengeName]);

  useEffect(() => {
    if (challenge?.activity_type) {
      loadFields(challenge.activity_type);
    }
  }, [challenge]);


  const addSession = async (sessionData) => {
    const res = await fetch(
      `http://localhost:5000/challenges/${encodeURIComponent(challengeName)}/sessions`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(sessionData),
      }
    );
    if (res.ok) loadChallenge();
  };


  const saveGoal = async () => {
    const res = await fetch(
      `http://localhost:5000/challenges/${encodeURIComponent(challengeName)}/goal`,
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
  };

const deleteGoal = async () => {
  const res = await fetch(
    `http://localhost:5000/challenges/${encodeURIComponent(challengeName)}/goal`,
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
            <strong>{challenge.goal.description}</strong><br />
            Ziel: {challenge.goal.target} - Zeitraum: {challenge.goal.period}
          </p>
          <Button variant="secondary" size="sm" onClick={deleteGoal}>
            Ziel bearbeiten
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

      <h4 className="mt-4">Sessions</h4>
      {challenge.sessions.length === 0 && <p>Noch keine Sessions.</p>}

      <ul>
        {challenge.sessions.map((s, i) => (
          <li key={i}>
            {s.date} {s.time} – {JSON.stringify(s.values)}
          </li>
        ))}
      </ul>

      <h2>{name}</h2>
    <ChallengePlot challengeName={challengeName} availableFields={fields} />
    </Container>
  );
}

export default ChallengeDetail;
