// components/NavBar.tsx
import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const NavBar: React.FC = () => {
  const auth = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    auth?.logout();
    navigate("/login");
  };

  return (
    <nav className="bg-light py-3 border-bottom">
      <div className="container d-flex justify-content-center align-items-center gap-3">
        {auth?.user ? (
          <>
            <Link className="text-decoration-none" to="/dashboard">
              Dashboard
            </Link>
            <span>|</span>
            <Link className="text-decoration-none" to="/workouts">
              Workouts
            </Link>
            <span>|</span>
            <button
              onClick={handleLogout}
              className="btn btn-outline-danger btn-sm"
              style={{ marginLeft: "0.5rem" }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link className="text-decoration-none" to="/login">
              Login
            </Link>
            <span>|</span>
            <Link className="text-decoration-none" to="/register">
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default NavBar;
