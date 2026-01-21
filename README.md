# EC2 Monitoring System

A production-style, agent-based monitoring system for AWS EC2 instances that collects and visualizes real-time system metrics without relying on SSH access.

## Overview

This project implements a scalable monitoring architecture where lightweight agents run on individual EC2 instances and periodically push system metrics to a centralized monitoring server over HTTP. The server ingests, processes, and exposes metrics through REST APIs, which are consumed by a real-time web dashboard.

## Architecture

Agent EC2 Instances ---> Monitoring Server ---> Web Dashboard
(HTTP POST) (Flask APIs) (React UI)


<img width="1897" height="833" alt="534526214-6052e8f5-b9b4-462b-bd46-cf35e3d69997" src="https://github.com/user-attachments/assets/ac24d5a1-fc16-4fb1-bfcb-6afd25dbf933" />
<img width="1883" height="903" alt="534526224-6f0423ac-f28b-45fa-b5be-af6e812296b5" src="https://github.com/user-attachments/assets/6e7dce83-5898-434c-aa2b-9ede0c2435a6" />


- **Agents** collect metrics locally and push data to the server.
- **Monitoring Server** ingests metrics, determines service health, and serves APIs.
- **Dashboard** visualizes metrics and service status in real time.

## Key Features

- Agent-based metric collection (no SSH dependency)
- Real-time monitoring of CPU, memory, disk, and network usage
- Heartbeat-based service health detection (UP / DOWN)
- Persistent service tracking for offline instances
- RESTful APIs for metrics ingestion and retrieval
- systemd-managed services with auto-start and crash recovery
- React-based dashboard for visualization

## Tech Stack

- **Backend:** Python, Flask
- **Agent Metrics:** psutil
- **Frontend:** React (Vite)
- **Infrastructure:** AWS EC2, Linux (Ubuntu)
- **Service Management:** systemd
- **Communication:** HTTP/REST (JSON)
- **Version Control:** Git, GitHub

## API Endpoints

- `POST /ingest` – Ingest metrics from agents  
- `GET /services` – List monitored services  
- `GET /metrics/<service>` – Retrieve metrics for a service  
- `GET /status/<service>` – Get UP/DOWN status  
- `GET /health` – Server health check  

## Running the System

### Agent
- Runs as a systemd service on each EC2 instance
- Collects metrics at fixed intervals
- Pushes data to the monitoring server via HTTP

### Monitoring Server
- Runs as a systemd service on a central EC2 instance
- Receives metrics and exposes APIs
- Serves the frontend dashboard

## Testing

- CPU load: `yes > /dev/null`
- Memory load: `stress --vm 1 --vm-bytes 200M --timeout 120`
- Network traffic: `curl http://speedtest.tele2.net/100MB.zip -o /dev/null`

## Status

Active development – January 2026 to Present

## Author

Vraj Patel  
GitHub: https://github.com/vraj3724    
LinkedIn: https://www.linkedin.com/in/vrajpatel-sde

Krish Mungalpara
Github: https://github.com/krishop90   
LinkedIn: https://www.linkedin.com/in/krish-mungalpara-8a718a260/



