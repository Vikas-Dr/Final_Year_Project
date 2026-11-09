import { useEffect, useState } from "react";
import api from "../api";

export default function AdminPage() {
  const [roles, setRoles] = useState([]);
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newRole, setNewRole] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  useEffect(() => {
    Promise.all([
      api.get("/available-roles").then((r) => setRoles(r.data.roles)).catch(() => []),
      api.get("/reports").then((r) => setReports(r.data)).catch(() => []),
    ]).finally(() => setLoading(false));
  }, []);

  const handleAddRole = (e) => {
    e.preventDefault();
    if (!newRole.trim()) return;
    if (!roles.includes(newRole.trim())) {
      setRoles((prev) => [...prev, newRole.trim()]);
      setSuccessMsg(`Role "${newRole.trim()}" added to active memory list.`);
      setNewRole("");
      setTimeout(() => setSuccessMsg(""), 3000);
    }
  };

  return (
    <section>
      <div className="page-header">
        <p className="eyebrow">Admin</p>
        <h2 className="page-title">Admin Panel</h2>
        <p className="page-subtitle">System administration, role configuration, and platform management</p>
      </div>

      <div className="grid two">
        {/* Role Management */}
        <div className="card">
          <div className="section-title">⚙️ Job Role Configuration</div>
          <p className="helper-text" style={{ marginBottom: "1rem" }}>
            Active interview roles supported in question generation and job matching.
          </p>

          <div className="tag-row" style={{ marginBottom: "1.25rem" }}>
            {roles.map((r) => (
              <span className="tag blue" key={r} style={{ padding: "0.4rem 0.85rem", fontSize: "0.82rem" }}>
                {r}
              </span>
            ))}
          </div>

          <form onSubmit={handleAddRole} style={{ display: "flex", gap: "0.5rem" }}>
            <input
              type="text"
              placeholder="New Role Name (e.g. DevOps Engineer)..."
              value={newRole}
              onChange={(e) => setNewRole(e.target.value)}
            />
            <button className="primary-button" type="submit" style={{ whiteSpace: "nowrap" }}>
              + Add Role
            </button>
          </form>

          {successMsg && <p className="success-text">✅ {successMsg}</p>}
        </div>

        {/* Account & Access Details */}
        <div className="card">
          <div className="section-title">🔑 Seeded Demo Accounts</div>
          <p className="helper-text" style={{ marginBottom: "1rem" }}>
            Pre-configured users available for candidate and recruiter demonstration.
          </p>

          <div className="stack-list">
            <div className="list-row">
              <div>
                <strong>Candidate Account</strong>
                <p>candidate@example.com</p>
              </div>
              <span className="tag blue">candidate123</span>
            </div>
            <div className="list-row">
              <div>
                <strong>Recruiter Account</strong>
                <p>recruiter@example.com</p>
              </div>
              <span className="tag green">recruiter123</span>
            </div>
          </div>
        </div>
      </div>

      {/* System Status */}
      <div className="card" style={{ marginTop: "1.25rem" }}>
        <div className="section-title">📊 System Status & Scope</div>
        <div className="grid three">
          <div className="metric-panel" style={{ background: "var(--bg-3)" }}>
            <span>Active Roles</span>
            <strong>{roles.length}</strong>
          </div>
          <div className="metric-panel" style={{ background: "var(--bg-3)" }}>
            <span>Total Saved Reports</span>
            <strong>{reports.length}</strong>
          </div>
          <div className="metric-panel" style={{ background: "var(--bg-3)" }}>
            <span>NLP & AI Layer</span>
            <strong style={{ color: "var(--accent)" }}>Active (Rule + TF-IDF)</strong>
          </div>
        </div>
      </div>
    </section>
  );
}
