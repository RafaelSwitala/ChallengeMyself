import { useState } from "react";
import { Container, Form, Button } from "react-bootstrap";

function App() {
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");

  const createChallenge = async () => {
    const response = await fetch("http://localhost:5000/challenges", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name }),
    });

    if (response.ok) {
      setMessage("Challenge erstellt 🎉");
      setName("");
    } else {
      setMessage("Fehler beim Erstellen");
    }
  };

  return (
    <Container className="mt-5">
      <h1>ChallengeMyself</h1>

      <Form>
        <Form.Group className="mb-3">
          <Form.Label>Neue Challenge</Form.Label>
          <Form.Control
            type="text"
            placeholder="z.B. Lernen"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </Form.Group>

        <Button onClick={createChallenge}>Erstellen</Button>
      </Form>

      {message && <p className="mt-3">{message}</p>}
    </Container>
  );
}

export default App;
