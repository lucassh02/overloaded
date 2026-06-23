import React, { useState, useEffect, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { fetchWorkouts, deleteWorkout } from "../api";
import { Workout } from "../types";

const WorkoutLog: React.FC = () => {
  const auth = useContext(AuthContext);
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (auth?.token) {
      loadWorkouts();
    }
  }, [auth?.token]);

  const loadWorkouts = async () => {
    try {
      const data = await fetchWorkouts(auth!.token!);
      setWorkouts(data);
    } catch (err) {
      setError("Failed to load workouts");
      console.error(err);
    }
  };

  const handleDelete = async (id: number) => {
    if (!auth?.token) return;
    try {
      await deleteWorkout(auth.token, id);
      await loadWorkouts();
    } catch (err) {
      setError("Failed to delete workout");
      console.error(err);
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: "700px" }}>
      <h2 className="mb-4">Workout History</h2>
      {error && <div className="alert alert-danger">{error}</div>}

      {workouts.length === 0 ? (
        <div className="text-center text-muted py-5">
          <p className="mb-1">No workouts logged yet.</p>
          <p className="small">Head to the dashboard to start one.</p>
        </div>
      ) : (
        <div className="d-flex flex-column gap-3">
          {workouts.map((workout) => (
            <div
              key={workout.id}
              className="card shadow-sm"
              style={{ border: "none", borderLeft: "5px solid #6366f1" }}
            >
              <div className="card-body">
                <div className="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <span className="badge bg-primary mb-1">
                      {workout.workout_type}
                    </span>
                    <div className="text-muted small">{workout.date}</div>
                  </div>
                  <button
                    className="btn btn-outline-danger btn-sm"
                    onClick={() => handleDelete(workout.id)}
                  >
                    Delete
                  </button>
                </div>

                {workout.exercises.length > 0 && (
                  <ul className="list-unstyled mb-0 mt-3">
                    {workout.exercises.map((ex, i) => (
                      <li
                        key={i}
                        className="d-flex justify-content-between py-2 border-top"
                      >
                        <span className="fw-medium">{ex.name}</span>
                        <span className="text-muted small">
                          {ex.sets} × {ex.reps} @ {ex.weight} lbs
                          {ex.rpe ? ` · RPE ${ex.rpe}` : ""}
                        </span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default WorkoutLog;
