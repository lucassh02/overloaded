import React, { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Dashboard: React.FC = () => {
  const auth = useContext(AuthContext);
  const navigate = useNavigate();

  if (!auth?.user) {
    navigate("/login");
    return null;
  }

  return (
    <div>
      <h2>Welcome, {auth.user.email}</h2>
      <button onClick={auth.logout}>Logout</button>
    </div>
  );
};

export default Dashboard;
