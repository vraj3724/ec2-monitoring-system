from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import os

app = Flask(__name__)

# -------------------- STORAGE --------------------
METRICS = {}   # { service: [metric, ...] }
ALERTS = {}    # { service: [alert, ...] }

# -------------------- HEALTH --------------------
@app.route("/health")
def health():
    return {"status": "up"}

# -------------------- INGEST --------------------
@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "invalid payload"}), 400

    service = data.get("agent_id")
    raw_ts = data.get("timestamp")
    metrics = data.get("metrics", {})

    if not service or not raw_ts:
        return jsonify({"error": "missing agent_id or timestamp"}), 400

    # ISO timestamp → epoch seconds
    ts = int(datetime.fromisoformat(raw_ts.replace("Z", "+00:00")).timestamp())

    normalized = {
        "timestamp": ts,
        "cpu": metrics.get("cpu_percent", 0),
        "memory": metrics.get("memory_percent", 0),
        "disk": metrics.get("disk_percent", 0),
        "net_in": 0,
        "net_out": 0
    }

    METRICS.setdefault(service, []).append(normalized)

    # Simple alert rule
    if normalized["cpu"] > 80:
        ALERTS.setdefault(service, []).append({
            "timestamp": ts,
            "type": "CPU",
            "value": normalized["cpu"]
        })

    print(f"[INGEST] {service} cpu={normalized['cpu']}%", flush=True)

    return jsonify({"ok": True})

# -------------------- FRONTEND APIs --------------------
@app.route("/services")
def services():
    return jsonify(sorted(METRICS.keys()))

@app.route("/metrics/<service>")
def metrics(service):
    return jsonify(METRICS.get(service, []))

@app.route("/status/<service>")
def status(service):
    if service in METRICS and METRICS[service]:
        return jsonify({"status": "UP"})
    return jsonify({"status": "DOWN"})

@app.route("/alerts/<service>")
def alerts(service):
    return jsonify(ALERTS.get(service, []))

@app.route("/alerts/active/<service>")
def active_alerts(service):
    return jsonify({"count": len(ALERTS.get(service, []))})

# -------------------- SERVE REACT --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.join(BASE_DIR, "../frontend/dist")

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    file_path = os.path.join(FRONTEND_DIST, path)
    if path and os.path.exists(file_path):
        return send_from_directory(FRONTEND_DIST, path)
    return send_from_directory(FRONTEND_DIST, "index.html")

# -------------------- MAIN --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
