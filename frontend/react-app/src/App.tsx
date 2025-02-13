import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Login from "./components/Login";
import Register from "./components/Register";
import Dashboard from "./components/Dashboard";
import TestComponent from "./components/TestComponent";

const App: React.FC = () => {
  return (
    <AuthProvider>
      <nav>
        <Link to="/">Home</Link> | 
        <Link to="/register">Register</Link> | 
        <Link to="/login">Login</Link> | 
        <Link to="/dashboard">Dashboard</Link> | 
        <Link to="/test">Test</Link>
      </nav>
      <Routes>
        <Route path="/" element={<h2>Home Page</h2>} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/test" element={<TestComponent />} />
      </Routes>
    </AuthProvider>
  );
};

export default App;