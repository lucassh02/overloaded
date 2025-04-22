import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const auth = useAuth();

  if (!auth?.token) {
    console.log("User not authenticated. Redirecting to login...");
    return <Navigate to="/login" />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
