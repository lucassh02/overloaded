import React, { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Login: React.FC = () => {
  console.log("Login component rendered");
  const auth = useContext(AuthContext);
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevent default form submission behavior

    // Sanitize inputs
    const sanitizedEmail = email.trim().toLowerCase();

    // Validate inputs
    if (!sanitizedEmail || !password) {
      setError("Please enter both email and password.");
      return;
    }

    if (!emailRegex.test(sanitizedEmail)) {
      setError("The email address format is invalid. Please try again.");
      return;
    }

    try {
      setLoading(true);
      setError(null); // Clear any previous errors

      if (auth) {
        console.log("Navigating to dashboard...");
        await auth.login(sanitizedEmail, password);
        navigate("/dashboard");
        console.log("Navigation complete.");
      }
    } catch (err: any) {
      console.error("Login error:", err);
      console.log("Error object:", err);

      // Handle backend error response
      if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error);
      } else if (err.message) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-4">
          <h2 className="text-center mb-4">Login</h2>
          <form
            onSubmit={handleSubmit}
            noValidate
            className="border p-4 rounded shadow"
          >
            {/* Render error alert */}
            {error && <div className="alert alert-danger">{error}</div>}
            <div className="mb-3">
              <input
                type="email"
                className="form-control"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="mb-3">
              <input
                type="password"
                className="form-control"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button
              type="submit"
              className="btn btn-primary w-100"
              disabled={loading}
            >
              {loading ? (
                <span className="spinner-border spinner-border-sm"></span>
              ) : (
                "Login"
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
