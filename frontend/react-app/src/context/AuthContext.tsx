import React, { createContext, useState, useEffect, ReactNode } from "react";
import { loginUser, getUserProfile } from "../api";
import { User, AuthContextType } from "../types";

export const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token")
  );

  useEffect(() => {
    if (token) {
      const userId = localStorage.getItem("userId");
      if (userId) {
        getUserProfile(Number(userId), token)
          .then((res) => setUser(res))
          .catch(() => logout());
      }
    }
  }, [token]);

  const login = async (email: string, password: string) => {
    try {
      const res = await loginUser({ email, password });
      setToken(res.access_token);
      setUser({ id: res.user_id, username: "", email });
      localStorage.setItem("token", res.access_token);
      localStorage.setItem("userId", res.user_id.toString());
    } catch (error) {
      console.error("Login failed", error);
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
    localStorage.removeItem("userId");
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
