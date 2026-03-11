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
  const [goalReference, setGoalReference] = useState("");
  const [goalTarget, setGoalTarget] = useState("");
  const [goalPeriod, setGoalPeriod] = useState("");
  const [goalProgress, setGoalProgress] = useState(null);
  const [goalDef, setGoalDef] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);
  const [availablePeriods, setAvailablePeriods] = useState([]);
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
        setGoalReference(data.goal.reference || "");
        setGoalTarget(data.goal.target || "");
        setGoalPeriod(data.goal.period || "");
      } else {
        setGoalDescription("");
        setGoalReference("");
        setGoalTarget("");
        setGoalPeriod("");
      }
      
      loadGoalProgress(data.name);
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

  const loadGoalDefinition = async (activity) => {
    try {
      const res = await fetch(
        `http://localhost:5000/activities/${encodeURIComponent(activity)}/goals`
      );
      if (res.ok) {
        const data = await res.json();
        setGoalDef(data);
      }
    } catch (err) {
      console.error("Error loading goal definition:", err);
    }
  };

  const loadGoalProgress = async (challengeName, dateParam = null) => {
    try {
      let url = `http://localhost:5000/challenges/${encodeURIComponent(challengeName)}/goal/progress`;
      if (dateParam) {
        url += `?selected_date=${dateParam}`;
      }
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setGoalProgress(data.progress);
        
        if (data.progress && (data.progress.period_label.includes("Monat") || data.progress.period_label.includes("Tag"))) {
          generateAvailablePeriods(data.goal.period);
        }
      }
    } catch (err) {
      console.error("Error loading goal progress:", err);
    }
  };

  const generateAvailablePeriods = (period) => {
    const periods = [];
    const today = new Date();
    
    if (period === "monthly") {
      for (let i = 0; i < 12; i++) {
        const date = new Date(today.getFullYear(), today.getMonth() - i, 1);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const label = date.toLocaleDateString("de-DE", { month: "long", year: "numeric" });
        periods.push({
          value: `${year}-${month}`,
          label: label.charAt(0).toUpperCase() + label.slice(1)
        });
      }
    } else if (period === "daily") {
      for (let i = 0; i < 30; i++) {
        const date = new Date(today.getTime() - i * 24 * 60 * 60 * 1000);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");
        const dateStr = `${year}-${month}-${day}`;
        const label = date.toLocaleDateString("de-DE");
        periods.push({
          value: dateStr,
          label: label
        });
      }
    }
    
    setAvailablePeriods(periods);
  };

  useEffect(() => {
    loadChallenge();
  }, [challengeName]);

  useEffect(() => {
    if (challenge?.activity_type) {
      loadFields(challenge.activity_type);
      loadGoalDefinition(challenge.activity_type);
    }
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
            reference: goalReference,
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
        setSelectedDate(null);
        loadGoalProgress(challengeName);
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
        setGoalReference("");
        setGoalTarget("");
        setGoalPeriod("");
        setGoalProgress(null);
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
                  {challenge.goal.reference && (
                    <p>
                      <strong>Messkriterium:</strong> {challenge.goal.reference}
                    </p>
                  )}
                  <p>
                    <strong>Zielwert:</strong> {challenge.goal.target}
                    {goalDef?.reference_units?.[challenge.goal.reference] && ` ${goalDef.reference_units[challenge.goal.reference]}`}
                  </p>
                  <p>
                    <strong>Zeitraum:</strong> {challenge.goal.period}
                  </p>
                  {goalProgress && (
                    <div className="goal-progress">
                      <h4>Fortschritt</h4>
                      
                      {availablePeriods.length > 0 && (
                        <div className="period-selector">
                          <label htmlFor="periodSelect">Zeitraum:</label>
                          <select 
                            id="periodSelect"
                            value={selectedDate || (goalProgress.selected_period || "")}
                            onChange={(e) => {
                              setSelectedDate(e.target.value);
                              loadGoalProgress(challengeName, e.target.value);
                            }}
                          >
                            {availablePeriods.map((period) => (
                              <option key={period.value} value={period.value}>
                                {period.label}
                              </option>
                            ))}
                          </select>
                        </div>
                      )}
                      
                      <div className="progress-bar" style={{
                        background: `linear-gradient(to right, #4CAF50 0%, #4CAF50 ${Math.min((goalProgress.current / goalProgress.target) * 100, 100)}%, #e0e0e0 ${Math.min((goalProgress.current / goalProgress.target) * 100, 100)}%, #e0e0e0 100%)`
                      }} />
                      <p className="progress-message">
                        {goalProgress.message}
                      </p>
                      <p className="progress-status" style={{
                        color: goalProgress.status === 'completed' ? '#4CAF50' : goalProgress.status === 'in_progress' ? '#2196F3' : '#FF9800'
                      }}>
                        <strong>Status:</strong> {goalProgress.status}
                      </p>
                      
                      {challenge.goal.period === "daily" && goalProgress.consecutive_days > 0 && (
                        <p className="consecutive-days">
                          <strong>Tage in Folge:</strong> {goalProgress.consecutive_days} 
                        </p>
                      )}
                    </div>
                  )}
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
                    placeholder="z.B. neue Fremdsprache"
                  />
                </div>
                {goalDef?.allowed_references && goalDef.allowed_references.length > 0 && (
                  <div className="form-group">
                    <label htmlFor="goalRef">Messkriterium</label>
                    <select
                      id="goalRef"
                      value={goalReference}
                      onChange={(e) => setGoalReference(e.target.value)}
                    >
                      <option value="">-- Bitte wählen --</option>
                      {goalDef.allowed_references.map((ref) => (
                        <option key={ref} value={ref}>
                          {ref}
                          {goalDef.reference_units?.[ref] ? ` (${goalDef.reference_units[ref]})` : ""}
                        </option>
                      ))}
                    </select>
                  </div>
                )}
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
                {goalDef?.allowed_periods && goalDef.allowed_periods.length > 0 && (
                  <div className="form-group">
                    <label htmlFor="goalPeriod">Zeitraum</label>
                    <select
                      id="goalPeriod"
                      value={goalPeriod}
                      onChange={(e) => setGoalPeriod(e.target.value)}
                    >
                      <option value="">-- Bitte wählen --</option>
                      {goalDef.allowed_periods.map((p) => (
                        <option key={p} value={p}>
                          {p}
                        </option>
                      ))}
                    </select>
                  </div>
                )}
                {!goalDef?.allowed_periods && (
                  <div className="form-group">
                    <label htmlFor="goalPeriod">Zeitraum</label>
                    <input
                      id="goalPeriod"
                      value={goalPeriod}
                      onChange={(e) => setGoalPeriod(e.target.value)}
                      placeholder="z.B. pro Woche"
                    />
                  </div>
                )}
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

          <section className="challenge-section">
            <h2>Diagramme & Analysen</h2>
            <div style={{ textAlign: "center", padding: "2rem" }}>
              <p style={{ color: "#6c757d", marginBottom: "1.5rem" }}>
                Umfassende Diagrammanalyse mit erweiterten Filtern verfügbar
              </p>
              <button
                className="btn btn-primary"
                onClick={() => navigate(`/challenge/${encodeURIComponent(challengeName)}/stats`)}
              >
                Zur Analyse & Diagrammen →
              </button>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

export default ChallengeDetail;
