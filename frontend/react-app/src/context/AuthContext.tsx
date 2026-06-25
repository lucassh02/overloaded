import React, { createContext, useEffect, ReactNode, useContext } from "react";
import { loginUser, getUserProfile } from "../api";
import { User, AuthContextType } from "../types";
import useLocalStorage from "../hooks/useLocalStorage";

export const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Provides authentication state (current user + JWT token) to the whole app.
 * Token and user are persisted to localStorage so the session survives a refresh.
 * On load, the stored token is used to re-fetch the user's profile from the
 * server — this keeps the profile fresh and verifies the token is still valid.
 */
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useLocalStorage<User | null>("user", null);
  const [token, setToken] = useLocalStorage<string | null>("token", null);

  useEffect(() => {
    if (!token) return;

    // The user object (with its id) was persisted at login; read the id from it.
    const stored = localStorage.getItem("user");
    const storedUser = stored ? JSON.parse(stored) : null;
    if (!storedUser?.id) return;

    getUserProfile(Number(storedUser.id), token)
      .then((freshUser) => setUser(freshUser))
      .catch(() => logout()); // token rejected/expired → clear the session
  }, [token]);

  const login = async (email: string, password: string) => {
    const res = await loginUser({ email, password });
    if (!res.access_token) throw new Error("No token received");

    setToken(res.access_token);
    setUser({ id: res.user_id, username: "", email });
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
