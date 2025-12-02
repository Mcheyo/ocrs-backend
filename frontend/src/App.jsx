import { useEffect, useState } from "react";
import "./App.css";

const BACKEND_BASE_URL = "http://127.0.0.1:5000";

function App() {
  const [backendStatus, setBackendStatus] = useState("Checking backend...");
  const [courses, setCourses] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        setError("");

        // 1️⃣ Health check – matches /health in Swagger
        const healthRes = await fetch(`${BACKEND_BASE_URL}/health`);
        if (!healthRes.ok) {
          throw new Error(`Health check failed: ${healthRes.status}`);
        }
        const healthJson = await healthRes.json();
        setBackendStatus(healthJson.status || "Backend OK");

        // 2️⃣ Load courses – matches the JSON you showed me
        const coursesRes = await fetch(`${BACKEND_BASE_URL}/api/courses/`);
        if (!coursesRes.ok) {
          throw new Error(`Courses request failed: ${coursesRes.status}`);
        }

        const coursesJson = await coursesRes.json();

        // Your API wraps the list like: { data: { courses: [...] }, ... }
        const list = coursesJson?.data?.courses ?? [];

        setCourses(list);
      } catch (err) {
        console.error("Frontend API error:", err);
        setError(err.message || "Unknown error talking to backend");
      }
    }

    loadData();
  }, []);

  return (
    <div className="container">
      <h1>Online Course Registration System</h1>
      <h3>Frontend ↔ Backend Integration Test</h3>

      <div className="card">
        <h3>Backend status</h3>
        <p>{backendStatus}</p>
      </div>

      <div className="card">
        <h3>Courses (from Flask API)</h3>

        {error && (
          <p style={{ color: "#ff4d4f", marginTop: "0.5rem" }}>
            Error: {error}
          </p>
        )}

        {!error && courses.length === 0 && (
          <p style={{ opacity: 0.7, marginTop: "0.5rem" }}>
            No courses found (database is empty).
          </p>
        )}

        {!error && courses.length > 0 && (
          <ul style={{ marginTop: "0.75rem", textAlign: "left" }}>
            {courses.map((c) => (
              <li key={c.course_id}>
                {c.course_id} — {c.course_name}
              </li>
            ))}
          </ul>
        )}
      </div>

      <p style={{ marginTop: "2rem", opacity: 0.4 }}>
        Once this works, we can replace this test screen with the real UI
        (login, enrollment, etc.) using these same API calls.
      </p>
    </div>
  );
}

export default App;

