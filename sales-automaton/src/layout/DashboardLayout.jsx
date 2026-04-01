import { Outlet, Link } from "react-router-dom";
import { useContext, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import "../styles/dashboard.css";

export default function DashboardLayout() {

  const { logout, user } = useContext(AuthContext);
  const [open, setOpen] = useState(false);

  const closeMenu = () => setOpen(false);

  return (
    <div className="dashboard">

      {/* Overlay for mobile */}
      {open && <div className="overlay" onClick={closeMenu}></div>}

      {/* Sidebar */}
      <aside className={`sidebar ${open ? "open" : ""}`}>

        <button className="sidebar-close" onClick={closeMenu}>
          ✕
        </button>

        <h3>{user?.tenant_name}</h3>

        <nav>

          <Link to="/" onClick={closeMenu}>Overview</Link>
          <Link to="/whatsapp" onClick={closeMenu}>Link your WhatsApp</Link>
          <Link to="/leads" onClick={closeMenu}>Leads</Link>
          <Link to="/billing" onClick={closeMenu}>Billing</Link>
          <Link to="/leads/new" onClick={closeMenu}>Add Lead</Link>
          <Link to="/escalations" onClick={closeMenu}>Escalated</Link>
          <Link to="/leads/import" onClick={closeMenu}>Import Leads</Link>
          <Link to="/logs" onClick={closeMenu}>Logs</Link>
          <Link to="/analytics" onClick={closeMenu}>Analytics</Link>
          <Link to="/settings" onClick={closeMenu}>Settings</Link>
          <button className="logout" onClick={logout}>
          Logout
        </button>
        </nav>

      </aside>


      {/* Main content */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>

        <div className="topbar">
          <button className="menu-btn" onClick={() => setOpen(true)}>
            ☰
          </button>

          <div>{user?.tenant_name}</div>
        </div>

        <main className="dashboard-content">
          <Outlet />
        </main>

      </div>

    </div>
  );
}