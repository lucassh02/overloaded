import React, { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Dashboard: React.FC = () => {
  const auth = useContext(AuthContext);
  const navigate = useNavigate();

  const handleStartWorkout = () => {
    if (!auth?.token) return;
    navigate("/log-workout");
  };

  return (
    <div>
      <h2>Welcome, {auth?.user?.email || "User"}</h2>
      <button onClick={handleStartWorkout} className="btn btn-primary mt-3">
        Start Workout
      </button>
    </div>
  );
};

export default Dashboard;
