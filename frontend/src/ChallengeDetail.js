import { useState, useEffect } from "react";
import SessionForm from "./SessionForm";

function ChallengeDetail({ challengeName }) {
  const [challenge, setChallenge] = useState(null);

  const loadChallenge = async () => {
    const res = await fetch(`http://localhost:5000/challenges/${challengeName}`);
    const data = await res.json();
    setChallenge(data);
  };

  useEffect(() => {
    loadChallenge();
  }, [challengeName]);

  const addSession = async (sessionData) => {
    const res = await fetch(`http://localhost:5000/challenges/${challengeName}/sessions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(sessionData),
    });
    if (res.ok) loadChallenge();
  };

  if (!challenge) return <p>Lade Challenge…</p>;

  return (
    <div>
      <h2>{challenge.name} ({challenge.activity_type})</h2>

      <h3>Neue Session</h3>
      <SessionForm
        fields={challenge.sessions.length > 0 
          ? Object.keys(challenge.sessions[0].values) 
          : []} // oder vom Backend per GET /activities/<activity_type>
        onSubmit={addSession}
      />

      <h3>Sessions</h3>
      <ul>
        {challenge.sessions.map((s, i) => (
          <li key={i}>
            {s.date} {s.time} – {JSON.stringify(s.values)}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ChallengeDetail;
