import React, { createContext, useEffect, ReactNode, useContext } from "react";
import { loginUser, getUserProfile } from "../api";
import { User, AuthContextType } from "../types";
import useLocalStorage from "../hooks/useLocalStorage";

export const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useLocalStorage<User | null>("user", null);
  const [token, setToken] = useLocalStorage<string | null>("token", null);

  useEffect(() => {
    if (token) {
      const userId = localStorage.getItem("userId");
      if (userId) {
        console.log("Token before fetching profile:", token);
        console.log("User ID before fetching profile:", userId);
        getUserProfile(Number(userId), token)
          .then((res) => setUser(res))
          .catch(() => logout());
      }
    }
  }, [token]);

  const login = async (email: string, password: string) => {
    try {
      const res = await loginUser({ email, password });

      console.log("Login response:", res); // Debugging line
      if (!res.access_token) throw new Error("No token received");

      setToken(res.access_token);
      setUser({ id: res.user_id, username: "", email });
    } catch (error) {
      console.error("Login failed", error);
      throw error; // Ensure the error propagates to Login.tsx
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
