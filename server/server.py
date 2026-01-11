from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return {"status": "up"}

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json(force=True, silent=True)

    print("\n==============================")
    print("METRICS RECEIVED AT:", datetime.utcnow().isoformat())
    print(json.dumps(data, indent=2))
    print("==============================\n")

    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
