export interface User {
    id: number;
    username: string;
    email: string;
  }
  
  export interface LoginResponse {
    access_token: string;
    user_id: number;
  }
  
  export interface AuthContextType {
    user: User | null;
    token: string | null;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
  }