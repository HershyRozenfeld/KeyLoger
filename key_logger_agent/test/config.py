import os

# הגדרות הצפנה
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "The_best_day_of_my_life_is_today.").encode('utf-8')

# הגדרות קבצים
ENCRYPTED_LOG_FILE = "encrypted_logs.json"

# הגדרות שרת
SERVER_URL = os.getenv("SERVER_URL", "https://example.com/receive_logs")
