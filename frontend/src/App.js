import { useState, useEffect } from "react";
import { Container, Form, Button } from "react-bootstrap";
import { Routes, Route, Link } from "react-router-dom";
import ChallengeDetail from "./ChallengeDetail";

function App() {
  const [activities, setActivities] = useState([]);
  const [selectedActivity, setSelectedActivity] = useState("");
  const [challengeName, setChallengeName] = useState("");
  const [message, setMessage] = useState("");
  const [challenges, setChallenges] = useState([]);

  // Challenges laden
  const loadChallenges = async () => {
    try {
      const res = await fetch("http://localhost:5000/challenges");
      const data = await res.json();
      setChallenges(data);
    } catch (err) {
      console.error("Failed to load challenges", err);
      setMessage("Fehler beim Laden der Challenges");
    }
  };

  // Activities aus dem Backend laden
  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const res = await fetch("http://localhost:5000/activities");
        const data = await res.json();
        setActivities(data.activities || []);
        if (data.activities && data.activities.length > 0) {
          setSelectedActivity(data.activities[0].name);
        }
      } catch (err) {
        console.error("Failed to load activities", err);
        setMessage("Fehler beim Laden der Activities");
      }
    };

    fetchActivities();
    loadChallenges();
  }, []);

  const createChallenge = async () => {
    if (!challengeName.trim()) {
      setMessage("Bitte einen Challenge-Namen eingeben");
      return;
    }

    if (!selectedActivity) {
      setMessage("Bitte eine Activity auswählen");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/challenges", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: challengeName.trim(),
          activity: selectedActivity,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(`Fehler: ${data.error}`);
        return;
      }

      setMessage(`Challenge "${challengeName}" erstellt`);
      setChallengeName("");
      loadChallenges();
    } catch (err) {
      console.error("Failed to create challenge", err);
      setMessage("Serverfehler");
    }
  };

  return (
    <Container className="mt-5">
      <Routes>
        <Route
          path="/"
          element={
            <>
              <h1>ChallengeMyself</h1>

              <Form className="mt-4">
                <Form.Group className="mb-3">
                  <Form.Label>Challenge-Name</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="z. B. Übung-Marathon"
                    value={challengeName}
                    onChange={(e) => setChallengeName(e.target.value)}
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Activity</Form.Label>
                    <Form.Select
                      value={selectedActivity}
                      onChange={(e) => setSelectedActivity(e.target.value)}
                      disabled={activities.length === 0}
                    >
                      {activities.map((a) => (
                        <option key={a} value={a}>
                          {a}
                        </option>
                      ))}
                    </Form.Select>

                </Form.Group>

                <Button type="button" onClick={createChallenge}>
                  Neue Challenge erstellen
                </Button>
              </Form>

              {message && <p className="mt-3">{message}</p>}

              <hr />

              <h3>Deine Challenges</h3>
              {challenges.length === 0 && (
                <p>Noch keine Challenges vorhanden.</p>
              )}

              <ul>
                {challenges.map((c) => (
                  <li key={c.name}>
                    <Link to={`/challenge/${encodeURIComponent(c.name)}`}>
                      <strong>{c.name}</strong> ({c.activity_type})
                    </Link>
                  </li>
                ))}
              </ul>
            </>
          }
        />

        <Route path="/challenge/:name" element={<ChallengeDetail />} />
      </Routes>
    </Container>
  );
}

export default App;