import React, { useContext, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { startWorkoutSession } from "../api";

const Dashboard: React.FC = () => {
  const auth = useContext(AuthContext);
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleStartWorkout = async () => {
    if (!auth?.token) return;

    try {
      setLoading(true);
      const res = await startWorkoutSession(auth.token, "Lifting");
      const sessionId = res.session_id;
      console.log("Started workout session with ID:", sessionId);

      // Navigate to your workout logging screen
      navigate(`/log-workout/${sessionId}`);
    } catch (err) {
      console.error("Failed to start workout session:", err);
      setError("Failed to start workout session. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Welcome, {auth?.user?.email || "User"}</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button
        onClick={handleStartWorkout}
        className="btn btn-primary mt-3"
        disabled={loading}
      >
        {loading ? "Starting..." : "Start Workout"}
      </button>
    </div>
  );
};

export default Dashboard;
