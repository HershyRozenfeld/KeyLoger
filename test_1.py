from datetime import datetime
import sys
from pynput import keyboard

press_char = []


def on_press(key):
    try:
        formatted_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        press_char.append({formatted_date: key.char})
    except AttributeError:
        press_char.append(key)


def on_release(key):
    if key == keyboard.Key.esc:
        return False


def show_pressed_key():
    print(press_char[0])


# מאזין להקשות ושחרור מקשים
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
print(press_char)
command = sys.argv[1]
if command.upper() == "SHOW":
    print("Command received: SHOW")
else:
    print(f"Unknown command: {command}")
show = input()
if show.upper() == 'SHOW':
    show_pressed_key()
