from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread
import time

app = Flask(__name__)
CORS(app, origins=["http://localhost:8888"])

progress = {"value": 0, "running": False}

def run_progress():
    progress["running"] = True
    progress["value"] = 0
    while progress["value"] < 95:
        progress["value"] += 1
        time.sleep(0.01)
    progress["running"] = False

@app.route("/start", methods=["POST"])
def start_progress():
    if not progress["running"]:
        Thread(target=run_progress, daemon=True).start()
    return jsonify({"message": "started"})

@app.route("/progress", methods=["GET"])
def get_progress():
    return jsonify({"value": progress["value"]})

if __name__ == "__main__":
    app.run(debug=True)