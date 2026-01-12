
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

function CustomTooltip({ active, payload, label, unit }) {
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
      <div style={{ color: payload[0].stroke }}>
        {payload[0].name}: {payload[0].value.toFixed(1)}{unit}
      </div>
    </div>
  );
}

function TimeSeriesChart({ title, dataKey, color, unit, data }) {
  const chartData = data.map(m => ({
    time: formatTime(m.timestamp),
    value: m[dataKey]
  }));

  return (
    <div style={{
      background: "#161b22",
      padding: 16,
      borderRadius: 12,
      flex: 1
    }}>
      <div style={{
        fontSize: 14,
        color: "#9ca3af",
        marginBottom: 8
      }}>
        {title}
      </div>

      <ResponsiveContainer width="100%" height={260}>
        <LineChart data={chartData}>
          <CartesianGrid stroke="#1f2933" strokeDasharray="3 3" />

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

          <Tooltip content={<CustomTooltip unit={unit} />} />

          <Line
            type="monotone"
            dataKey="value"
            name={title}
            stroke={color}
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default TimeSeriesChart;
