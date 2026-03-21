import { NavLink, Outlet } from "react-router-dom";
import { useState } from "react";
import "../../styles/analyticsLayout.css";

export default function AnalyticsLayout() {

  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="analytics-layout">

      <button
        className="analytics-menu-button"
        onClick={() => setMenuOpen(true)}
      >
        ☰
      </button>

      <aside className={`analytics-sidebar ${menuOpen ? "open" : ""}`}>

        <button
          className="analytics-close"
          onClick={() => setMenuOpen(false)}
        >
          ✕
        </button>

        <div className="analytics-header">
          Analytics
        </div>

        <nav className="analytics-nav">

          <NavLink to="" end className="nav-link">
            Overview
          </NavLink>

          <NavLink to="funnel" className="nav-link">
            Funnel
          </NavLink>

          <NavLink to="agents" className="nav-link">
            Agents
          </NavLink>

          <NavLink to="ai-impact" className="nav-link">
            AI Impact
          </NavLink>

          <NavLink to="sla" className="nav-link">
            SLA
          </NavLink>

        </nav>

      </aside>

      <main className="analytics-main">
        <Outlet />
      </main>

    </div>
  );
}