import React, { useState } from "react";

const TestComponent: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState<string | null>(null);

  const handleLogin = async () => {
    const response = await fetch("http://127.0.0.1:5000/test-login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    if (data.access_token) {
      setToken(data.access_token);
    } else {
      alert("Invalid credentials");
    }
  };

  return (
    <div>
      <h2>Test Login</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
      {token && <p>JWT Token: {token}</p>}
    </div>
  );
};

export default TestComponent;
