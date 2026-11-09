export default function ScoreCard({ label, value, accent = "blue" }) {
  return (
    <div className={`card score-card ${accent}`}>
      <p>{label}</p>
      <h3>{value}</h3>
    </div>
  );
}
