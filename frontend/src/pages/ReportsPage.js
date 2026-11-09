import { useEffect, useState } from "react";
import api from "../api";
import ReportModal from "../components/ReportModal";

export default function ReportsPage() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");
  const [expanded, setExpanded] = useState(null);
  const [previewReport, setPreviewReport] = useState(null);
  const [downloading, setDownloading] = useState(null);
  const [toast, setToast] = useState("");

  useEffect(() => {
    api.get("/reports")
      .then((r) => {
        if (Array.isArray(r.data)) setReports(r.data);
      })
      .catch((err) => {
        console.warn("Could not load reports:", err);
      })
      .finally(() => setLoading(false));
  }, []);

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(""), 3500);
  };

  const downloadPDF = async (report) => {
    setDownloading(report.id);
    try {
      const res = await api.get(`/report/${report.id}/pdf`, { responseType: "blob" });
      const url = URL.createObjectURL(new Blob([res.data], { type: "application/pdf" }));
      const a = document.createElement("a");
      a.href = url;
      a.download = `report_${report.candidate_name.replace(/\s/g, "_")}_${report.id}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
      showToast(`📥 PDF for ${report.candidate_name} downloaded successfully!`);
    } catch {
      alert("PDF download failed. Ensure the backend is running.");
    } finally {
      setDownloading(null);
    }
  };

  const filtered = reports.filter((r) => {
    if (!filter) return true;
    const q = filter.toLowerCase();
    return (
      r.candidate_name.toLowerCase().includes(q) ||
      r.role.toLowerCase().includes(q) ||
      r.recommendation?.toLowerCase().includes(q)
    );
  });

  const recColor = (rec) => {
    if (rec === "Highly Recommended") return "green";
    if (rec === "Recommended") return "blue";
    if (rec === "Job description needed") return "blue";
    if (rec === "Consider with Further Review") return "gold";
    return "red";
  };

  const scoreColor = (score) => (score >= 70 ? "#10b981" : score >= 50 ? "#f59e0b" : "#ef4444");

  return (
    <section>
      <div className="page-header">
        <p className="eyebrow">Reports</p>
        <h2 className="page-title">Candidate Reports</h2>
        <p className="page-subtitle">All evaluation results — resume, interview, and coding scores with PDF download</p>
      </div>

      {/* ── Summary Stats ── */}
      {reports.length > 0 && (
        <div className="grid three" style={{ marginBottom: "1.5rem" }}>
          <div className="stat-card">
            <div className="stat-icon blue">📋</div>
            <div className="stat-info">
              <label>Total Reports</label>
              <div className="stat-value">{reports.length}</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon green">✅</div>
            <div className="stat-info">
              <label>Recommended</label>
              <div className="stat-value">
                {reports.filter((r) => r.recommendation === "Highly Recommended" || r.recommendation === "Recommended").length}
              </div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon gold">📊</div>
            <div className="stat-info">
              <label>Average Score</label>
              <div className="stat-value">
                {reports.length
                  ? Math.round(reports.reduce((s, r) => s + r.overall_score, 0) / reports.length)
                  : 0}%
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── Filter Bar ── */}
      <div className="card" style={{ marginBottom: "1.25rem" }}>
        <input
          type="text"
          id="reports-filter"
          placeholder="🔍 Filter by candidate name, role, or recommendation..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
      </div>

      {/* ── Table ── */}
      <div className="card">
        {loading ? (
          <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
            {[1, 2, 3].map((i) => <div key={i} className="skeleton" style={{ height: 52 }} />)}
          </div>
        ) : filtered.length ? (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Candidate</th>
                  <th>Role</th>
                  <th>Resume score</th>
                  <th>Interview</th>
                  <th>Coding</th>
                  <th>Overall</th>
                  <th>Recommendation</th>
                  <th>Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((r, i) => (
                  <>
                    <tr
                      key={r.id}
                      style={{ cursor: "pointer" }}
                      onClick={() => setExpanded(expanded === r.id ? null : r.id)}
                    >
                      <td style={{ color: "var(--text-muted)" }}>{i + 1}</td>
                      <td><strong>{r.candidate_name}</strong></td>
                      <td style={{ color: "var(--text-muted)" }}>{r.role}</td>
                      <td>
                        <span style={{ color: scoreColor(r.resume_score), fontWeight: 700 }}>
                          {r.resume_score}%
                        </span>
                      </td>
                      <td>
                        <span style={{ color: scoreColor(r.interview_score), fontWeight: 700 }}>
                          {r.interview_score}%
                        </span>
                      </td>
                      <td>
                        <span style={{ color: scoreColor(r.coding_score), fontWeight: 700 }}>
                          {r.coding_score}%
                        </span>
                      </td>
                      <td>
                        <strong style={{ fontSize: "1rem", color: scoreColor(r.overall_score) }}>
                          {r.overall_score}%
                        </strong>
                      </td>
                      <td>
                        <span className={`tag ${recColor(r.recommendation)}`} style={{ fontSize: "0.72rem" }}>
                          {r.recommendation}
                        </span>
                      </td>
                      <td style={{ color: "var(--text-muted)", fontSize: "0.82rem" }}>
                        {r.created_at?.slice(0, 10)}
                      </td>
                      <td>
                        <div style={{ display: "flex", gap: "0.4rem" }}>
                          <button
                            className="secondary-button"
                            style={{ padding: "0.35rem 0.65rem", fontSize: "0.78rem" }}
                            onClick={(e) => { e.stopPropagation(); setPreviewReport(r); }}
                            title="Screen Preview"
                          >
                            👁️ Preview
                          </button>
                          <button
                            className="primary-button"
                            style={{ padding: "0.35rem 0.65rem", fontSize: "0.78rem" }}
                            disabled={downloading === r.id}
                            onClick={(e) => { e.stopPropagation(); downloadPDF(r); }}
                            id={`download-report-${r.id}`}
                          >
                            {downloading === r.id ? "⏳" : "📥 PDF"}
                          </button>
                        </div>
                      </td>
                    </tr>
                    {/* Expanded row */}
                    {expanded === r.id && (
                      <tr key={`exp-${r.id}`}>
                        <td colSpan={10} style={{ padding: "1.25rem", background: "var(--bg-3)" }}>
                          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.5rem" }}>
                            {r.feedback?.length > 0 && (
                              <div>
                                <div className="section-title" style={{ marginBottom: "0.75rem" }}>💬 Feedback</div>
                                {r.feedback.map((fb, fi) => (
                                  <p key={fi} style={{ fontSize: "0.85rem", color: "var(--text-muted)", marginBottom: "0.35rem" }}>→ {fb}</p>
                                ))}
                              </div>
                            )}
                            {r.questions_log?.length > 0 && (
                              <div>
                                <div className="section-title" style={{ marginBottom: "0.75rem" }}>📋 Q&A Summary</div>
                                {r.questions_log.slice(0, 5).map((q, qi) => (
                                  <div key={qi} style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.4rem", fontSize: "0.82rem" }}>
                                    <span style={{ color: "var(--text-muted)" }}>
                                      [{q.type}] {q.question?.slice(0, 50)}...
                                    </span>
                                    <span className={`tag ${q.score >= 70 ? "green" : q.score >= 40 ? "gold" : "red"}`} style={{ fontSize: "0.68rem" }}>
                                      {q.score}%
                                    </span>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        </td>
                      </tr>
                    )}
                  </>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="alert info">
            <span>💡</span>
            {filter ? `No reports match "${filter}". Clear the filter to see all reports.` : "No reports available yet. Upload a resume or submit an interview evaluation to create a report."}
          </div>
        )}
      </div>

      {/* ── Screen Modal Preview ── */}
      {previewReport && (
        <ReportModal
          report={previewReport}
          onClose={() => setPreviewReport(null)}
          onDownload={downloadPDF}
        />
      )}

      {/* ── Toast Notification ── */}
      {toast && (
        <div className="toast-notification animate-fadeInUp">
          <span>{toast}</span>
        </div>
      )}
    </section>
  );
}
