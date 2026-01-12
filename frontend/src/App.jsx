import { useEffect, useState, useMemo } from "react";
import {
  getServices,
  getMetrics,
  getStatus,
  getAlerts,
  getActiveAlerts,
} from "./api";

import GaugeCard from "./components/GaugeCard";
import TimeSeriesChart from "./components/TimeSeriesChart";

const TIME_RANGES = [
  { label: "5m", value: 300 },
  { label: "15m", value: 900 },
  { label: "1h", value: 3600 },
  { label: "6h", value: 21600 },
];

function App() {
  const [services, setServices] = useState([]);
  const [selectedService, setSelectedService] = useState("");

  const [metrics, setMetrics] = useState([]);
  const [status, setStatus] = useState("UNKNOWN");
  const [alerts, setAlerts] = useState([]);
  const [activeAlerts, setActiveAlerts] = useState(0);

  const [timeRange, setTimeRange] = useState(300);

  /* ---------------- Load services ---------------- */
  useEffect(() => {
    getServices().then((s) => {
      setServices(s);
      if (s.length > 0) setSelectedService(s[0]);
    });
  }, []);

  /* ---------------- Poll data every 5s ---------------- */
  useEffect(() => {
    if (!selectedService) return;

    const load = () => {
      getMetrics(selectedService).then(setMetrics);
      getStatus(selectedService).then((r) => setStatus(r.status));
      getActiveAlerts(selectedService).then((r) => setActiveAlerts(r.count));
      getAlerts(selectedService).then(setAlerts);
    };

    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, [selectedService]);

  /* ---------------- Time filtering ---------------- */
  const nowTs = Math.floor(new Date().getTime() / 1000);

  const filteredMetrics = useMemo(() => {
    return metrics.filter((m) => m.timestamp >= nowTs - timeRange);
  }, [metrics, timeRange, nowTs]);

  const latest =
    filteredMetrics.length > 0
      ? filteredMetrics[filteredMetrics.length - 1]
      : null;

  return (
    <div
      style={{
        background: "#0e1117",
        minHeight: "100vh",
        color: "#e5e7eb",
        padding: 24,
        fontFamily: "Inter, system-ui, sans-serif",
      }}
    >
      {/* ---------------- HEADER ---------------- */}
      <h1 style={{ fontSize: 22, marginBottom: 12 }}>
        Monitoring Dashboard
      </h1>

      {/* ---------------- TOP CONTROL BAR ---------------- */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 16,
          marginBottom: 24,
          flexWrap: "wrap",
        }}
      >
        {/* LEFT: Service + Status + Alerts */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 12,
            flexWrap: "wrap",
          }}
        >
          {/* Service selector */}
          <select
            value={selectedService}
            onChange={(e) => setSelectedService(e.target.value)}
            style={{
              background: "#161b22",
              color: "white",
              border: "1px solid #2a2f3a",
              borderRadius: 6,
              padding: "6px 10px",
            }}
          >
            {services.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>

          {/* Status */}
          <span
            style={{
              background: status === "UP" ? "#22c55e" : "#ef4444",
              color: "black",
              padding: "4px 10px",
              borderRadius: 6,
              fontWeight: 600,
            }}
          >
            {status}
          </span>

          {/* Alerts */}
          <span
            style={{
              background: activeAlerts > 0 ? "#ef4444" : "#374151",
              color: "white",
              padding: "4px 10px",
              borderRadius: 6,
              fontWeight: 600,
            }}
          >
            Alerts: {activeAlerts}
          </span>
        </div>

        {/* RIGHT: Time range selector */}
        <div
          style={{
            display: "inline-flex",
            background: "#161b22",
            borderRadius: 8,
            padding: 4,
            gap: 4,
          }}
        >
          {TIME_RANGES.map((r) => (
            <button
              key={r.value}
              onClick={() => setTimeRange(r.value)}
              style={{
                background:
                  timeRange === r.value ? "#2563eb" : "transparent",
                color: timeRange === r.value ? "white" : "#9ca3af",
                border: "none",
                borderRadius: 6,
                padding: "6px 12px",
                cursor: "pointer",
              }}
            >
              {r.label}
            </button>
          ))}
        </div>
      </div>

      {/* ---------------- GAUGES ---------------- */}
      {latest && (
        <div
          style={{
            display: "flex",
            gap: 16,
            flexWrap: "wrap",
            marginBottom: 20,
          }}
        >
          <GaugeCard title="CPU Usage" value={latest.cpu ?? 0} unit="%" />
          <GaugeCard title="Memory Usage" value={latest.memory ?? 0} unit="%" />
          <GaugeCard title="Disk Usage" value={latest.disk ?? 0} unit="%" />
        </div>
      )}

      {/* ---------------- GRAPHS ---------------- */}
      {filteredMetrics.length > 0 && (
        <>
          {/* CPU & Memory */}
          <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
            <TimeSeriesChart
              title="CPU Usage"
              dataKey="cpu"
              color="#ef4444"
              unit="%"
              data={filteredMetrics}
            />
            <TimeSeriesChart
              title="Memory Usage"
              dataKey="memory"
              color="#3b82f6"
              unit="%"
              data={filteredMetrics}
            />
          </div>

          {/* Network */}
          <div
            style={{
              display: "flex",
              gap: 16,
              flexWrap: "wrap",
              marginTop: 20,
            }}
          >
            <TimeSeriesChart
              title="Network IN"
              dataKey="net_in"
              color="#22c55e"
              unit=" KB"
              data={filteredMetrics.map((m) => ({
                ...m,
                net_in: m.net_in / 1024,
              }))}
            />
            <TimeSeriesChart
              title="Network OUT"
              dataKey="net_out"
              color="#a855f7"
              unit=" KB"
              data={filteredMetrics.map((m) => ({
                ...m,
                net_out: m.net_out / 1024,
              }))}
            />
          </div>
        </>
      )}

      {/* ---------------- ALERT HISTORY ---------------- */}
      {alerts.length > 0 && (
        <div
          style={{
            background: "#161b22",
            borderRadius: 12,
            padding: 16,
            marginTop: 30,
          }}
        >
          <h3 style={{ marginBottom: 12 }}>Alert History</h3>

          {alerts
            .slice(-10)
            .reverse()
            .map((a, i) => (
              <div
                key={i}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  padding: "6px 0",
                  borderBottom: "1px solid #2a2f3a",
                  color: "#fca5a5",
                }}
              >
                <span>
                  {new Date(a.timestamp * 1000).toLocaleString()}
                </span>
                <span>{a.type}</span>
                <span>{a.value.toFixed(1)}%</span>
              </div>
            ))}
        </div>
      )}
    </div>
  );
}

export default App;
