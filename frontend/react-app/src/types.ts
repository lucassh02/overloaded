// Shapes returned by and sent to the backend API.
// Kept in sync with the Flask routes in app.py.

export interface User {
  id: string;
  username: string;
  email: string;
}

export interface LoginResponse {
  access_token: string;
  user_id: string;
}

export interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

// A logged exercise as returned from the server (rpe may be null in the DB).
export interface LoggedExercise {
  name: string;
  sets: number;
  reps: number;
  weight: number;
  rpe: number | null;
}

// A full workout session with its exercises, as returned by GET /workouts.
export interface Workout {
  id: number;
  date: string;
  workout_type: string;
  exercises: LoggedExercise[];
}

// A single exercise entry as sent to the server when logging a workout.
export interface ExerciseEntry {
  exercise_id: number;
  sets: number;
  reps: number;
  weight: number;
  rpe: number;
}

// An exercise option for the dropdown (id + name only).
export interface ExerciseOption {
  id: number;
  name: string;
}
