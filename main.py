import cv2
from pynput import keyboard, mouse
import datetime
import pyautogui
import numpy as np
recording = 0
log_var = ""
output_file = 'screen_record.mp4'
fps = 30.0
def on_release(key):
    global log_var
    global recording
    if recording == 1:
        if hasattr(key, 'char'):
            log_var += "r " + str(key.char) + "\n"
        else:
            log_var += "r " + str(key) + "\n"
def on_press(key):
    global log_var
    global recording
    try:
        if key.char == 'q':
            recording = 2
            return False
        elif key.char == 'r':
            recording = 1
    except AttributeError:
        pass
    if recording == 1:
        if hasattr(key, 'char'):
            log_var += str(key.char) + "\n"
        else:
            log_var += str(key) + "\n"
def record_screen():
    global log_var
    global recording
    frame_number = 0
    screen_width, screen_height = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (screen_width, screen_height))
    while recording < 2:
        if recording == 1:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)
            frame_number += 1
            log_var += str(frame_number) + "\n"
    out.release()
    cv2.destroyAllWindows()
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()
record_screen()
keyboard_listener.stop()
text_file = open("sample.txt", "w")
text_file.write(log_var)
text_file.close()
print("Recording finished. Video file saved as", output_file)
