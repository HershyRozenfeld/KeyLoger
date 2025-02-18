import json
import logging
from datetime import datetime
from config import ENCRYPTED_LOG_FILE

logger = logging.getLogger(__name__)


class JSONFileHandler:
    @staticmethod
    def read_logs() -> dict:
        """קורא את הקובץ ומחזיר את הנתונים."""
        try:
            with open(ENCRYPTED_LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Log file not found or corrupted: {e}")
            return {"logs": []}

    @staticmethod
    def write_log(encrypted_content: str):
        """כותב לוג חדש לקובץ."""
        try:
            logs = JSONFileHandler.read_logs()
            log_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "encrypted_content": encrypted_content
            }
            logs["logs"].append(log_entry)
            with open(ENCRYPTED_LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to write logs: {e}")
            raise
