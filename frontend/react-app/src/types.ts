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

export interface LoggedExercise {
  name: string;
  sets: number;
  reps: number;
  weight: number;
  rpe: number | null;
}

export interface Workout {
  id: number;
  date: string;
  workout_type: string;
  exercises: LoggedExercise[];
}

export interface ExerciseEntry {
  exercise_id: number;
  sets: number;
  reps: number;
  weight: number;
  rpe: number;
}

export interface ExerciseOption {
  id: number;
  name: string;
}
