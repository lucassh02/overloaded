import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";
import { fetchWorkouts } from "../api";
import { Workout } from "../types";

const Dashboard: React.FC = () => {
  const auth = useContext(AuthContext);
  const navigate = useNavigate();
  const [workouts, setWorkouts] = useState<Workout[]>([]);

  useEffect(() => {
    const loadWorkouts = async () => {
      if (!auth?.token) return;
      try {
        const data = await fetchWorkouts(auth.token);
        setWorkouts(data);
      } catch (err) {
        console.error("Failed to load workouts", err);
      }
    };
    loadWorkouts();
  }, [auth?.token]);

  const handleStartWorkout = () => {
    if (!auth?.token) return;
    navigate("/log-workout");
  };

  // Stats derived from the workouts data we already have
  const totalWorkouts = workouts.length;
  const totalExercises = workouts.reduce(
    (sum, w) => sum + w.exercises.length,
    0,
  );
  const lastWorkoutDate = workouts.length > 0 ? workouts[0].date : "—";

  const recentWorkouts = workouts.slice(0, 3);

  return (
    <div className="container mt-5" style={{ maxWidth: "700px" }}>
      <h2 className="mb-1">Welcome back</h2>
      <p className="text-muted mb-4">{auth?.user?.email || "User"}</p>

      {/* Start Workout call-to-action */}
      <div
        className="card shadow-sm mb-4"
        style={{ border: "none", borderLeft: "5px solid #6366f1" }}
      >
        <div className="card-body d-flex justify-content-between align-items-center">
          <div>
            <h5 className="mb-1">Ready to train?</h5>
            <span className="text-muted small">
              Log your lifts quickly and get back to it.
            </span>
          </div>
          <button
            onClick={handleStartWorkout}
            className="btn btn-primary btn-lg"
          >
            Start Workout
          </button>
        </div>
      </div>

      {/* Quick stats */}
      <div className="row g-3 mb-4">
        <div className="col">
          <div className="card shadow-sm text-center border-0">
            <div className="card-body">
              <div className="h3 mb-0">{totalWorkouts}</div>
              <div className="text-muted small">Workouts</div>
            </div>
          </div>
        </div>
        <div className="col">
          <div className="card shadow-sm text-center border-0">
            <div className="card-body">
              <div className="h3 mb-0">{totalExercises}</div>
              <div className="text-muted small">Exercises Logged</div>
            </div>
          </div>
        </div>
        <div className="col">
          <div className="card shadow-sm text-center border-0">
            <div className="card-body">
              <div className="h6 mb-0 mt-2">{lastWorkoutDate}</div>
              <div className="text-muted small">Last Workout</div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent workouts preview */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h5 className="mb-0">Recent Activity</h5>
        <Link to="/workouts" className="small text-decoration-none">
          View all
        </Link>
      </div>

      {recentWorkouts.length === 0 ? (
        <div className="text-center text-muted py-4">
          No workouts yet — start your first one above.
        </div>
      ) : (
        <div className="d-flex flex-column gap-2">
          {recentWorkouts.map((workout) => (
            <div key={workout.id} className="card shadow-sm border-0">
              <div className="card-body py-2 d-flex justify-content-between align-items-center">
                <div>
                  <span className="badge bg-primary me-2">
                    {workout.workout_type}
                  </span>
                  <span className="text-muted small">{workout.date}</span>
                </div>
                <span className="text-muted small">
                  {workout.exercises.length} exercise
                  {workout.exercises.length !== 1 ? "s" : ""}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
