import { useRef, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import ScoreRing from "../components/ScoreRing";
import ProgressBar from "../components/ProgressBar";

const SAMPLE_RESUME = `Vikramaditya Singh
Email: vikram.singh@example.com | Phone: +91 98765-43210
Location: Bengaluru, India | LinkedIn: linkedin.com/in/vikram-singh | GitHub: github.com/vikram

PROFESSIONAL SUMMARY
Passionate Full Stack Developer and AI enthusiast with 3+ years experience building scalable web applications, RESTful microservices, and machine learning pipelines.

TECHNICAL SKILLS
- Languages: Python, Java, JavaScript, TypeScript, C++, SQL, Bash
- Frameworks & Web: React.js, Next.js, Node.js, Express.js, FastAPI, Flask, Django, Tailwind CSS, HTML5, CSS3
- Databases & Cloud: PostgreSQL, MySQL, MongoDB, Redis, Docker, Kubernetes, AWS, Git, CI/CD
- AI / ML: PyTorch, TensorFlow, Scikit-Learn, Pandas, NumPy, NLP, Large Language Models (LLM), LangChain

EDUCATION
B.Tech in Computer Science and Engineering — National Institute of Technology, 2024 (CGPA: 8.9 / 10)

EXPERIENCE
Software Engineering Intern — TechCorp Solutions (6 months)
- Developed automated resume parsing microservices using FastAPI and NLP algorithms.
- Built interactive candidate dashboards and real-time evaluation portals in React.
- Improved database query performance by 35% on PostgreSQL instances.

PROJECTS
1. AI Interview & Resume Intelligence Platform: Full-stack hiring system with automated coding execution, NLP scoring, and identity verification.
2. Smart ATS Resume Matcher: Semantic keyword matching engine with TF-IDF and LLM evaluation.

CERTIFICATIONS
- AWS Certified Solutions Architect Associate
- Deep Learning Specialization — DeepLearning.AI (Coursera)`;

const SAMPLE_JD = `Looking for a skilled Full Stack / Python Developer with hands-on experience in FastAPI, React.js, PostgreSQL, Docker, and RESTful APIs. Experience with Machine Learning, NLP, and cloud deployments on AWS is a strong plus. Good communication skills, structured problem solving, and project experience required.`;

export default function ResumeAnalysisPage() {
  const fileInputRef = useRef(null);
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [fileName, setFileName] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [analysisStage, setAnalysisStage] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const [documentStats, setDocumentStats] = useState(null);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const handleAnalyze = async () => {
    if (!resumeText.trim()) {
      setError("Please upload a resume file or paste resume text to analyze.");
      return;
    }
    setError("");
    setSuccessMsg("");
    setAnalysis(null);
    setAnalysisStage("Analyzing resume text");
    setLoading(true);
    try {
      const res = await api.post("/analyze-resume", {
        resume_text: resumeText,
        job_description: jobDescription,
      });
      setAnalysis(res.data);
      setSuccessMsg(`Analysis complete! Analyzed ${res.data.skills?.length || 0} skills via ${res.data.ai_provider || "AI Engine"}.`);
    } catch (err) {
      setError(err.response?.data?.detail || "Analysis failed. Please check backend connection.");
    } finally {
      setLoading(false);
      setAnalysisStage("");
    }
  };

  const processFile = async (file) => {
    if (!file) return;
    const extension = file.name.split(".").pop()?.toLowerCase();
    if (!["pdf", "docx", "doc", "txt"].includes(extension)) {
      setError("Choose a PDF, DOCX, DOC, or TXT resume.");
      return;
    }

    setFileName(file.name);
    setError("");
    setSuccessMsg("");
    setAnalysis(null);
    setResumeText("");
    setDocumentStats(null);
    setUploadProgress(0);
    setAnalysisStage("Uploading file");
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    if (jobDescription.trim()) {
      formData.append("job_description", jobDescription);
    }

    try {
      const res = await api.post("/upload-resume", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (event) => {
          if (event.total) {
            const progress = Math.round((event.loaded / event.total) * 100);
            setUploadProgress(progress);
            if (progress >= 100) setAnalysisStage("Reading and analyzing resume");
          }
        },
      });

      const extracted = res.data.extracted_text || "";
      setResumeText(extracted);
      setDocumentStats({
        size: file.size,
        characters: extracted.length,
        type: extension.toUpperCase(),
      });

      if (!extracted || extracted.trim().length < 20) {
        setAnalysis(null);
        setError("The file was received, but we couldn’t find enough selectable text to analyze. If this is a scanned PDF, upload a searchable PDF or paste its text below.");
      } else {
        setAnalysis({
          ...res.data.analysis,
          report_id: res.data.report_id,
          mongo_profile_status: res.data.mongo_profile_status,
          mongo_profile_id: res.data.mongo_profile_id,
          mongo_profile_message: res.data.mongo_profile_message,
        });
        setSuccessMsg(`Analysis complete. We extracted ${extracted.length.toLocaleString()} characters from ${file.name}.`);
      }
    } catch (err) {
      setAnalysis(null);
      setError(err.response?.data?.detail || "We couldn’t read this document. Check that it is a valid PDF, DOCX, DOC, or TXT file, then try again.");
    } finally {
      setLoading(false);
      setAnalysisStage("");
      setUploadProgress(0);
    }
  };

  const handleUpload = (e) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    processFile(file);
  };

  const handleFileDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);
    processFile(event.dataTransfer.files?.[0]);
  };

  const handleLoadSample = () => {
    setResumeText(SAMPLE_RESUME);
    setJobDescription(SAMPLE_JD);
    setFileName("sample_candidate_resume.pdf");
    setAnalysis(null);
    setDocumentStats(null);
    setError("");
    setSuccessMsg("Sample resume and job description loaded. Run analysis when you’re ready.");
  };

  const handleClear = () => {
    setResumeText("");
    setJobDescription("");
    setAnalysis(null);
    setFileName("");
    setDocumentStats(null);
    setAnalysisStage("");
    setUploadProgress(0);
    setError("");
    setSuccessMsg("");
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const sectionIcons = {
    education: "🎓",
    experience: "💼",
    projects: "🛠️",
    certifications: "📜",
    skills: "⚡",
  };

  return (
    <section>
      <div className="page-header">
        <p className="eyebrow">Module 1</p>
        <h2 className="page-title">Resume Analysis</h2>
        <p className="page-subtitle">
          A consistent 100-point resume rubric, evidence-based role matching, and specific improvement guidance.
        </p>
      </div>

      <div className="resume-analysis-layout">
        {/* ── Input Panel ── */}
        <div className="card resume-input-card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
            <div className="section-title" style={{ margin: 0 }}>📤 Upload or Paste Resume</div>
            <div style={{ display: "flex", gap: "0.5rem" }}>
              <button
                type="button"
                onClick={handleLoadSample}
                className="secondary-button"
                disabled={loading}
                style={{ fontSize: "0.8rem", padding: "0.35rem 0.75rem" }}
              >
                📋 Load Sample
              </button>
              <button
                type="button"
                onClick={handleClear}
                className="secondary-button"
                disabled={loading}
                style={{ fontSize: "0.8rem", padding: "0.35rem 0.75rem", borderColor: "rgba(239,68,68,0.4)" }}
              >
                🗑️ Clear
              </button>
            </div>
          </div>

          <div className="form-group">
            <span className="field-label">Resume document</span>
            <div
              className={`resume-dropzone ${isDragging ? "is-dragging" : ""} ${fileName ? "has-document" : ""}`}
              onDragOver={(event) => { event.preventDefault(); setIsDragging(true); }}
              onDragLeave={(event) => { if (!event.currentTarget.contains(event.relatedTarget)) setIsDragging(false); }}
              onDrop={handleFileDrop}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.docx,.doc,.txt,application/pdf"
                onChange={handleUpload}
                id="resume-file-input"
                className="resume-file-input"
                disabled={loading}
              />
              <span className="resume-file-glyph" aria-hidden="true">{fileName ? "✓" : "PDF"}</span>
              <div className="resume-drop-copy">
                <strong>{fileName || "Drop your resume here"}</strong>
                <span>{fileName ? `${documentStats?.type || "Document"}${documentStats?.size ? ` · ${(documentStats.size / (1024 * 1024)).toFixed(2)} MB` : ""}` : "PDF, DOCX or TXT · Choose a file or drag it here"}</span>
              </div>
              <button
                type="button"
                className="resume-browse-button"
                onClick={() => fileInputRef.current?.click()}
                disabled={loading}
              >
                {fileName ? "Replace" : "Browse"}
              </button>
            </div>
            {documentStats && (
              <div className="resume-document-meta">
                <span><strong>{documentStats.characters.toLocaleString()}</strong> characters extracted</span>
                <span>{documentStats.type} · ready</span>
              </div>
            )}
          </div>

          <details className="resume-advanced-fields">
            <summary>
              <span>Review extracted text or add a job description</span>
              <span aria-hidden="true">＋</span>
            </summary>
            <div className="form-group">
              <label className="field-label">
                Resume text{" "}
                {resumeText && <span style={{ color: "var(--text-muted)", fontSize: "0.8rem" }}>({resumeText.length.toLocaleString()} characters)</span>}
              </label>
              <textarea
                rows={9}
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
                placeholder="Upload a document to extract text automatically, or paste resume text here..."
              />
            </div>

            <div className="form-group">
              <label className="field-label">Target job description <span className="resume-optional-label">Optional</span></label>
              <textarea
                rows={5}
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Add a job description to see how closely this resume matches the role..."
              />
            </div>
          </details>

          <details className="resume-advanced-fields resume-rubric-overview">
            <summary>
              <span>How the scores work</span>
              <span aria-hidden="true">＋</span>
            </summary>
            <div className="resume-rubric-intro">
              Resume completeness is scored from the extracted document, not from an AI-generated mark:
              sections (25), distinct skills (20), contact details (10), career evidence (15),
              measurable impact (10), projects (10), length (5), and readable bullets (5).
              A job-fit score is separate: 80% required-skill coverage and 20% relevant job-description
              keyword coverage. Without a job description, job fit is not scored.
            </div>
          </details>

          <div className="resume-storage-info">
            Uploaded files and reports are saved for later review. Pasted resume text is analyzed
            but is not saved as an uploaded resume.
          </div>

          {error && <p className="error-text resume-message" role="alert">⚠️ {error}</p>}
          {successMsg && <p className="helper-text" style={{ color: "#10b981", fontWeight: 500, marginBottom: "1rem" }}>✅ {successMsg}</p>}

          <button
            className="primary-button"
            onClick={handleAnalyze}
            disabled={loading}
            id="analyze-resume-btn"
            style={{ width: "100%", padding: "0.85rem", fontSize: "1rem" }}
          >
            {loading ? "Analysing…" : fileName ? "Re-analyze resume" : "Analyze pasted resume"}
          </button>
        </div>

        {/* ── Output Panel ── */}
        <div className="card resume-results-card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
            <div className="section-title" style={{ margin: 0 }}>📊 Live Analysis Output</div>
            {analysis && (
              <span className="tag blue" style={{ fontSize: "0.75rem", padding: "0.2rem 0.6rem" }}>
                Scores: fixed rubric
              </span>
            )}
          </div>

          {!analysis && !loading && (
            <div className="alert info" style={{ marginTop: "1rem" }}>
              <span>💡</span>
              <div>
                <strong>Ready for Analysis</strong>
                <p style={{ margin: "0.3rem 0 0 0", fontSize: "0.88rem" }}>
                  Upload your resume PDF/DOCX or click <strong>Load Sample</strong> to inspect skill detection, section breakdown, rubric score, and improvement feedback.
                </p>
              </div>
            </div>
          )}

          {loading && (
            <div className="resume-analysis-progress" role="status">
              <div className="resume-progress-document" aria-hidden="true"><span>PDF</span><i /></div>
              <div className="resume-progress-copy">
                <strong>{analysisStage || "Preparing your resume"}</strong>
                <span>{analysisStage === "Uploading file" ? `Sending your file${uploadProgress ? ` · ${uploadProgress}%` : ""}` : "Finding sections, skills and role alignment"}</span>
              </div>
              <div className={`resume-progress-track ${analysisStage !== "Uploading file" ? "is-indeterminate" : ""}`}>
                <span style={analysisStage === "Uploading file" ? { width: `${uploadProgress}%` } : undefined} />
              </div>
              <div className="resume-progress-steps">
                <span className={analysisStage === "Uploading file" ? "is-active" : "is-done"}>Receive file</span>
                <span className={analysisStage === "Uploading file" ? "" : "is-active"}>Read &amp; analyze</span>
              </div>
            </div>
          )}

          {analysis && (
            <div className="resume-analysis-report" key={`${fileName}-${analysis.candidate_name || "resume"}`}>
              {/* Candidate Info Card */}
              <div className="resume-candidate-summary">
                <div className="resume-candidate-avatar">
                  {analysis.candidate_name?.[0] || "👤"}
                </div>
                <div className="resume-candidate-copy">
                  <strong>{analysis.candidate_name}</strong>
                  <p>
                    {analysis.email && <span>{analysis.email}</span>}
                    {analysis.email && analysis.phone && <span aria-hidden="true"> · </span>}
                    {analysis.phone && <span>{analysis.phone}</span>}
                  </p>
                </div>
                {documentStats && <span className="resume-report-source">{documentStats.type} analyzed</span>}
              </div>

              {/* Score Rings */}
              <div className="resume-score-pair">
                <ScoreRing score={analysis.resume_score} size={90} color="#3b82f6" label="Resume Completeness" />
                {analysis.job_match_available === false ? (
                  <div className="resume-match-unavailable">
                    <span>ROLE MATCH</span>
                    <strong>Add a job description</strong>
                    <p>We need target-role requirements to calculate a meaningful fit score.</p>
                  </div>
                ) : (
                  <ScoreRing score={analysis.job_match_score} size={90} color="#10b981" label="Job Fit Match" />
                )}
              </div>

              {/* Progress Bars */}
              <ProgressBar label="Resume Completeness" value={analysis.resume_score} color="blue" />
              {analysis.job_match_available !== false && (
                <ProgressBar label="Target Role Alignment" value={analysis.job_match_score} color="green" />
              )}

              {analysis.resume_score_breakdown?.criteria && (
                <details className="resume-score-breakdown">
                  <summary>See how the resume score was calculated</summary>
                  <div className="resume-score-criteria">
                    {analysis.resume_score_breakdown.criteria.map((criterion) => (
                      <div className="resume-score-criterion" key={criterion.key}>
                        <div>
                          <strong>{criterion.name}</strong>
                          <span>{criterion.score} / {criterion.max_score}</span>
                        </div>
                        <p>{criterion.guideline}</p>
                      </div>
                    ))}
                  </div>
                </details>
              )}

              {analysis.job_match_available && (
                <div className="resume-role-match-detail">
                  <strong>Role match evidence</strong>
                  <p>{analysis.job_match_breakdown?.guideline}</p>
                  <p><b>Keyword coverage:</b> {analysis.job_match_breakdown?.keyword_coverage ?? 0}%</p>
                  {analysis.matched_skills?.length > 0 && (
                    <p><b>Matched skills:</b> {analysis.matched_skills.join(", ")}</p>
                  )}
                  {analysis.missing_skills?.length > 0 && (
                    <p><b>Not found in this resume:</b> {analysis.missing_skills.join(", ")}</p>
                  )}
                </div>
              )}

              <div className="section-divider" style={{ margin: "1rem 0" }} />

              {/* Executive Summary */}
              {analysis.summary && (
                <div style={{ marginBottom: "1.2rem", padding: "0.85rem", background: "rgba(59, 130, 246, 0.08)", borderRadius: "8px", borderLeft: "3px solid #3b82f6" }}>
                  <strong style={{ fontSize: "0.85rem", color: "#60a5fa", display: "block", marginBottom: "0.3rem" }}>
                    🤖 AI Executive Summary
                  </strong>
                  <p style={{ margin: 0, fontSize: "0.85rem", lineHeight: 1.5, color: "var(--text)" }}>
                    {analysis.summary}
                  </p>
                </div>
              )}

              {/* Section Detection */}
              <div className="section-title resume-result-heading">Core sections</div>
              <div className="tag-row resume-section-tags">
                {Object.entries(analysis.sections || {}).map(([section, found]) => (
                  <span
                    key={section}
                    className={`tag ${found ? "green" : "red"}`}
                    style={{ fontSize: "0.8rem", padding: "0.3rem 0.6rem" }}
                  >
                    {sectionIcons[section] || "📄"} {section.charAt(0).toUpperCase() + section.slice(1)} {found ? "✓" : "✗"}
                  </span>
                ))}
              </div>

              {/* Skills */}
              <div className="section-title resume-result-heading">
                Skills detected <span>{analysis.skills?.length || 0}</span>
              </div>
              <div className="tag-row resume-skill-tags">
                {analysis.skills && analysis.skills.length > 0 ? (
                  analysis.skills.map((skill) => (
                    <span key={skill} className="tag" style={{ background: "rgba(59, 130, 246, 0.15)", borderColor: "rgba(59, 130, 246, 0.4)", color: "#93c5fd" }}>
                      {skill}
                    </span>
                  ))
                ) : (
                  <span style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>No matching skills detected.</span>
                )}
              </div>

              <div className="section-divider" style={{ margin: "1rem 0" }} />

              {/* Strengths */}
              <div className="section-title resume-result-heading">Profile strengths</div>
              <ul className="plain-list resume-strength-list">
                {analysis.strengths && analysis.strengths.length > 0 ? (
                  analysis.strengths.map((s, i) => (
                    <li key={i} style={{ color: "#34d399", fontWeight: 500, fontSize: "0.85rem", marginBottom: "0.35rem" }}>
                      ✓ {s}
                    </li>
                  ))
                ) : (
                  <li style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>No notable strengths calculated.</li>
                )}
              </ul>

              {/* Improvements */}
              {analysis.improvements && analysis.improvements.length > 0 && (
                <>
                  <div className="section-title resume-result-heading">Ways to improve</div>
                  <ul className="plain-list resume-improvement-list">
                    {analysis.improvements.map((item, i) => (
                      <li key={i} style={{ fontSize: "0.85rem", color: "#fbbf24", marginBottom: "0.35rem" }}>
                        → {item}
                      </li>
                    ))}
                  </ul>
                </>
              )}

              {analysis.report_id && (
                <div className="resume-persistence-note" role="status">
                  <div>
                    <strong>Uploaded analysis saved · Report #{analysis.report_id}</strong>
                    <p>
                      SQL report: saved. MongoDB candidate profile:{" "}
                      {analysis.mongo_profile_status === "saved"
                        ? `saved${analysis.mongo_profile_id ? ` · ${analysis.mongo_profile_id}` : ""}`
                        : `not saved${analysis.mongo_profile_message ? ` · ${analysis.mongo_profile_message}` : ""}`}
                    </p>
                  </div>
                  <Link to="/reports">View saved reports <span aria-hidden="true">→</span></Link>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
