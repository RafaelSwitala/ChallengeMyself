import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import SessionForm from "./SessionForm";
import ChallengePlot from "./ChallengePlot";
import "./ChallengeDetail.css";

function ChallengeDetail() {
  const { name } = useParams();
  const challengeName = decodeURIComponent(name);
  const navigate = useNavigate();

  const [challenge, setChallenge] = useState(null);
  const [fields, setFields] = useState([]);
  const [goalDescription, setGoalDescription] = useState("");
  const [goalTarget, setGoalTarget] = useState("");
  const [goalPeriod, setGoalPeriod] = useState("");
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");
  const [editingGoal, setEditingGoal] = useState(false);

  const loadChallenge = async () => {
    try {
      const res = await fetch(
        `http://localhost:5000/challenges/${encodeURIComponent(challengeName)}`
      );
      if (!res.ok) throw new Error("Challenge nicht gefunden");
      const data = await res.json();
      setChallenge(data);

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
      setMessageType("error");
    }
  };

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

  const addSession = async (sessionData) => {
    try {
      const res = await fetch(
        `http://localhost:5000/challenges/${encodeURIComponent(challengeName)}/sessions`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(sessionData),
        }
      );
      if (res.ok) {
        setMessage("Session successfully added");
        setMessageType("success");
        setTimeout(() => setMessage(""), 3000);
        loadChallenge();
      } else {
        const errorData = await res.json().catch(() => ({}));
        setMessage(`Fehler: ${errorData.error || 'Session konnte nicht gespeichert werden'}`);
        setMessageType("error");
      }
    } catch (err) {
      console.error(err);
      setMessage("Fehler beim Hinzufügen der Session");
      setMessageType("error");
    }
  };

  const saveGoal = async () => {
    try {
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
      if (res.ok) {
        setMessage("Goal saved");
        setMessageType("success");
        setEditingGoal(false);
        setTimeout(() => setMessage(""), 3000);
        loadChallenge();
      } else {
        const errorData = await res.json().catch(() => ({}));
        setMessage(`Fehler: ${errorData.error || 'Ziel konnte nicht gespeichert werden'}`);
        setMessageType("error");
      }
    } catch (err) {
      console.error(err);
      setMessage("Fehler beim Speichern des Ziels");
      setMessageType("error");
    }
  };

  const deleteGoal = async () => {
    if (!window.confirm("Ziel wirklich löschen?")) return;
    try {
      const res = await fetch(
        `http://localhost:5000/challenges/${encodeURIComponent(challengeName)}/goal?delete=1`,
        { method: "POST", headers: { "Content-Type": "application/json" } }
      );
      if (res.ok) {
        setGoalDescription("");
        setGoalTarget("");
        setGoalPeriod("");
        setEditingGoal(false);
        setMessage("Goal deleted");
        setMessageType("success");
        setTimeout(() => setMessage(""), 3000);
        loadChallenge();
      } else {
        const errorData = await res.json().catch(() => ({}));
        setMessage(`Fehler: ${errorData.error || 'Ziel konnte nicht gelöscht werden'}`);
        setMessageType("error");
      }
    } catch (err) {
      console.error(err);
      setMessage("Fehler beim Löschen des Ziels");
      setMessageType("error");
    }
  };

  if (!challenge) {
    return (
      <div className="challenge-detail-container">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="challenge-detail-container">
      <header className="challenge-header">
        <div className="container">
          <button className="btn-back" onClick={() => navigate("/")}>&larr; Zurück</button>
          <div>
            <h1>{challenge.name}</h1>
            <p className="challenge-activity"> {challenge.activity_type}</p>
          </div>
        </div>
      </header>

      <div className="container">
        <div className="challenge-content">
          {message && (
            <div className={`alert alert-${messageType}`}>
              {message}
            </div>
          )}

          <section className="challenge-section">
            <h2>Ziel</h2>
            {challenge.goal && !editingGoal ? (
              <div className="goal-display">
                <div className="goal-content">
                  <h3>{challenge.goal.description}</h3>
                  <p>
                    <strong>Zielwert:</strong> {challenge.goal.target}
                  </p>
                  <p>
                    <strong>Zeitraum:</strong> {challenge.goal.period}
                  </p>
                </div>
                <div className="goal-actions">
                  <button className="btn btn-secondary" onClick={() => setEditingGoal(true)}>
                    Bearbeiten
                  </button>
                  <button className="btn btn-danger" onClick={deleteGoal}>
                    Löschen
                  </button>
                </div>
              </div>
            ) : (
              <form className="goal-form" onSubmit={(e) => {
                e.preventDefault();
                saveGoal();
              }}>
                <div className="form-group">
                  <label htmlFor="goalDesc">Beschreibung</label>
                  <input
                    id="goalDesc"
                    value={goalDescription}
                    onChange={(e) => setGoalDescription(e.target.value)}
                    placeholder="z.B. 10 km laufen"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="goalTarget">Zielwert</label>
                  <input
                    id="goalTarget"
                    type="number"
                    step="0.1"
                    value={goalTarget}
                    onChange={(e) => setGoalTarget(e.target.value)}
                    placeholder="z.B. 100"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="goalPeriod">Zeitraum</label>
                  <input
                    id="goalPeriod"
                    value={goalPeriod}
                    onChange={(e) => setGoalPeriod(e.target.value)}
                    placeholder="z.B. pro Woche"
                  />
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn btn-primary">Speichern</button>
                  {challenge.goal && (
                    <button
                      type="button"
                      className="btn btn-outline"
                      onClick={() => setEditingGoal(false)}
                    >
                      Abbrechen
                    </button>
                  )}
                </div>
              </form>
            )}
          </section>

          <section className="challenge-section">
            <h2>Neue Session</h2>
            <SessionForm fields={fields} onSubmit={addSession} />
          </section>

          <section className="challenge-section">
            <h2>Sessions</h2>
            {challenge.sessions.length === 0 ? (
              <div className="empty-state">
                <p>Noch keine Sessions eingetragen.</p>
              </div>
            ) : (
              <div className="sessions-table-wrapper">
                <table className="sessions-table">
                  <thead>
                    <tr>
                      <th>Datum</th>
                      <th>Zeit</th>
                      {fields
                        .filter((f) => !f.hidden)
                        .map((f) => (
                          <th key={f.name}>
                            {f.name}{f.unit ? ` (${f.unit})` : ""}
                          </th>
                        ))}
                    </tr>
                  </thead>
                  <tbody>
                    {challenge.sessions.map((s, idx) => (
                      <tr key={idx}>
                        <td>{s.date}</td>
                        <td>{s.time}</td>
                        {fields
                          .filter((f) => !f.hidden)
                          .map((f) => (
                            <td key={f.name}>{String(s.values?.[f.name] ?? "—")}</td>
                          ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>

          {/* Chart Section */}
          <section className="challenge-section">
            <h2>Diagramme & Analysen</h2>
            <ChallengePlot challengeName={challengeName} availableFields={fields} />
          </section>
        </div>
      </div>
    </div>
  );
}

export default ChallengeDetail;
