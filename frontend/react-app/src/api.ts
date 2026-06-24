import {
  User,
  LoginResponse,
  Workout,
  ExerciseEntry,
  ExerciseOption,
} from "./types";

const API_URL = import.meta.env.VITE_API_URL;

/**
 * Core request helper. Wraps fetch with JSON headers, optional JWT auth,
 * and consistent error handling — every API call below goes through this.
 * The generic <T> lets each caller declare the shape of the response.
 */
const request = async <T>(
  endpoint: string,
  method: string = "GET",
  body: any = null,
  token: string | null = null,
): Promise<T> => {
  const headers: HeadersInit = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const options: RequestInit = { method, headers };
  if (body) options.body = JSON.stringify(body);

  const response = await fetch(`${API_URL}${endpoint}`, options);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(
      errorData?.error || `HTTP error! Status: ${response.status}`,
    );
  }

  return response.json();
};

// Create a new user account
export const registerUser = async (userData: {
  username: string;
  email: string;
  password: string;
}) => {
  try {
    return await request<{ message: string }>("/register", "POST", userData);
  } catch (err: any) {
    if (err.message) {
      throw new Error(err.message); // surface the backend's error message
    }
    throw new Error("An unexpected error occurred.");
  }
};

// Authenticate and receive a JWT access token
export const loginUser = (userData: { email: string; password: string }) => {
  return request<LoginResponse>("/login", "POST", userData);
};

// Fetch a user's profile (requires token)
export const getUserProfile = (userId: number, token: string) => {
  return request<User>(`/user/${userId}`, "GET", null, token);
};

// Fetch all workout sessions for the logged-in user, each with its exercises
export const fetchWorkouts = (token: string) => {
  return request<Workout[]>("/workouts", "GET", null, token);
};

// Fetch the exercise list (global exercises + any the user created)
export const fetchExercises = (token: string) => {
  return request<ExerciseOption[]>("/exercises", "GET", null, token);
};

// Log a complete workout: creates the session and all exercise logs in one transaction
export const logWorkout = (
  token: string,
  workoutType: string,
  exercises: ExerciseEntry[],
) => {
  return request<{ message: string; session_id: number }>(
    "/log-workout",
    "POST",
    { workout_type: workoutType, exercises },
    token,
  );
};

// Delete a workout session by ID
export const deleteWorkout = (token: string, workoutId: number) => {
  return request<{ message: string }>(
    `/workouts/${workoutId}`,
    "DELETE",
    null,
    token,
  );
};
