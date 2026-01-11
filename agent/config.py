import os

INGEST_URL = os.getenv("INGEST_URL", "http://127.0.0.1:8000/ingest")
AGENT_ID = os.getenv("AGENT_ID", "local-test")
AGENT_TOKEN = os.getenv("AGENT_TOKEN", "test-token")

INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS", "5"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "5"))
