import React, { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

const Dashboard: React.FC = () => {
  const auth = useContext(AuthContext);

  return (
    <div>
      <h2>Welcome, {auth?.user?.email || "User"}</h2>
      <button onClick={auth?.logout}>Logout</button>
    </div>
  );
};

export default Dashboard;
