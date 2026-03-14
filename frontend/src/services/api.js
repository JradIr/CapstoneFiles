import { Navigate } from "react-router-dom";

const API_URL = "http://127.0.0.1:8000/api";

// --- API Functions ---
export const login = async (email, password) => {
  const res = await fetch(`${API_URL}/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }), // use email instead of username
  });
  return res.json();
};

export const getDashboard = async () => {
  const token = localStorage.getItem("access"); // use access token
  const res = await fetch(`${API_URL}/dashboard/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
};

// --- Route Protection ---
export const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem("access");
  return token ? children : <Navigate to="/login" />;
};

export const AdminPrivateRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem("adminAuth");
  return isAuthenticated ? children : <Navigate to="/admin" />;
};
