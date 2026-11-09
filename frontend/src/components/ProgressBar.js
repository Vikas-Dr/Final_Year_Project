export default function ProgressBar({ label, value, color = "blue" }) {
  const pct = Math.min(Math.max(value || 0, 0), 100);
  return (
    <div className="progress-bar-wrap">
      <div className="progress-bar-label-row">
        <span>{label}</span>
        <span style={{ color: pct >= 70 ? "#34d399" : pct >= 50 ? "#fbbf24" : "#fc8181", fontWeight: 700 }}>{pct}%</span>
      </div>
      <div className="progress-bar-track">
        <div className={`progress-bar-fill ${color}`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}
