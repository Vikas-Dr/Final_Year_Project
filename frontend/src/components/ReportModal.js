import ScoreRing from "./ScoreRing";
import ProgressBar from "./ProgressBar";

export default function ReportModal({ report, onClose, onDownload }) {
  if (!report) return null;

  const scoreColor = (score) => (score >= 70 ? "#10b981" : score >= 50 ? "#f59e0b" : "#ef4444");

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content animate-scaleIn" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose} title="Close">
          ✕
        </button>

        <div style={{ marginBottom: "1.5rem" }}>
          <div className="eyebrow">Candidate Report Preview</div>
          <h2 style={{ fontSize: "1.6rem", fontWeight: 800, marginTop: "0.2rem" }}>
            {report.candidate_name}
          </h2>
          <p style={{ color: "var(--text-muted)", fontSize: "0.9rem" }}>
            Applied Role: <strong style={{ color: "var(--text)" }}>{report.role}</strong> · Submitted: {report.created_at?.slice(0, 10) || "Recent"}
          </p>
        </div>

        {/* Score Ring Summary */}
        <div style={{ display: "flex", justifyContent: "space-around", flexWrap: "wrap", gap: "1rem", marginBottom: "1.5rem", padding: "1.25rem", background: "var(--bg-3)", border: "1px solid var(--glass-border)", borderRadius: "var(--radius-lg)" }}>
          <ScoreRing score={report.resume_score} size={85} color="#3b82f6" label="Resume" />
          <ScoreRing score={report.interview_score} size={85} color="#8b5cf6" label="Interview" />
          <ScoreRing score={report.coding_score} size={85} color="#10b981" label="Coding" />
          <ScoreRing score={report.overall_score} size={85} color={scoreColor(report.overall_score)} label="Overall" />
        </div>

        {/* Status Badge */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "1rem 1.25rem", background: "var(--bg-3)", border: "1px solid var(--glass-border)", borderRadius: "var(--radius-md)", marginBottom: "1.5rem" }}>
          <span style={{ fontSize: "0.85rem", color: "var(--text-muted)", fontWeight: 600 }}>FINAL RECOMMENDATION</span>
          <span className={`rec-badge ${report.recommendation}`}>
            {report.recommendation}
          </span>
        </div>

        {/* Progress Breakdown */}
        <ProgressBar label="Resume Score" value={report.resume_score} color="blue" />
        <ProgressBar label="Interview Score" value={report.interview_score} color="purple" />
        <ProgressBar label="Coding Test Cases" value={report.coding_score} color="green" />
        <ProgressBar label="Overall Score" value={report.overall_score} color="teal" />

        {/* Feedback List */}
        {report.feedback?.length > 0 && (
          <div style={{ marginTop: "1.5rem" }}>
            <div className="section-title">💬 Performance Feedback</div>
            <div className="feedback-list">
              {report.feedback.map((fb, i) => (
                <div className="feedback-item" key={i}>
                  <span className="fb-icon">📌</span>
                  <span>{fb}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Modal Actions */}
        <div style={{ display: "flex", gap: "1rem", marginTop: "2rem" }}>
          <button className="secondary-button" style={{ flex: 1 }} onClick={onClose}>
            Close Preview
          </button>
          {onDownload && (
            <button className="primary-button" style={{ flex: 1 }} onClick={() => onDownload(report)}>
              📥 Download Official PDF
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
