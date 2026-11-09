import { useState, useEffect } from "react";
import { NavLink, Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";
import {
  HomeIcon,
  DashboardIcon,
  ShieldCheckIcon,
  FileTextIcon,
  InterviewIcon,
  EvaluateIcon,
  ReportsIcon,
  AdminIcon,
  SunIcon,
  MoonIcon,
  LogOutIcon,
  LogInIcon,
  BrainCircuitIcon,
  MenuIcon,
  CloseIcon,
} from "./Icons";

const NAV_ITEMS = [
  { to: "/", label: "Home", icon: HomeIcon, roles: ["guest", "candidate", "recruiter"] },
  { to: "/ai-assistant", label: "AI Assistant", icon: BrainCircuitIcon, roles: ["guest", "candidate", "recruiter"] },
  { to: "/dashboard", label: "Dashboard", icon: DashboardIcon, roles: ["candidate", "recruiter"] },
  { to: "/verification", label: "Identity Check", icon: ShieldCheckIcon, roles: ["candidate"] },
  { to: "/resume-analysis", label: "Resume Analysis", icon: FileTextIcon, roles: ["candidate", "recruiter"] },
  { to: "/interview", label: "Take Interview", icon: InterviewIcon, roles: ["candidate", "recruiter"] },
  { to: "/interview-evaluation", label: "Evaluate Candidate", icon: EvaluateIcon, roles: ["recruiter"] },
  { to: "/reports", label: "Reports", icon: ReportsIcon, roles: ["recruiter", "candidate"] },
  { to: "/admin", label: "Admin Panel", icon: AdminIcon, roles: ["recruiter"] },
];

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  const role = user?.role || "guest";
  const visibleLinks = NAV_ITEMS.filter((item) => item.roles.includes(role));

  const initials = user?.name
    ? user.name
        .split(" ")
        .map((n) => n[0])
        .join("")
        .toUpperCase()
        .slice(0, 2)
    : "U";

  // Close mobile drawer on route change
  useEffect(() => {
    setMobileOpen(false);
  }, [location.pathname]);

  return (
    <div className="app-shell">
      {/* ── Top Navigation Bar ──────────────────────────────────────── */}
      <header className="top-navbar">
        <div className="top-nav-container">
          {/* Brand Logo */}
          <Link to="/" className="top-brand">
            <div className="brand-logo-icon">
              <BrainCircuitIcon size={22} />
            </div>
            <div className="brand-text-container">
              <span className="brand-title">AI Eval System</span>
              <span className="brand-tagline">Recruitment Intelligence</span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="top-nav-links">
            {visibleLinks.map((item) => {
              const IconComp = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.to === "/"}
                  className={({ isActive }) => `top-nav-link${isActive ? " active" : ""}`}
                >
                  <span className="top-nav-icon">
                    <IconComp size={17} />
                  </span>
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>

          {/* Right Header Actions */}
          <div className="top-nav-actions">
            {/* Theme Switcher Button */}
            <button
              className="top-theme-btn"
              onClick={toggleTheme}
              title={`Switch to ${theme === "dark" ? "Light" : "Dark"} Mode`}
              aria-label="Toggle Theme"
            >
              {theme === "dark" ? <SunIcon size={18} /> : <MoonIcon size={18} />}
            </button>

            {/* User Profile / Auth State */}
            {user ? (
              <div className="top-user-pill">
                <div className="top-user-avatar">{initials}</div>
                <div className="top-user-details">
                  <span className="top-user-name">{user.name}</span>
                  <span className={`top-role-badge ${user.role}`}>{user.role}</span>
                </div>
                <button
                  className="top-logout-btn"
                  onClick={logout}
                  title="Logout"
                  aria-label="Logout"
                >
                  <LogOutIcon size={15} />
                  <span className="logout-text">Logout</span>
                </button>
              </div>
            ) : (
              <div className="top-guest-actions">
                <Link to="/auth/candidate" className="top-login-btn">
                  <LogInIcon size={15} />
                  <span>Login</span>
                </Link>
              </div>
            )}

            {/* Mobile Menu Toggle Button */}
            <button
              className="top-mobile-toggle"
              onClick={() => setMobileOpen(!mobileOpen)}
              aria-label="Toggle navigation menu"
            >
              {mobileOpen ? <CloseIcon size={22} /> : <MenuIcon size={22} />}
            </button>
          </div>
        </div>

        {/* ── Mobile Dropdown Menu ──────────────────────────────────── */}
        {mobileOpen && (
          <div className="mobile-nav-drawer animate-fadeIn">
            <div className="mobile-nav-inner">
              <div className="mobile-nav-list">
                {visibleLinks.map((item) => {
                  const IconComp = item.icon;
                  return (
                    <NavLink
                      key={item.to}
                      to={item.to}
                      end={item.to === "/"}
                      onClick={() => setMobileOpen(false)}
                      className={({ isActive }) => `mobile-nav-link${isActive ? " active" : ""}`}
                    >
                      <span className="mobile-nav-icon">
                        <IconComp size={18} />
                      </span>
                      <span>{item.label}</span>
                    </NavLink>
                  );
                })}
              </div>

              <div className="mobile-nav-footer">
                {user ? (
                  <div className="mobile-user-row">
                    <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
                      <div className="top-user-avatar">{initials}</div>
                      <div>
                        <strong style={{ fontSize: "0.9rem", display: "block" }}>{user.name}</strong>
                        <span className={`top-role-badge ${user.role}`}>{user.role}</span>
                      </div>
                    </div>
                    <button
                      className="sidebar-button"
                      onClick={() => {
                        setMobileOpen(false);
                        logout();
                      }}
                      style={{ marginTop: "0.75rem" }}
                    >
                      <LogOutIcon size={16} /> Logout
                    </button>
                  </div>
                ) : (
                  <div style={{ display: "flex", gap: "0.5rem" }}>
                    <Link
                      to="/auth/candidate"
                      className="primary-button"
                      style={{ flex: 1, textAlign: "center", padding: "0.6rem 1rem", fontSize: "0.85rem" }}
                      onClick={() => setMobileOpen(false)}
                    >
                      Candidate Login
                    </Link>
                    <Link
                      to="/auth/recruiter"
                      className="secondary-button"
                      style={{ flex: 1, textAlign: "center", padding: "0.6rem 1rem", fontSize: "0.85rem" }}
                      onClick={() => setMobileOpen(false)}
                    >
                      Recruiter Login
                    </Link>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </header>

      {/* ── Main Content Body ────────────────────────────────────────── */}
      <main className="main-content">{children}</main>
    </div>
  );
}
