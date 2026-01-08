import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

LOG_FILE = "metrics.log"
REFRESH_INTERVAL = 5000  # milliseconds

timestamps = []
cpu = []
memory = []
disk = []

fig, ax = plt.subplots()
line_cpu, = ax.plot([], [], label="CPU %")
line_mem, = ax.plot([], [], label="Memory %")
line_disk, = ax.plot([], [], label="Disk %")

ax.set_xlabel("Time")
ax.set_ylabel("Usage (%)")
ax.set_title("Live System Metrics")
ax.legend()
plt.xticks(rotation=45)


def read_latest_data():
    timestamps.clear()
    cpu.clear()
    memory.clear()
    disk.clear()

    with open(LOG_FILE, "r") as f:
        for line in f:
            data = json.loads(line)
            timestamps.append(
                datetime.fromisoformat(data["timestamp"])
            )
            cpu.append(data["cpu_percent"])
            memory.append(data["memory_percent"])
            disk.append(data["disk_percent"])


def update(frame):
    read_latest_data()

    line_cpu.set_data(timestamps, cpu)
    line_mem.set_data(timestamps, memory)
    line_disk.set_data(timestamps, disk)

    ax.relim()
    ax.autoscale_view()

    return line_cpu, line_mem, line_disk


ani = animation.FuncAnimation(
    fig,
    update,
    interval=REFRESH_INTERVAL
)

plt.tight_layout()
plt.show()
