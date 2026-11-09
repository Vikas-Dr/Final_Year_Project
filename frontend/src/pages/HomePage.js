import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import {
  BrainCircuitIcon,
  DashboardIcon,
  FileTextIcon,
  InterviewIcon,
  ReportsIcon,
  ShieldCheckIcon,
  SparklesIcon,
} from "../components/Icons";

const WORKFLOW = [
  { icon: ShieldCheckIcon, title: "Verify", description: "Confirm candidate identity before the interview." },
  { icon: FileTextIcon, title: "Understand", description: "Compare a resume with the role requirements." },
  { icon: InterviewIcon, title: "Evaluate", description: "Run structured questions and review responses." },
  { icon: ReportsIcon, title: "Review", description: "Bring the results together in one report." },
];

const CAPABILITIES = [
  {
    icon: ShieldCheckIcon,
    tone: "blue",
    title: "Identity, handled first",
    description: "ID and live camera verification help establish who is taking the interview.",
  },
  {
    icon: FileTextIcon,
    tone: "teal",
    title: "A resume with context",
    description: "Extract skills and experience, then compare them with a job description.",
  },
  {
    icon: BrainCircuitIcon,
    tone: "purple",
    title: "Consistent interview review",
    description: "Role-based questions and response evaluation give recruiters a clearer view.",
  },
  {
    icon: ReportsIcon,
    tone: "gold",
    title: "Results you can use",
    description: "Review candidate performance in the dashboard and export a report as PDF.",
  },
];

export default function HomePage() {
  const { user } = useAuth();
  const primaryPath = user
    ? (user.role === "candidate" ? "/verification" : "/dashboard")
    : "/auth/candidate";

  return (
    <div className="landing-page">
      <section className="landing-hero">
        <div className="landing-hero-copy">
          <span className="landing-kicker"><span /> INTERVIEW & RESUME EVALUATION</span>
          <h1>
            See the person<br />
            behind the <span>answers.</span>
          </h1>
          <p className="landing-intro">
            A more considered hiring process, from identity verification and resume review
            to structured interviews and clear performance reports.
          </p>
          <div className="landing-actions">
            <Link className="landing-primary-action" to={primaryPath}>
              {user?.role === "recruiter" ? "Open recruiter dashboard" : user ? "Continue as candidate" : "Start as a candidate"}
              <span aria-hidden="true">↗</span>
            </Link>
            <Link className="landing-secondary-action" to={user ? "/resume-analysis" : "/auth/recruiter"}>
              {user ? <FileTextIcon size={17} /> : <DashboardIcon size={17} />}
              {user ? "Analyze a resume" : "Recruiter sign in"}
            </Link>
          </div>
          <div className="landing-trust-line">
            <span><ShieldCheckIcon size={15} /> Identity-first process</span>
            <span><SparklesIcon size={15} /> Local AI assistant</span>
          </div>
        </div>

        <div className="landing-review" aria-label="Example of a structured interview review">
          <div className="landing-review-topline">
            <span>SAMPLE INTERVIEW REVIEW</span>
            <span className="landing-review-state"><i /> EXAMPLE</span>
          </div>
          <div className="landing-candidate-row">
            <div className="landing-candidate-monogram">JD</div>
            <div>
              <strong>Example evaluation</strong>
              <span>Software engineering · Round 1</span>
            </div>
            <span className="landing-review-more" aria-hidden="true">···</span>
          </div>
          <div className="landing-score-block">
            <div>
              <span className="landing-score-label">SAMPLE SIGNAL</span>
              <strong>78<span>/100</span></strong>
            </div>
            <div className="landing-score-ring" aria-hidden="true"><span>78</span></div>
          </div>
          <div className="landing-score-rows">
            <div><span>Problem solving</span><i><b style={{ width: "82%" }} /></i><strong>82</strong></div>
            <div><span>Communication</span><i><b style={{ width: "74%" }} /></i><strong>74</strong></div>
            <div><span>Role alignment</span><i><b style={{ width: "78%" }} /></i><strong>78</strong></div>
          </div>
          <div className="landing-review-foot">
            <span><BrainCircuitIcon size={15} /> Structured evaluation</span>
            <span>EXAMPLE REVIEW SUMMARY</span>
          </div>
          <div className="landing-review-orbit orbit-one" />
          <div className="landing-review-orbit orbit-two" />
        </div>

        <div className="landing-hero-index" aria-hidden="true">PEOPLE / POTENTIAL / PROGRESS</div>
      </section>

      <section className="landing-process" aria-label="Hiring workflow">
        <div className="landing-section-heading">
          <span>ONE CONNECTED WORKFLOW</span>
          <p>From first check to final review</p>
        </div>
        <div className="landing-workflow">
          {WORKFLOW.map(({ icon: Icon, title, description }, index) => (
            <div className="landing-workflow-item" key={title}>
              <div className="landing-workflow-marker">
                <span>{String(index + 1).padStart(2, "0")}</span>
                <Icon size={18} />
              </div>
              <div><strong>{title}</strong><p>{description}</p></div>
            </div>
          ))}
        </div>
      </section>

      <section className="landing-capabilities">
        <div className="landing-capabilities-heading">
          <div>
            <span className="landing-kicker"><span /> BUILT FOR BOTH SIDES</span>
            <h2>A fairer process.<br /><span>A fuller picture.</span></h2>
          </div>
          <p>Less jumping between tools. More useful context for candidates and recruiters at each step.</p>
        </div>
        <div className="landing-capability-grid">
          {CAPABILITIES.map(({ icon: Icon, tone, title, description }) => (
            <article className="landing-capability-card" key={title}>
              <div className={`landing-capability-icon ${tone}`}><Icon size={20} /></div>
              <h3>{title}</h3>
              <p>{description}</p>
            </article>
          ))}
        </div>
        <div className="landing-bottom-cta">
          <div>
            <span>NEED A HAND GETTING READY?</span>
            <strong>Your AI career assistant is one tab away.</strong>
          </div>
          <Link to="/ai-assistant">Talk to the assistant <span aria-hidden="true">↗</span></Link>
        </div>
      </section>
    </div>
  );
}
