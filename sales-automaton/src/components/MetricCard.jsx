export default function MetricCard({ title, value }) {
  return (
    <div style={{ border: "1px solid #ddd", padding: 20 }}>
      <h4>{title}</h4>
      <h2>{value}</h2>
    </div>
  );
}
