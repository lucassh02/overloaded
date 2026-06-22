import React, { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { fetchExercises, logWorkout } from "../api";
import { ExerciseOption, ExerciseEntry } from "../types";

const LogWorkout: React.FC = () => {
  const auth = useContext(AuthContext);
  const [exercises, setExercises] = useState<ExerciseEntry[]>([
    { exercise_id: 0, sets: 3, reps: 10, weight: 0, rpe: 7 },
  ]);
  const [exerciseOptions, setExerciseOptions] = useState<ExerciseOption[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const loadExercises = async () => {
      if (!auth?.token) return;
      try {
        const res = await fetchExercises(auth.token);
        setExerciseOptions(res);
      } catch (err) {
        console.error("Failed to fetch exercises", err);
      }
    };
    loadExercises();
  }, [auth]);

  const handleExerciseChange = (
    index: number,
    field: keyof ExerciseEntry,
    value: string | number,
  ) => {
    const updated = [...exercises];
    updated[index][field] = Number(value);
    setExercises(updated);
  };

  const addExercise = () => {
    setExercises([
      ...exercises,
      { exercise_id: 0, sets: 3, reps: 10, weight: 0, rpe: 7 },
    ]);
  };

  const removeExercise = (index: number) => {
    setExercises(exercises.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!auth?.token) return;

    // Validate that at least one real exercise is selected
    const validExercises = exercises.filter((ex) => ex.exercise_id !== 0);
    if (validExercises.length === 0) {
      setError("Please select at least one exercise before saving.");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await logWorkout(auth.token, "Lifting", validExercises);
      alert("Workout saved successfully!");
      navigate("/dashboard");
    } catch (err) {
      console.error("Failed to log workout:", err);
      setError("Failed to log workout. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4 border p-4 rounded shadow">
      <h3>Log Workout</h3>
      {error && <p style={{ color: "red" }}>{error}</p>}

      {exercises.map((exercise, index) => (
        <div key={index} className="border p-3 mb-3 rounded">
          <div className="mb-2">
            <select
              className="form-control"
              value={exercise.exercise_id}
              onChange={(e) =>
                handleExerciseChange(index, "exercise_id", e.target.value)
              }
              required
            >
              <option value={0}>-- Select Exercise --</option>
              {exerciseOptions.map((opt) => (
                <option key={opt.id} value={opt.id}>
                  {opt.name}
                </option>
              ))}
            </select>
          </div>
          <div className="d-flex gap-2 align-items-end">
            <div className="flex-fill">
              <label className="form-label small mb-1">Sets</label>
              <input
                type="number"
                className="form-control"
                placeholder="Sets"
                value={exercise.sets}
                onChange={(e) =>
                  handleExerciseChange(index, "sets", e.target.value)
                }
              />
            </div>
            <div className="flex-fill">
              <label className="form-label small mb-1">Reps</label>
              <input
                type="number"
                className="form-control"
                placeholder="Reps"
                value={exercise.reps}
                onChange={(e) =>
                  handleExerciseChange(index, "reps", e.target.value)
                }
              />
            </div>
            <div className="flex-fill">
              <label className="form-label small mb-1">Weight (lbs)</label>
              <input
                type="number"
                className="form-control"
                placeholder="Weight"
                value={exercise.weight}
                onChange={(e) =>
                  handleExerciseChange(index, "weight", e.target.value)
                }
              />
            </div>
            <div className="flex-fill">
              <label className="form-label small mb-1">RPE</label>
              <input
                type="number"
                className="form-control"
                placeholder="RPE"
                value={exercise.rpe}
                onChange={(e) =>
                  handleExerciseChange(index, "rpe", e.target.value)
                }
              />
            </div>
            <button
              type="button"
              className="btn btn-danger"
              onClick={() => removeExercise(index)}
            >
              ✖
            </button>
          </div>
        </div>
      ))}

      <button
        type="button"
        className="btn btn-secondary mb-3"
        onClick={addExercise}
      >
        + Add Exercise
      </button>

      <button
        type="submit"
        className="btn btn-success w-100"
        disabled={loading}
      >
        {loading ? "Saving..." : "Save Workout"}
      </button>
    </form>
  );
};

export default LogWorkout;
