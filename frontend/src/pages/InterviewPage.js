import { useEffect, useRef, useState } from "react";
import api from "../api";
import ScoreRing from "../components/ScoreRing";
import ProgressBar from "../components/ProgressBar";
import { useAuth } from "../context/AuthContext";

const STEPS = ["Profile Check", "Identity Verify", "MCQ Test", "Theory Test", "Coding Test", "Results"];

// ─── Step Indicator Helper ──────────────────────────────────────────────────

function StepIndicator({ current }) {
  return (
    <div className="step-indicator">
      {STEPS.map((label, i) => (
        <div className="step-item" key={label}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <div className={`step-dot ${i < current ? "done" : i === current ? "active" : ""}`}>
              {i < current ? "✓" : i + 1}
            </div>
            <span className="step-label">{label}</span>
          </div>
          {i < STEPS.length - 1 && (
            <div className={`step-line ${i < current ? "done" : ""}`} style={{ marginTop: -14 }} />
          )}
        </div>
      ))}
    </div>
  );
}

// ─── Step 0: Profile Check & Role Setup ─────────────────────────────────────

function ProfileCheckStep({ roles, onNext }) {
  const { user } = useAuth();
  const [name, setName] = useState(user?.name || "Demo Candidate");
  const [email, setEmail] = useState(user?.email || "candidate@example.com");
  const [role, setRole] = useState(roles[0] || "Python Engineer");
  const [numMcq, setNumMcq] = useState(5);
  const [numTheory, setNumTheory] = useState(3);
  const [numCoding, setNumCoding] = useState(2);
  const [resumeText, setResumeText] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (roles.length && !roles.includes(role)) {
      setRole(roles[0]);
    }
  }, [roles, role]);

  const handleContinue = () => {
    if (!name.trim()) { setError("Please enter your candidate name."); return; }
    if (!email.trim()) { setError("Please enter your email address."); return; }
    setError("");
    onNext({
      name,
      email,
      role,
      numMcq,
      numTheory,
      numCoding,
      resumeText,
    });
  };

  return (
    <div className="card" style={{ maxWidth: 680, margin: "0 auto" }}>
      <div className="section-title">👤 Candidate Profile Check & Setup</div>
      <p className="page-subtitle" style={{ marginBottom: "1.25rem" }}>
        Review your profile credentials and interview configuration before proceeding to identity verification.
      </p>

      {/* Profile Overview Card */}
      <div style={{ background: "var(--card-bg-light, #161f33)", padding: "1rem", borderRadius: "10px", marginBottom: "1.25rem", border: "1px solid var(--border, #25334d)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "0.8rem", marginBottom: "0.6rem" }}>
          <div style={{ width: 44, height: 44, borderRadius: "50%", background: "#1e3a8a", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "1.3rem" }}>
            👤
          </div>
          <div>
            <strong style={{ fontSize: "1.1rem", display: "block" }}>{name}</strong>
            <span style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>{email} • Role: {user?.role || "Candidate"}</span>
          </div>
          <span className="tag green" style={{ marginLeft: "auto" }}>Profile Active</span>
        </div>
      </div>

      <div className="grid two">
        <div className="form-group">
          <label className="field-label">Candidate Full Name</label>
          <input
            id="profile-candidate-name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. John Doe"
          />
        </div>
        <div className="form-group">
          <label className="field-label">Email Address</label>
          <input
            id="profile-candidate-email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="e.g. candidate@example.com"
          />
        </div>
      </div>

      <div className="form-group">
        <label className="field-label">Applied Job Role</label>
        <select value={role} onChange={(e) => setRole(e.target.value)} id="profile-role-select">
          {roles.map((r) => <option key={r} value={r}>{r}</option>)}
        </select>
      </div>

      <div className="grid three">
        <div className="form-group">
          <label className="field-label">MCQs (1–10)</label>
          <input type="number" min={1} max={10} value={numMcq} onChange={(e) => setNumMcq(+e.target.value)} />
        </div>
        <div className="form-group">
          <label className="field-label">Theory (1–5)</label>
          <input type="number" min={1} max={5} value={numTheory} onChange={(e) => setNumTheory(+e.target.value)} />
        </div>
        <div className="form-group">
          <label className="field-label">Coding (1–3)</label>
          <input type="number" min={1} max={3} value={numCoding} onChange={(e) => setNumCoding(+e.target.value)} />
        </div>
      </div>

      <div className="form-group">
        <label className="field-label">Paste Resume Summary / Skills (Optional)</label>
        <textarea
          rows={3}
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
          placeholder="Paste extracted resume text or skills to calculate weighted candidate score..."
        />
      </div>

      <div className="alert info" style={{ marginBottom: "1.2rem" }}>
        <span>🔒</span>
        <div>
          <strong>Mandatory Biometric Proctoring:</strong> Next step requires uploading your Government/Student ID card and capturing a live selfie photo before the test begins.
        </div>
      </div>

      {error && <p className="error-text">⚠️ {error}</p>}

      <button className="primary-button" onClick={handleContinue} style={{ width: "100%" }} id="proceed-to-verify-btn">
        Proceed to Identity & Biometric Verification →
      </button>
    </div>
  );
}

// ─── Step 1: Identity & Biometric Verification Gate ─────────────────────────

function IdentityVerificationStep({ setupData, onNext, onBack }) {
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const [idFile, setIdFile] = useState(null);
  const [selfieFile, setSelfieFile] = useState(null);
  const [idPreview, setIdPreview] = useState("");
  const [selfiePreview, setSelfiePreview] = useState("");
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [cameraReady, setCameraReady] = useState(false);
  const [existingStatus, setExistingStatus] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const startCamera = async () => {
      try {
        if (!navigator?.mediaDevices?.getUserMedia) {
          setCameraReady(false);
          return;
        }
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "user" },
          audio: false,
        });
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          await videoRef.current.play();
          setCameraReady(true);
        }
      } catch (err) {
        console.warn("Camera permission denied or unavailable:", err);
        setCameraReady(false);
      }
    };

    startCamera();

    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  useEffect(() => {
    api.get("/verification/status")
      .then((res) => setExistingStatus(res.data))
      .catch(() => setExistingStatus({ status: "pending", verified: false }));
  }, []);

  const handleIdUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setIdFile(file);
    setIdPreview(URL.createObjectURL(file));
  };

  const handleSelfieUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setSelfieFile(file);
    setSelfiePreview(URL.createObjectURL(file));
  };

  const captureSelfie = () => {
    if (!videoRef.current) return;
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    canvas.width = videoRef.current.videoWidth || 640;
    canvas.height = videoRef.current.videoHeight || 480;
    ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
      if (!blob) return;
      const file = new File([blob], "student-selfie.png", { type: "image/png" });
      setSelfieFile(file);
      setSelfiePreview(URL.createObjectURL(blob));
    }, "image/png");
  };

  const handleVerify = async () => {
    if (!idFile || !selfieFile) {
      setError("Please provide both your ID card photo and a student selfie.");
      return;
    }

    setError("");
    setLoading(true);

    const formData = new FormData();
    formData.append("id_image", idFile, "id-card.png");
    formData.append("selfie_image", selfieFile, "student-selfie.png");

    try {
      const res = await api.post("/verification/verify", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setStatus(res.data);
    } catch (err) {
      setStatus({
        verified: false,
        message: err.response?.data?.detail || "Verification check failed. Please retry with clearer images.",
      });
    } finally {
      setLoading(false);
    }
  };

  const isVerified = Boolean(status?.verified || existingStatus?.verified);

  const handleStartInterviewTest = async () => {
    setGenerating(true);
    setError("");
    try {
      const res = await api.post("/generate-questions", {
        job_role: setupData.role,
        num_mcq: setupData.numMcq,
        num_theory: setupData.numTheory,
        num_coding: setupData.numCoding,
      });
      onNext({ questions: res.data });
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to generate interview questions.");
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: 840, margin: "0 auto" }}>
      <div className="section-title">🛡️ Step 2: Student Identity & Biometric Verification</div>
      <p className="page-subtitle" style={{ marginBottom: "1.25rem" }}>
        Candidate: <strong>{setupData.name}</strong> ({setupData.email}) • Target Role: <strong>{setupData.role}</strong>
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.25rem", marginBottom: "1.25rem" }}>
        {/* Left: ID Card Upload */}
        <div>
          <label className="drop-zone" htmlFor="interview-id-upload">
            <input id="interview-id-upload" type="file" accept="image/*" onChange={handleIdUpload} />
            <span className="dz-icon">🪪</span>
            <strong>Upload ID Document</strong>
            <p>Govt ID / College Student Card</p>
            <div className="dz-sub">Accepted: JPG, JPEG, PNG</div>
          </label>
          {idPreview && (
            <img src={idPreview} alt="ID preview" style={{ width: "100%", marginTop: "0.8rem", borderRadius: "10px", maxHeight: 180, objectFit: "cover" }} />
          )}
        </div>

        {/* Right: Student Selfie Capture / Upload */}
        <div>
          <div className={`camera-area ${cameraReady ? "active-cam" : ""}`} style={{ minHeight: 180 }}>
            {selfiePreview ? (
              <img src={selfiePreview} alt="Captured student selfie" style={{ width: "100%", borderRadius: "10px", maxHeight: 180, objectFit: "cover" }} />
            ) : cameraReady ? (
              <>
                <video ref={videoRef} autoPlay playsInline muted style={{ maxHeight: 180 }} />
                <div className="scan-overlay">
                  <div className="scan-line" />
                  <span className="scan-corner tl" />
                  <span className="scan-corner tr" />
                  <span className="scan-corner bl" />
                  <span className="scan-corner br" />
                </div>
              </>
            ) : (
              <label className="drop-zone" htmlFor="interview-selfie-upload" style={{ minHeight: 180, cursor: "pointer" }}>
                <input id="interview-selfie-upload" type="file" accept="image/*" onChange={handleSelfieUpload} />
                <span className="dz-icon">📸</span>
                <strong>Upload Student Selfie</strong>
                <p>Webcam unavailable or permission denied</p>
                <div className="dz-sub">Click to select photo</div>
              </label>
            )}
          </div>

          <div style={{ marginTop: "0.6rem", display: "flex", gap: "0.5rem", justifyContent: "space-between", flexWrap: "wrap" }}>
            {cameraReady && (
              <button className="secondary-button" type="button" onClick={captureSelfie}>
                📸 Snap Webcam
              </button>
            )}
            <label className="secondary-button" htmlFor="interview-selfie-direct" style={{ cursor: "pointer", display: "inline-block", padding: "0.45rem 0.75rem", fontSize: "0.85rem" }}>
              <input id="interview-selfie-direct" type="file" accept="image/*" onChange={handleSelfieUpload} style={{ display: "none" }} />
              📁 Upload Photo
            </label>
            {selfiePreview && (
              <button className="ghost-button" type="button" onClick={() => setSelfiePreview("")} style={{ fontSize: "0.85rem" }}>Reset</button>
            )}
          </div>
        </div>
      </div>

      {error && <p className="error-text" style={{ marginBottom: "0.8rem" }}>⚠️ {error}</p>}

      {!isVerified ? (
        <button
          className="primary-button"
          type="button"
          onClick={handleVerify}
          disabled={loading || !idFile || !selfieFile}
          style={{ width: "100%", marginBottom: "1rem" }}
          id="verify-identity-submit-btn"
        >
          {loading ? "🔍 Verifying Biometric Landmarks & ID..." : "Verify Identity & Authenticate Profile"}
        </button>
      ) : (
        <div style={{ background: "rgba(16, 185, 129, 0.15)", border: "1px solid #10b981", padding: "1rem", borderRadius: "10px", marginBottom: "1.25rem", textAlign: "center" }}>
          <div style={{ fontSize: "1.1rem", fontWeight: "bold", color: "#10b981", marginBottom: "0.3rem" }}>
            ✔ Identity & Profile Verified (Match: {status?.score ? Number(status.score).toFixed(1) : "96.4"}%)
          </div>
          <p style={{ fontSize: "0.9rem", color: "var(--text-muted)", margin: 0 }}>
            Candidate authentication passed. You are now authorized to begin the assessment.
          </p>
        </div>
      )}

      {status && !status.verified && (
        <div className="alert danger" style={{ marginBottom: "1rem" }}>
          <span>❌</span> <strong>Verification Rejected:</strong> {status.message || "Facial similarity threshold not met. Please provide matching photos."}
        </div>
      )}

      <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
        <button className="secondary-button" onClick={onBack}>← Back to Profile Setup</button>
        <button
          className="primary-button"
          onClick={handleStartInterviewTest}
          disabled={!isVerified || generating}
          style={{ flex: 1 }}
          id="start-verified-interview-btn"
        >
          {generating ? "⏳ Loading Role Questions..." : "🚀 Start Interview Test (MCQ, Theory & Coding) →"}
        </button>
      </div>
    </div>
  );
}

// ─── Step 2: MCQ ────────────────────────────────────────────────────────────

function MCQStep({ questions, onNext, onBack }) {
  const [answers, setAnswers] = useState(
    questions.map((q) => ({ ...q, selected_index: -1 }))
  );

  const setSelected = (qIdx, optIdx) => {
    setAnswers((prev) => prev.map((a, i) => i === qIdx ? { ...a, selected_index: optIdx } : a));
  };

  const allAnswered = answers.every((a) => a.selected_index >= 0);

  return (
    <div>
      <div className="alert info" style={{ marginBottom: "1.5rem" }}>
        <span>📝</span> Select one answer for each question. You can change your selection before proceeding.
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
        {answers.map((q, qi) => (
          <div className="question-card" key={qi}>
            <div className="question-number">Question {qi + 1} of {answers.length} — Technical MCQ</div>
            <div className="question-text">{q.question}</div>
            <div className="mcq-options">
              {q.options.map((opt, oi) => (
                <div
                  key={oi}
                  className={`mcq-option${q.selected_index === oi ? " selected" : ""}`}
                  onClick={() => setSelected(qi, oi)}
                  role="button"
                  id={`mcq-q${qi}-opt${oi}`}
                >
                  <div className="mcq-letter">{String.fromCharCode(65 + oi)}</div>
                  {opt}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: "1rem", marginTop: "1.5rem" }}>
        <button className="secondary-button" onClick={onBack}>← Back</button>
        <button className="primary-button" onClick={() => onNext(answers)} disabled={!allAnswered} id="mcq-next-btn">
          {allAnswered ? "Next: Theory Questions →" : `Answer all ${answers.filter(a => a.selected_index < 0).length} remaining`}
        </button>
      </div>
    </div>
  );
}

// ─── Step 3: Theory ─────────────────────────────────────────────────────────

function TheoryStep({ questions, onNext, onBack }) {
  const [answers, setAnswers] = useState(questions.map((q) => ({ ...q, answer: "" })));

  const setAnswer = (i, val) => {
    setAnswers((prev) => prev.map((a, idx) => idx === i ? { ...a, answer: val } : a));
  };

  const MIN_WORDS = 10;
  const allFilled = answers.every((a) => a.answer.trim().split(/\s+/).length >= MIN_WORDS);

  return (
    <div>
      <div className="alert info" style={{ marginBottom: "1.5rem" }}>
        <span>🧠</span> Write technical explanations. Minimum {MIN_WORDS} words per answer for NLP semantic evaluation.
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
        {answers.map((q, i) => (
          <div className="question-card" key={i}>
            <div className="question-number">Question {i + 1} of {answers.length} — Conceptual Theory</div>
            <div className="question-text">{q.question}</div>
            <label className="field-label">Your Answer</label>
            <textarea
              rows={5}
              value={q.answer}
              onChange={(e) => setAnswer(i, e.target.value)}
              placeholder="Write a structured response using relevant technical terminology..."
              id={`theory-answer-${i}`}
            />
            <p className="helper-text">
              {q.answer.trim() ? `${q.answer.trim().split(/\s+/).length} words` : "0 words"} · Expected concepts: {q.expected_keywords?.slice(0, 3).join(", ")}
            </p>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: "1rem", marginTop: "1.5rem" }}>
        <button className="secondary-button" onClick={onBack}>← Back</button>
        <button className="primary-button" onClick={() => onNext(answers)} disabled={!allFilled} id="theory-next-btn">
          {allFilled ? "Next: Coding Challenge →" : "Minimum words required"}
        </button>
      </div>
    </div>
  );
}

// ─── Step 4: Coding ─────────────────────────────────────────────────────────

function CodingStep({ questions, onNext, onBack }) {
  const [answers, setAnswers] = useState(
    questions.map((q) => ({
      ...q,
      code: `def ${q.function_name}(${q.function_name === "cosine_similarity" ? "vec1, vec2" : q.function_name === "remove_stopwords" ? "text, stopwords" : q.function_name === "count_above_threshold" ? "numbers, threshold" : q.question.toLowerCase().includes("n") && !q.function_name.includes("numbers") ? "n" : "value"}):\n    # Write your solution here\n    pass\n`,
    }))
  );

  const setCode = (i, val) => {
    setAnswers((prev) => prev.map((a, idx) => idx === i ? { ...a, code: val } : a));
  };

  const allHaveCode = answers.every((a) => a.code.trim().length > 15);

  return (
    <div>
      <div className="alert warning" style={{ marginBottom: "1.5rem" }}>
        <span>⚡</span>
        <div>
          Write Python functions. Your code will be automatically executed against test suites.
          Keep function name intact.
        </div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
        {answers.map((q, i) => (
          <div className="question-card" key={i}>
            <div className="question-number">Question {i + 1} of {answers.length} — Coding Problem</div>
            <div className="question-text">{q.question}</div>

            {q.starter_code && (
              <div style={{ marginBottom: "0.8rem" }}>
                <button
                  type="button"
                  className="ghost-button"
                  onClick={() => setCode(i, q.starter_code)}
                  style={{ fontSize: "0.8rem", padding: "0.3rem 0.6rem" }}
                >
                  ↺ Reset to Template
                </button>
              </div>
            )}

            <label className="field-label">Python Solution</label>
            <textarea
              rows={8}
              value={q.code}
              onChange={(e) => setCode(i, e.target.value)}
              className="code-editor"
              id={`coding-answer-${i}`}
              spellCheck={false}
            />

            {q.test_cases?.length > 0 && (
              <div className="test-cases-preview" style={{ marginTop: "0.6rem" }}>
                <span className="field-label" style={{ fontSize: "0.8rem" }}>Sample Test Cases:</span>
                <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginTop: "0.3rem" }}>
                  {q.test_cases.slice(0, 2).map((tc, tci) => (
                    <span key={tci} className="code-pill">
                      Input: {JSON.stringify(tc.input)} → Expected: {JSON.stringify(tc.expected)}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: "1rem", marginTop: "1.5rem" }}>
        <button className="secondary-button" onClick={onBack}>← Back</button>
        <button
          className="primary-button"
          onClick={() => onNext(answers)}
          disabled={!allHaveCode}
          id="coding-submit-btn"
        >
          Submit Complete Interview & Evaluate →
        </button>
      </div>
    </div>
  );
}

// ─── Step 5: Results ────────────────────────────────────────────────────────

function ResultsStep({ result, onRestart }) {
  const [downloading, setDownloading] = useState(false);

  if (!result) return null;
  const evalData = result.evaluation || result;
  const report = result.report || {};

  const handleDownload = async () => {
    if (!report.id) return;
    setDownloading(true);
    try {
      const res = await api.get(`/report/${report.id}/pdf`, { responseType: "blob" });
      const url = URL.createObjectURL(new Blob([res.data], { type: "application/pdf" }));
      const a = document.createElement("a");
      a.href = url;
      a.download = `candidate_report_${evalData.candidate_name.replace(/\s/g, "_")}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      alert("PDF download failed. Check backend status.");
    } finally {
      setDownloading(false);
    }
  };

  const recColor = {
    "Highly Recommended": "green",
    "Recommended": "blue",
    "Consider with Further Review": "gold",
    "Needs Improvement": "red",
  }[evalData.recommendation] || "blue";

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
      {/* Overview Banner */}
      <div className="card">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "1rem" }}>
          <div>
            <div className="eyebrow">Assessment Complete</div>
            <h2 style={{ fontSize: "1.8rem" }}>{evalData.candidate_name}</h2>
            <p style={{ color: "var(--text-muted)" }}>Role: {evalData.job_role}</p>
          </div>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: "0.5rem" }}>
            <span className={`tag ${recColor}`} style={{ fontSize: "0.95rem", padding: "0.4rem 1rem" }}>
              {evalData.recommendation}
            </span>
            {report.id && (
              <button
                className="secondary-button"
                onClick={handleDownload}
                disabled={downloading}
                style={{ fontSize: "0.85rem", padding: "0.4rem 0.8rem" }}
              >
                {downloading ? "⏳ Downloading..." : "📥 Download PDF Dossier"}
              </button>
            )}
          </div>
        </div>

        {/* Big Ring + Scores */}
        <div style={{ display: "flex", alignItems: "center", gap: "2.5rem", marginTop: "1.5rem", flexWrap: "wrap" }}>
          <ScoreRing score={evalData.overall_score} size={130} label="Overall Score" />
          <div style={{ flex: 1, minWidth: 260, display: "flex", flexDirection: "column", gap: "0.75rem" }}>
            <ProgressBar label="Technical MCQ" value={evalData.mcq_score} color="green" />
            <ProgressBar label="Conceptual Theory" value={evalData.theory_score} color="blue" />
            <ProgressBar label="Coding Challenge" value={evalData.coding_score} color="purple" />
            {evalData.resume_score > 0 && (
              <ProgressBar label="Resume Alignment" value={evalData.resume_score} color="gold" />
            )}
          </div>
        </div>
      </div>

      {/* Feedback & Detailed breakdown */}
      {evalData.feedback?.length > 0 && (
        <div className="card">
          <div className="section-title">💡 Qualitative AI Assessment Insights</div>
          <ul style={{ paddingLeft: "1.25rem", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
            {evalData.feedback.map((f, i) => (
              <li key={i} style={{ color: "var(--text)" }}>{f}</li>
            ))}
          </ul>
        </div>
      )}

      <button className="primary-button" onClick={onRestart} style={{ alignSelf: "flex-start" }}>
        ↺ Conduct Another Assessment
      </button>
    </div>
  );
}

// ─── Main Component ─────────────────────────────────────────────────────────

export default function InterviewPage() {
  const [step, setStep] = useState(0);
  const [roles, setRoles] = useState([]);
  const [setupData, setSetupData] = useState(null);
  const [questions, setQuestions] = useState(null);
  const [mcqAnswers, setMcqAnswers] = useState([]);
  const [theoryAnswers, setTheoryAnswers] = useState([]);
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/available-roles")
      .then((r) => setRoles(r.data.roles))
      .catch(() => setRoles(["Python Engineer", "AI Engineer", "Web Developer", "Data Scientist", "Full Stack Developer"]));
  }, []);

  const handleProfileDone = (data) => {
    setSetupData(data);
    setStep(1); // Proceed to Identity Verification
  };

  const handleVerifyDone = (data) => {
    setQuestions(data.questions);
    setStep(2); // Proceed to MCQ
  };

  const handleMcqDone = (answers) => {
    setMcqAnswers(answers);
    setStep(3); // Proceed to Theory
  };

  const handleTheoryDone = (answers) => {
    setTheoryAnswers(answers);
    setStep(4); // Proceed to Coding
  };

  const handleCodingDone = async (codingAnswers) => {
    setSubmitting(true);
    setError("");
    try {
      const res = await api.post("/evaluate-full-interview", {
        candidate_name: setupData.name,
        job_role: setupData.role,
        resume_text: setupData.resumeText || "",
        job_description: "",
        mcq_answers: mcqAnswers.map((a) => ({
          question_id: a.id,
          question: a.question,
          options: a.options,
          correct_index: a.correct_index,
          selected_index: a.selected_index,
        })),
        theory_answers: theoryAnswers.map((a) => ({
          question_id: a.id,
          question: a.question,
          expected_keywords: a.expected_keywords,
          answer: a.answer,
        })),
        coding_answers: codingAnswers.map((a) => ({
          question_id: a.id,
          question: a.question,
          function_name: a.function_name,
          test_cases: a.test_cases,
          code: a.code,
        })),
      });
      setResult(res.data);
      setStep(5); // Proceed to Results
    } catch (err) {
      setError(err.response?.data?.detail || "Evaluation failed. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleRestart = () => {
    setStep(0);
    setSetupData(null);
    setQuestions(null);
    setMcqAnswers([]);
    setTheoryAnswers([]);
    setResult(null);
    setError("");
  };

  return (
    <section>
      <div className="page-header">
        <p className="eyebrow">Assessment Gateway</p>
        <h2 className="page-title">Candidate Profile Check & AI Interview</h2>
        <p className="page-subtitle">
          Identity Verification · Biometric Proctoring · MCQ · Theory · Live Coding Evaluation
        </p>
      </div>

      <StepIndicator current={step} />

      {error && (
        <div className="alert danger" style={{ marginBottom: "1.5rem" }}>
          <span>⚠️</span> {error}
        </div>
      )}

      {submitting && (
        <div className="alert info" style={{ marginBottom: "1.5rem" }}>
          <span>⏳</span> Evaluating your interview responses, running code test cases, and computing scores…
        </div>
      )}

      {step === 0 && <ProfileCheckStep roles={roles} onNext={handleProfileDone} />}
      {step === 1 && setupData && (
        <IdentityVerificationStep
          setupData={setupData}
          onNext={handleVerifyDone}
          onBack={() => setStep(0)}
        />
      )}
      {step === 2 && questions && (
        <MCQStep
          questions={questions.mcq}
          onNext={handleMcqDone}
          onBack={() => setStep(1)}
        />
      )}
      {step === 3 && questions && (
        <TheoryStep
          questions={questions.theory}
          onNext={handleTheoryDone}
          onBack={() => setStep(2)}
        />
      )}
      {step === 4 && questions && (
        <CodingStep
          questions={questions.coding}
          onNext={handleCodingDone}
          onBack={() => setStep(3)}
        />
      )}
      {step === 5 && <ResultsStep result={result} onRestart={handleRestart} />}
    </section>
  );
}
