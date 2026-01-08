import { useState } from "react";
import { Container, Form, Button } from "react-bootstrap";

const activities = [
"Laufen",
"Radfahren",
"Lesen",
"Lernen",
"Liegestütze",
"Rauchen",
"Schlaf",
"Wasser",
"Spazieren",
"Workout",
"Schwimmen",
"Bildschirmzeit",
"Alkohol",
"Stimmung",
"Stress",
"Energielevel",
"Motivation"

];

function App() {
  const [selectedActivity, setSelectedActivity] = useState(activities[0]);
  const [message, setMessage] = useState("");

  const createChallenge = async () => {
    const response = await fetch("http://localhost:5000/challenges", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: selectedActivity }),
    });

    if (response.ok) {
      setMessage(`Challenge "${selectedActivity}" erstellt 🎉`);
    } else {
      const data = await response.json();
      setMessage(`Fehler: ${data.error}`);
    }
  };

  return (
    <Container className="mt-5">
      <h1>ChallengeMyself</h1>

      <Form>
        <Form.Group className="mb-3">
          <Form.Label>Neue Challenge</Form.Label>
          <Form.Select
            value={selectedActivity}
            onChange={(e) => setSelectedActivity(e.target.value)}
          >
            {activities.map((a) => (
              <option key={a} value={a}>{a}</option>
            ))}
          </Form.Select>
        </Form.Group>

        <Button onClick={createChallenge}>Erstellen</Button>
      </Form>

      {message && <p className="mt-3">{message}</p>}
    </Container>
  );
}

export default App;
