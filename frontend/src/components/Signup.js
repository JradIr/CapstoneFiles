import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./Signup.css";

const Signup = () => {
  const [username, setUsername] = useState("");   // NEW username field
  const [email, setEmail] = useState("");   
  const [password, setPassword] = useState("");
  const [repeatPassword, setRepeatPassword] = useState(""); 
  const [popupMessage, setPopupMessage] = useState("");     
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password !== repeatPassword) {
      setPopupMessage("Passwords do not match!");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/api/signup/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }), // include username
      });

      const data = await res.json();

      if (res.ok) {
        setPopupMessage(data.message || "Account created successfully!");
        setTimeout(() => {
          navigate("/login"); 
        }, 2000);
      } else {
        setPopupMessage(JSON.stringify(data));
      }
    } catch (err) {
      console.error("Signup error:", err);
      setPopupMessage("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-box">
        <h2>User Signup</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Choose a Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Enter your Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Choose a Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Repeat Password"
            value={repeatPassword}
            onChange={(e) => setRepeatPassword(e.target.value)}
            required
          />
          <button type="submit">Sign Up</button>
          <p>
            Back to login? <Link to="/login">Login</Link>
          </p>
        </form>

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

export default Signup;
