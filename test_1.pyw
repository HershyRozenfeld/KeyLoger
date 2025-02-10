from datetime import datetime
import threading
import sys
from pynput import keyboard
from collections import defaultdict

press_char = defaultdict(list)
running = True  # To allow clean exit from the program


def on_press(key):
    """ מאזין להקשות מקשים ושומר אותן לפי דקות """
    try:
        formatted_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        if hasattr(key, 'char') and key.char is not None:
            press_char[formatted_date].append(key.char)
        else:
            press_char[formatted_date].append(key.name if hasattr(key, "name") else str(key))
    except Exception as e:
        print(f"error: {e}")


def show_pressed_key():
    """ מציג את כל הקשות המקשים שנשמרו, מקובצות לפי דקות """
    if not press_char:
        print("❌ No data to display.")
        return
    print("\n📋 **Recorded Key Presses:**")
    for minute, keys in sorted(press_char.items()):
        print(f"\n🕒 {minute}:\n {', '.join(keys)}")
    print()


def command_listener():
    """ מאזין פקודות משתמש בצורה רציפה בזמן שההקשה על המקשים נמשכת """
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
