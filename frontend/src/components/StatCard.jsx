function StatCard({ title, value, unit, color }) {
  return (
    <div style={{
      background: "#161b22",
      padding: 20,
      borderRadius: 12,
      minWidth: 180,
      flex: 1
    }}>
      <div style={{ fontSize: 14, color: "#9ca3af" }}>{title}</div>
      <div style={{
        fontSize: 28,
        fontWeight: "bold",
        marginTop: 6,
        color
      }}>
        {value}{unit}
      </div>
    </div>
  );
}

export default StatCard;
