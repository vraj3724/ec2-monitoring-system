import time
import psutil
import requests
from datetime import datetime, timezone

from config import (
    INGEST_URL,
    AGENT_ID,
    AGENT_TOKEN,
    INTERVAL_SECONDS,
    REQUEST_TIMEOUT,
)

# -------------------- NETWORK STATE --------------------
_prev_net = psutil.net_io_counters()
_prev_time = time.time()


def collect_metrics():
    global _prev_net, _prev_time

    # ---------- CPU ----------
    cpu_percent = psutil.cpu_percent(interval=1)
    load_avg_1m = psutil.getloadavg()[0]
    uptime_seconds = int(time.time() - psutil.boot_time())

    # ---------- MEMORY ----------
    mem = psutil.virtual_memory()

    # ---------- DISK ----------
    disk = psutil.disk_usage("/")

    # ---------- NETWORK ----------
    now = time.time()
    net = psutil.net_io_counters()

    interval = max(now - _prev_time, 1)

    net_in_bps = (net.bytes_recv - _prev_net.bytes_recv) / interval
    net_out_bps = (net.bytes_sent - _prev_net.bytes_sent) / interval

    _prev_net = net
    _prev_time = now

    return {
        # CPU
        "cpu_percent": round(cpu_percent, 2),
        "load_avg_1m": round(load_avg_1m, 2),
        "uptime_seconds": uptime_seconds,

        # Memory
        "memory_total_mb": round(mem.total / (1024 * 1024), 2),
        "memory_used_mb": round(mem.used / (1024 * 1024), 2),
        "memory_percent": round(mem.percent, 2),

        # Disk
        "disk_total_gb": round(disk.total / (1024 ** 3), 2),
        "disk_used_gb": round(disk.used / (1024 ** 3), 2),
        "disk_percent": round(disk.percent, 2),

        # Network (bytes per second)
        "network_in_bytes_per_sec": round(net_in_bps, 2),
        "network_out_bytes_per_sec": round(net_out_bps, 2),
    }


def build_payload(metrics):
    return {
        "agent_id": AGENT_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "interval_seconds": INTERVAL_SECONDS,
        "metrics": metrics,
    }


def send_payload(payload):
    headers = {
        "Authorization": f"Bearer {AGENT_TOKEN}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        INGEST_URL,
        json=payload,
        headers=headers,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()


def run():
    print(f"[AGENT] Monitoring agent started ({AGENT_ID})", flush=True)

    while True:
        try:
            metrics = collect_metrics()
            payload = build_payload(metrics)
            send_payload(payload)
            print("[AGENT] Metrics sent", flush=True)
        except Exception as e:
            print("[AGENT] Error:", e, flush=True)

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
