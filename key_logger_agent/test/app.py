from flask import Flask, jsonify, request
from manager import Manager
import config

app = Flask(__name__)
manager = Manager()


@app.route('/start', methods=['GET'])
def start():
    manager.start_logging()
    return jsonify({"status": "started"}), 200


@app.route('/stop', methods=['GET'])
def stop():
    manager.stop_logging()
    return jsonify({"status": "stopped"}), 200


@app.route('/get_logs', methods=['GET'])
def get_logs():
    logs = manager.get_logs()
    return jsonify(logs), 200


@app.route('/time_to_run/<int:minutes>', methods=['GET'])
def time_to_run(minutes):
    if minutes > 0:
        manager.run_time(minutes)
        return jsonify({"status": f"running for {minutes} minutes"}), 200
    return jsonify({"error": "invalid runtime"}), 400


@app.route('/set_routing/<routing_type>', methods=['GET'])
def set_routing(routing_type):
    """משנה את הניתוב לפי הבקשה מהשרת."""
    if routing_type in ['file', 'server']:
        manager.set_routing(routing_type)
        return jsonify({"status": f"Routing set to {routing_type}"}), 200
    return jsonify({"error": "Invalid routing type. Use 'file' or 'server'."}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
