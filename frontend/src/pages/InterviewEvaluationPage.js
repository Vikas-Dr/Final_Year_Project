import { useState } from "react";
import api from "../api";
import ScoreRing from "../components/ScoreRing";
import ProgressBar from "../components/ProgressBar";

const SAMPLE_ANSWERS = [
  {
    question: "Tell us about your experience with Python and backend development.",
    answer: "I have worked with Python, FastAPI, Flask, SQL, and REST APIs in multiple academic and internship projects. I built a recruitment dashboard backend using FastAPI with MySQL.",
  },
  {
    question: "How would you design a resume analysis system using NLP?",
    answer: "I would extract text from PDF using pdfplumber, then use NLTK and scikit-learn for skill extraction and TF-IDF similarity. The system compares resume keywords with job descriptions and generates a match score.",
  },
  {
    question: "Explain the difference between supervised and unsupervised learning.",
    answer: "Supervised learning uses labeled training data with known outputs like classification or regression. Unsupervised learning finds patterns in unlabeled data through clustering or dimensionality reduction.",
  },
];

export default function InterviewEvaluationPage() {
  const [candidateName, setCandidateName] = useState("Rahul Sharma");
  const [jobRole, setJobRole] = useState("AI Engineer");
  const [answers, setAnswers] = useState(SAMPLE_ANSWERS);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const updateAnswer = (i, field, val) => {
    setAnswers((prev) => prev.map((a, idx) => idx === i ? { ...a, [field]: val } : a));
  };

  const addQuestion = () => {
    setAnswers((prev) => [...prev, { question: "", answer: "" }]);
  };

  const removeQuestion = (i) => {
    setAnswers((prev) => prev.filter((_, idx) => idx !== i));
  };

  const handleSubmit = async () => {
    if (!candidateName.trim() || !jobRole.trim()) { setError("Please enter candidate name and job role."); return; }
    if (answers.some((a) => !a.question.trim() || !a.answer.trim())) { setError("Please fill all question and answer fields."); return; }
    setError("");
    setLoading(true);
    try {
      const res = await api.post("/evaluate-interview", {
        candidate_name: candidateName,
        job_role: jobRole,
        answers,
      });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Evaluation failed. Ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = async (reportId) => {
    try {
      const res = await api.get(`/report/${reportId}/pdf`, { responseType: "blob" });
      const url = URL.createObjectURL(new Blob([res.data], { type: "application/pdf" }));
      const a = document.createElement("a");
      a.href = url;
      a.download = `evaluation_report_${reportId}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      alert("PDF download failed.");
    }
  };

  const ev = result?.evaluation;

  return (
    <section>
      <div className="page-header">
        <p className="eyebrow">Module 2</p>
        <h2 className="page-title">Candidate Evaluation</h2>
        <p className="page-subtitle">Recruiter view — enter candidate answers and generate an AI evaluation report</p>
      </div>

      <div className="grid two">
        {/* ── Input Panel ── */}
        <div className="card">
          <div className="section-title">📝 Evaluation Form</div>

          <div className="form-group">
            <label className="field-label">Candidate Name</label>
            <input
              id="eval-candidate-name"
              value={candidateName}
              onChange={(e) => setCandidateName(e.target.value)}
              placeholder="e.g. Rahul Sharma"
            />
          </div>

          <div className="form-group">
            <label className="field-label">Job Role</label>
            <input
              id="eval-job-role"
              value={jobRole}
              onChange={(e) => setJobRole(e.target.value)}
              placeholder="e.g. AI Engineer"
            />
          </div>

          <div className="section-divider" />
          <div className="section-title">💬 Interview Q&A</div>

          {answers.map((entry, i) => (
            <div
              key={i}
              style={{
                background: "var(--bg-3)",
                borderRadius: "var(--radius-md)",
                padding: "1rem",
                marginBottom: "1rem",
                border: "1px solid var(--glass-border)",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem" }}>
                <span style={{ fontSize: "0.75rem", fontWeight: 700, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.06em" }}>
                  Q{i + 1}
                </span>
                {answers.length > 1 && (
                  <button className="danger-button" style={{ padding: "0.25rem 0.6rem", fontSize: "0.75rem" }} onClick={() => removeQuestion(i)}>
                    Remove
                  </button>
                )}
              </div>
              <div className="form-group" style={{ marginBottom: "0.75rem" }}>
                <label className="field-label">Question</label>
                <input
                  value={entry.question}
                  onChange={(e) => updateAnswer(i, "question", e.target.value)}
                  placeholder="Interview question..."
                  id={`eval-q-${i}`}
                />
              </div>
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label className="field-label">Candidate Answer</label>
                <textarea
                  rows={4}
                  value={entry.answer}
                  onChange={(e) => updateAnswer(i, "answer", e.target.value)}
                  placeholder="Candidate's answer..."
                  id={`eval-a-${i}`}
                />
              </div>
            </div>
          ))}

          <button className="secondary-button" onClick={addQuestion} style={{ marginBottom: "1rem", width: "100%" }}>
            + Add Question
          </button>

          {error && <p className="error-text">⚠️ {error}</p>}

          <button className="primary-button" onClick={handleSubmit} disabled={loading} style={{ width: "100%" }} id="evaluate-btn">
            {loading ? "⏳ Evaluating..." : "🔍 Evaluate Candidate"}
          </button>
        </div>

        {/* ── Result Panel ── */}
        <div className="card">
          <div className="section-title">📊 Evaluation Result</div>

          {!ev && !loading && (
            <div className="alert info">
              <span>💡</span>
              Fill in the candidate details and interview Q&A, then click Evaluate Candidate.
            </div>
          )}

          {loading && (
            <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="skeleton" style={{ height: 50 }} />
              ))}
            </div>
          )}

          {ev && (
            <div className="animate-fadeIn">
              {/* Score Rings */}
              <div style={{ display: "flex", justifyContent: "space-around", marginBottom: "1.5rem", padding: "1.25rem", background: "var(--bg-3)", borderRadius: "var(--radius-md)" }}>
                <ScoreRing score={ev.communication_score} size={80} color="#3b82f6" label="Communication" />
                <ScoreRing score={ev.technical_score} size={80} color="#8b5cf6" label="Technical" />
                <ScoreRing score={ev.confidence_score} size={80} color="#14b8a6" label="Confidence" />
              </div>

              {/* Progress Bars */}
              <ProgressBar label="Communication" value={ev.communication_score} color="blue" />
              <ProgressBar label="Technical Knowledge" value={ev.technical_score} color="purple" />
              <ProgressBar label="Confidence" value={ev.confidence_score} color="teal" />

              <div className="section-divider" />

              {/* Overall + Recommendation */}
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "1rem", background: "var(--bg-3)", borderRadius: "var(--radius-md)", marginBottom: "1rem" }}>
                <div>
                  <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", fontWeight: 600, textTransform: "uppercase" }}>Overall Score</div>
                  <div style={{ fontSize: "2rem", fontWeight: 900 }}>{ev.overall_score}%</div>
                </div>
                <span className={`rec-badge ${ev.recommendation}`}>
                  {ev.recommendation}
                </span>
              </div>

              {/* Feedback */}
              <div className="section-title">💬 Feedback</div>
              <div className="feedback-list">
                {ev.feedback?.map((fb, i) => (
                  <div className="feedback-item" key={i}>
                    <span className="fb-icon">{i % 2 === 0 ? "📌" : "💡"}</span>
                    <span>{fb}</span>
                  </div>
                ))}
              </div>

              {result?.report?.id && (
                <button
                  className="secondary-button"
                  style={{ marginTop: "1rem", width: "100%" }}
                  onClick={() => downloadPDF(result.report.id)}
                  id="eval-download-pdf-btn"
                >
                  📥 Download PDF Report
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
