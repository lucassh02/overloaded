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

  export interface Workout {
    id: number;
    date: string;
    duration: number;
    workout_type: string;
  }
  