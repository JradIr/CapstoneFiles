import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./Login.css";
import { login } from "../services/api";   // API helper

const Login = () => {
  const [email, setEmail] = useState("");   
  const [password, setPassword] = useState("");
  const [popupMessage, setPopupMessage] = useState(""); // popup state
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const data = await login(email, password);

      if (data.tokens && data.tokens.access && data.tokens.refresh) {
        // store JWT tokens in localStorage
        localStorage.setItem("access", data.tokens.access);
        localStorage.setItem("refresh", data.tokens.refresh);

        navigate("/dashboard"); // redirect to dashboard
      } else {
        setPopupMessage(data.error || "Invalid credentials");
      }
    } catch (err) {
      console.error("Login error:", err);
      setPopupMessage("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>User Login</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Login</button>
        </form>
        <p>
          Don’t have an account? <Link to="/signup">Sign up</Link>
        </p>

        {/* Popup modal */}
        {popupMessage && (
          <div className="popup">
            <div className="popup-content">
              <p>{popupMessage}</p>
              <button onClick={() => setPopupMessage("")}>Close</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Login;
