import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

function getColor(value) {
  if (value < 60) return "#22c55e";   // green
  if (value < 80) return "#facc15";   // yellow
  return "#ef4444";                   // red
}

function GaugeCard({ title, value, unit }) {
  const data = [
    { name: "value", value },
    { name: "rest", value: 100 - value }
  ];

  const color = getColor(value);

  return (
    <div style={{
      background: "#161b22",
      padding: 20,
      borderRadius: 12,
      minWidth: 200,
      flex: 1,
      textAlign: "center"
    }}>
      <div style={{ color: "#9ca3af", marginBottom: 10 }}>{title}</div>

      <ResponsiveContainer width="100%" height={160}>
        <PieChart>
          <Pie
            data={data}
            startAngle={180}
            endAngle={0}
            innerRadius={60}
            outerRadius={80}
            dataKey="value"
          >
            <Cell fill={color} />
            <Cell fill="#2a2f3a" />
          </Pie>
        </PieChart>
      </ResponsiveContainer>

      <div style={{
        marginTop: -90,
        fontSize: 24,
        fontWeight: "bold",
        color
      }}>
        {Number(value).toFixed(1)}{unit}
      </div>
    </div>
  );
}

export default GaugeCard;
