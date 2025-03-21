import React, { useState, useEffect, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { fetchWorkouts, addWorkout, deleteWorkout } from "../api";
import { Workout } from "../types";

const WorkoutLog: React.FC = () => {
  const auth = useContext(AuthContext);
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [date, setDate] = useState("");
  const [duration, setDuration] = useState("");
  const [workoutType, setWorkoutType] = useState("");
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!auth?.token) return;

    try {
      await addWorkout(auth.token, date, Number(duration), workoutType);
      setDate("");
      setDuration("");
      setWorkoutType("");
      await loadWorkouts();
    } catch (err) {
      setError("Failed to log workout");
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
    <div>
      <h2>Workout Log</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Duration (minutes)"
          value={duration}
          onChange={(e) => setDuration(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Workout type (e.g. Running)"
          value={workoutType}
          onChange={(e) => setWorkoutType(e.target.value)}
          required
        />
        <button type="submit">Log Workout</button>
      </form>

      <h3>Workout History</h3>
      <ul>
        {workouts.map((workout) => (
          <li key={workout.id}>
            {workout.date} - {workout.workout_type} ({workout.duration} min)
            <button onClick={() => handleDelete(workout.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default WorkoutLog;
