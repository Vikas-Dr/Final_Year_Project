import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import api from "../api";
import { useAuth } from "../context/AuthContext";

const ROLE_CONFIG = {
  candidate: {
    title: "Candidate Login",
    desc: "Upload your resume, take AI-generated interviews, and view your performance scores.",
    email: "candidate@example.com",
    password: "candidate123",
    icon: "👤",
    color: "var(--primary)",
  },
  recruiter: {
    title: "Recruiter Login",
    desc: "Access the dashboard, evaluate candidates, and download structured performance reports.",
    email: "recruiter@example.com",
    password: "recruiter123",
    icon: "🏢",
    color: "var(--accent)",
  },
};

export default function AuthPage() {
  const { role = "candidate" } = useParams();
  const selectedRole = role === "recruiter" ? "recruiter" : "candidate";
  const config = ROLE_CONFIG[selectedRole];
  const navigate = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState(config.email);
  const [password, setPassword] = useState(config.password);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await api.post("/auth/login", { email, password, role: selectedRole });
      login({ user: res.data.user, accessToken: res.data.access_token });
      navigate(selectedRole === "candidate" ? "/verification" : "/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-outer">
      <div className="auth-card animate-scaleIn">
        {/* Role Icon */}
        <div style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>{config.icon}</div>

        <div className="eyebrow">{selectedRole === "candidate" ? "Candidate Access" : "Recruiter Access"}</div>
        <h2>{config.title}</h2>
        <p className="auth-desc">{config.desc}</p>

        {/* Demo Credentials Box */}
        <div className="auth-demo-box">
          <strong>Demo credentials:</strong> {config.email} / {selectedRole === "candidate" ? "candidate123" : "recruiter123"}
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="field-label">Email Address</label>
            <input
              id="auth-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              autoComplete="email"
            />
          </div>

          <div className="form-group">
            <label className="field-label">Password</label>
            <input
              id="auth-password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              autoComplete="current-password"
            />
          </div>

          {error && <p className="error-text">⚠️ {error}</p>}

          <button className="primary-button auth-submit-btn" type="submit" disabled={loading} id="auth-submit-btn">
            {loading ? "Signing in..." : `Login as ${selectedRole.charAt(0).toUpperCase() + selectedRole.slice(1)} →`}
          </button>
        </form>

        <div className="auth-switch">
          Need a different role?{" "}
          <Link to={selectedRole === "candidate" ? "/auth/recruiter" : "/auth/candidate"}>
            Switch to {selectedRole === "candidate" ? "Recruiter" : "Candidate"} login
          </Link>
        </div>
      </div>
    </div>
  );
}
