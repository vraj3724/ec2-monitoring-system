const BASE_URL = "backend api";

export async function getServices() {
  return fetch(`${BASE_URL}/services`).then(r => r.json());
}

/* ---------- METRICS ---------- */
export async function getMetrics(service) {
  return fetch(`${BASE_URL}/metrics/${service}`).then(r => r.json());
}

/* ---------- STATUS ---------- */
export async function getStatus(service) {
  return fetch(`${BASE_URL}/status/${service}`).then(r => r.json());
}

/* ---------- ALERTS ---------- */
export async function getAlerts(service) {
  return fetch(`${BASE_URL}/alerts/${service}`).then(r => r.json());
}

export async function getActiveAlerts(service) {
  return fetch(`${BASE_URL}/alerts/active/${service}`).then(r => r.json());
}