import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import AdminLogin from "./components/AdminLogin";
import AdminDashboard from "./components/AdminDashboard";
import Signup from "./components/Signup";
import { PrivateRoute } from "./services/api";
import { AdminPrivateRoute } from "./services/api"; // new helper for admin protection

const API_URL = "http://127.0.0.1:8000/api";

export const getDashboard = async () => {
  const token = localStorage.getItem("token");
  const res = await fetch(`${API_URL}/dashboard/`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    }
  });
  return res.json();
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Admin routes */}
        <Route path="/admin" element={<AdminLogin />} />
        <Route
          path="/admin/dashboard"
          element={
            <AdminPrivateRoute>
              <AdminDashboard />
            </AdminPrivateRoute>
          }
        />

        {/* User routes */}
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard getDashboard={getDashboard} />
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
