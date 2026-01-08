import psutil
import time
import json
from datetime import datetime

LOG_FILE = "metrics.log"

def collect_metrics():
    try:
        with open(LOG_FILE, "a") as logfile:
            while True:
                data = {}

                # CPU
                data["cpu_percent"] = psutil.cpu_percent(interval=1)
                data["load_avg_1m"] = psutil.getloadavg()[0]
                data["uptime_seconds"] = int(time.time() - psutil.boot_time())

                # Memory
                mem = psutil.virtual_memory()
                data["memory_total_mb"] = round(mem.total / (1024 * 1024), 2)
                data["memory_used_mb"] = round(mem.used / (1024 * 1024), 2)
                data["memory_percent"] = mem.percent

                # Disk
                disk = psutil.disk_usage('/')
                data["disk_total_gb"] = round(disk.total / (1024 ** 3), 2)
                data["disk_used_gb"] = round(disk.used / (1024 ** 3), 2)
                data["disk_percent"] = disk.percent

                # Network
                net = psutil.net_io_counters()
                data["net_bytes_sent"] = net.bytes_sent
                data["net_bytes_recv"] = net.bytes_recv

                # Process
                data["process_count"] = len(psutil.pids())

                # Timestamp
                data["timestamp"] = datetime.utcnow().isoformat()

                # -------- PRINT (human readable) --------
                for key, value in data.items():
                    print(f"{key}: {value}")
                print("-" * 40)

                # -------- SAVE (machine readable) --------
                logfile.write(json.dumps(data) + "\n")
                logfile.flush()

                time.sleep(5)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user. Data saved to metrics.log")

if __name__ == "__main__":
    collect_metrics()
