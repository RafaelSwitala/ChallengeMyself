import { useState, useEffect } from "react";
import { Routes, Route, Link, useNavigate } from "react-router-dom";
import ChallengeDetail from "./ChallengeDetail";
import "./App.css";

function App() {
  const [activities, setActivities] = useState([]);
  const [selectedActivity, setSelectedActivity] = useState("");
  const [challengeName, setChallengeName] = useState("");
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");
  const [challenges, setChallenges] = useState([]);
  const navigate = useNavigate();
  const loadChallenges = async () => {
    try {
      const res = await fetch("http://localhost:5000/challenges");
      const data = await res.json();
      setChallenges(data);
    } catch (err) {
      console.error("Failed to load challenges", err);
      setMessage("Fehler beim Laden der Challenges");
      setMessageType("error");
    }
  };

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const res = await fetch("http://localhost:5000/activities");
        const data = await res.json();
        setActivities(data.activities || []);
        if (data.activities && data.activities.length > 0) {
          setSelectedActivity(data.activities[0]);
        }
      } catch (err) {
        console.error("Failed to load activities", err);
        setMessage("Fehler beim Laden der Activities");
        setMessageType("error");
      }
    };

    fetchActivities();
    loadChallenges();
  }, []);

  const createChallenge = async (e) => {
    e.preventDefault();
    
    if (!challengeName.trim()) {
      setMessage("Bitte einen Challenge-Namen eingeben");
      setMessageType("error");
      return;
    }

    if (!selectedActivity) {
      setMessage("Bitte eine Activity auswählen");
      setMessageType("error");
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
        setMessageType("error");
        return;
      }

      setMessage(`Challenge "${challengeName}" successfully created`);
      setMessageType("success");
      setChallengeName("");
      loadChallenges();
      
      setTimeout(() => setMessage(""), 3000);
    } catch (err) {
      console.error("Failed to create challenge", err);
      setMessage("Serverfehler beim Erstellen der Challenge");
      setMessageType("error");
    }
  };

  return (
    <div className="App">
      <Routes>
        <Route
          path="/"
          element={
            <>
              <header className="App-header">
                <div className="container">
                  <h1>ChallengeMyself</h1>
                  <p>Verfolge deine persönlichen Ziele und Herausforderungen</p>
                </div>
              </header>

              <div className="container">
                <div className="App-content">
                  <div className="form-card">
                    <h2>Neue Challenge erstellen</h2>
                    <form onSubmit={createChallenge}>
                      <div className="form-group">
                        <label htmlFor="challengeName" className="required">Challenge-Name</label>
                        <input
                          id="challengeName"
                          type="text"
                          placeholder="z.B. Sommerfit 2026, Marathon-Training"
                          value={challengeName}
                          onChange={(e) => setChallengeName(e.target.value)}
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="activity" className="required">Activity-Typ</label>
                        <select
                          id="activity"
                          value={selectedActivity}
                          onChange={(e) => setSelectedActivity(e.target.value)}
                          disabled={activities.length === 0}
                        >
                          <option value="">-- Bitte wählen --</option>
                          {activities.map((activity) => (
                            <option key={activity} value={activity}>
                              {activity}
                            </option>
                          ))}
                        </select>
                      </div>

                      <div className="form-actions">
                        <button className="btn btn-primary" type="submit">
                          Challenge erstellen
                        </button>
                      </div>
                    </form>

                    {message && (
                      <div className={`alert alert-${messageType === "success" ? "success" : "error"}`}>
                        {message}
                      </div>
                    )}
                  </div>

                  <div style={{ marginTop: "3rem" }}>
                    <h2>Deine Challenges</h2>
                    
                    {challenges.length === 0 ? (
                      <div className="card" style={{ textAlign: "center", padding: "3rem" }}>
                        <p style={{ color: "#6c757d", fontSize: "1.1rem" }}>
                          Noch keine Challenges erstellt. Starten Sie eine neue Challenge oben!
                        </p>
                      </div>
                    ) : (
                      <div className="challenges-grid">
                        {challenges.map((c) => (
                          <div
                            key={c.name}
                            className="challenge-card"
                            onClick={() => navigate(`/challenge/${encodeURIComponent(c.name)}`)}
                          >
                            <h3>{c.name}</h3>
                            <div className="challenge-card-meta">
                              <span>{c.activity_type}</span>
                            </div>
                            <p style={{ margin: 0, color: "#6c757d", fontSize: "0.95rem" }}>
                              Klicken Sie um zu starten →
                            </p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </>
          }
        />

        <Route path="/challenge/:name" element={<ChallengeDetail />} />
      </Routes>
    </div>
  );
}

export default App;