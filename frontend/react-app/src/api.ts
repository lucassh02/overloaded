import { User, LoginResponse , Workout } from "./types";

const API_URL = import.meta.env.VITE_API_URL;  // Ensure the API_URL is defined

const request = async <T>(
  endpoint: string,
  method: string = "GET",
  body: any = null,
  token: string | null = null
): Promise<T> => {
  const headers: HeadersInit = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const options: RequestInit = { method, headers };
  if (body) options.body = JSON.stringify(body);

  const response = await fetch(`${API_URL}${endpoint}`, options);
  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }
  return response.json();
};

// Register user
export const registerUser = (userData: { username: string; email: string; password: string }) => {
  return request<{ message: string }>("/register", "POST", userData);
};

// Login user
export const loginUser = (userData: { email: string; password: string }) => {
  return request<LoginResponse>("/login", "POST", userData);
};

// Get user profile (requires token)
export const getUserProfile = (userId: number, token: string) => {
  return request<User>(`/user/${userId}`, "GET", null, token);
};


// Fetch all workouts for logged-in user
export const fetchWorkouts = (token: string) => {
  return request<Workout[]>("/workouts", "GET", null, token);
};

// Add a new workout
export const addWorkout = (
  token: string,
  date: string,
  duration: number,
  workoutType: string
) => {
  return request<{ message: string; id: number }>(
    "/workouts",
    "POST",
    { date, duration, workout_type: workoutType },
    token
  );
};

// Delete a workout
export const deleteWorkout = (token: string, workoutId: number) => {
  return request<{ message: string }>(
    `/workouts/${workoutId}`,
    "DELETE",
    null,
    token
  );
};