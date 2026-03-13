import React from "react";
import { useNavigate } from "react-router-dom";
import "./AdminDashboard.css";

const AdminDashboard = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("adminAuth"); // clear session
    navigate("/admin"); // back to login
  };

  return (
    <div className="admin-dashboard-container">
      <div className="admin-dashboard-box">
        <h1>Admin Dashboard</h1>
        <p>Welcome, Delarosa! You now have secure access to the admin panel.</p>

        <div className="admin-actions">
          <button>Manage Users</button>
          <button>View Reports</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
