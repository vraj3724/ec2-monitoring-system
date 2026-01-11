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


def collect_metrics():
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "load_avg_1m": psutil.getloadavg()[0],
        "uptime_seconds": int(time.time() - psutil.boot_time()),
        "memory_total_mb": round(mem.total / (1024 * 1024), 2),
        "memory_used_mb": round(mem.used / (1024 * 1024), 2),
        "memory_percent": mem.percent,
        "disk_total_gb": round(disk.total / (1024 ** 3), 2),
        "disk_used_gb": round(disk.used / (1024 ** 3), 2),
        "disk_percent": disk.percent,
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
    print("Monitoring agent started")
    while True:
        try:
            metrics = collect_metrics()
            payload = build_payload(metrics)
            send_payload(payload)
            print("Metrics sent")
        except Exception as e:
            print("Error:", e)

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
