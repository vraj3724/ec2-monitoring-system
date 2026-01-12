import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

function formatTime(ts) {
  return new Date(ts * 1000).toLocaleTimeString();
}

// Custom tooltip (Grafana-like)
function CustomTooltip({ active, payload, label }) {
  if (!active || !payload || !payload.length) return null;

  return (
    <div style={{
      background: "#0b1220",
      padding: "8px 12px",
      borderRadius: 8,
      border: "1px solid #1f2933",
      color: "white",
      fontSize: 12
    }}>
      <div style={{ marginBottom: 4, color: "#9ca3af" }}>{label}</div>
      {payload.map((p) => (
        <div key={p.dataKey} style={{ color: p.stroke }}>
          {p.name}: {p.value.toFixed(1)}%
        </div>
      ))}
    </div>
  );
}

function CpuMemoryChart({ data }) {
  const chartData = data.map(m => ({
    time: formatTime(m.timestamp),
    cpu: m.cpu,
    memory: m.memory
  }));

  return (
    <div style={{
      background: "#161b22",
      padding: 20,
      borderRadius: 12,
      marginTop: 24
    }}>
      <div style={{
        fontSize: 14,
        color: "#9ca3af",
        marginBottom: 10
      }}>
        CPU & Memory Usage
      </div>

      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={chartData} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
          <CartesianGrid
            stroke="#1f2933"
            strokeDasharray="3 3"
          />

          <XAxis
            dataKey="time"
            tick={{ fill: "#9ca3af", fontSize: 11 }}
            tickLine={false}
            axisLine={false}
            minTickGap={30}
          />

          <YAxis
            domain={[0, 100]}
            tick={{ fill: "#9ca3af", fontSize: 11 }}
            tickLine={false}
            axisLine={false}
            width={40}
          />

          <Tooltip content={<CustomTooltip />} />

          <Line
            type="monotone"
            dataKey="cpu"
            name="CPU"
            stroke="#ef4444"
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
          />

          <Line
            type="monotone"
            dataKey="memory"
            name="Memory"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default CpuMemoryChart;
