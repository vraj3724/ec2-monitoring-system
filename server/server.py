from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import os
import json

app = Flask(__name__)

# -------------------- STORAGE --------------------
METRICS = {}          # { service: [metric, ...] }
ALERTS = {}           # { service: [alert, ...] }

# Persist known services so they don’t disappear
SERVICES_FILE = "/tmp/services.json"

def load_services():
    if os.path.exists(SERVICES_FILE):
        with open(SERVICES_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_services():
    with open(SERVICES_FILE, "w") as f:
        json.dump(sorted(SERVICES), f)

SERVICES = load_services()

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

    # Register service permanently
    if service not in SERVICES:
        SERVICES.add(service)
        save_services()

    # ISO timestamp → epoch seconds
    ts = int(datetime.fromisoformat(raw_ts.replace("Z", "+00:00")).timestamp())

    normalized = {
        "timestamp": ts,
        "cpu": metrics.get("cpu_percent", 0),
        "memory": metrics.get("memory_percent", 0),
        "disk": metrics.get("disk_percent", 0),

        # ✅ NETWORK (from agent)
        "net_in": metrics.get("network_in_bytes_per_sec", 0),
        "net_out": metrics.get("network_out_bytes_per_sec", 0),
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
    return jsonify(sorted(SERVICES))

@app.route("/metrics/<service>")
def metrics(service):
    return jsonify(METRICS.get(service, []))

@app.route("/status/<service>")
def status(service):
    data = METRICS.get(service, [])
    if not data:
        return jsonify({"status": "DOWN"})

    last_ts = data[-1]["timestamp"]
    now = int(datetime.utcnow().timestamp())

    # If no data in last 15 seconds → DOWN
    if now - last_ts > 15:
        return jsonify({"status": "DOWN"})

    return jsonify({"status": "UP"})

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
