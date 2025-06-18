import pyglet
from pyglet import window, shapes, text
import xml.etree.ElementTree as ET
import time
from datetime import datetime
from recognizer import recognize
import threading
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mediapipe_sample import HandDetection

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
LINE_THICKNESS = 3

detector = HandDetection()
win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
dots = []
points = []
input_gesture = None
has_started = False
is_recording = False


# Check if a gesture is valid: It has to contain at least two points and the points cannot all be the same
def is_valid_gesture(points):
    if len(points) < 2:
        return False
    
    first = points[0]
    for p in points[1:]:
        if p != first:
            return True
        
    return False


def save_to_xml(points, gesture_name, subject="1", speed="slow", app_name="Gestures", app_ver="1.0.0.0"):
    if not points:
        return
    if gesture_name == "delete":
        gesture_name = "delete_mark"

    base_dir =  os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    dir_path = os.path.join(base_dir, f"datasets/hand_input/{speed}/s{str(subject).zfill(2)}")
    os.makedirs(dir_path, exist_ok=True)
    files = os.listdir(dir_path)
    gesture_files = [file for file in files if file.startswith(gesture_name) and file.endswith(".xml")]

    # Check which indices are already in use and fill in the numbers accordingly
    used_numbers = []
    for f in gesture_files:
        number = f[len(gesture_name):-4]
        if number.isdigit():
            used_numbers.append(int(number))
    next_number = 1
    while next_number in used_numbers:
        next_number += 1

    number = next_number
    name = gesture_name + str(number).zfill(2)
    dt = datetime.now()
    start_time = points[0][2]
    end_time = points[-1][2]
    millseconds = end_time - start_time
    gesture = ET.Element("Gesture", {
        "Name": name,
        "Subject": subject,
        "Speed": speed,
        "Number": str(number),
        "NumPts": str(len(points)),
        "Millseconds": str(millseconds),
        "AppName": app_name,
        "AppVer": app_ver,
        "Date": dt.strftime("%A, %B, %d, %Y"),
        "TimeOfDay": dt.strftime("%I:%M:%S %p")
    })
    for x, y, t in points:
        ET.SubElement(gesture, "Point", {
            "X": str(x),
            "Y": str(y),
            "T": str(t)
        })
    tree = ET.ElementTree(gesture)
    ET.indent(tree, space='  ', level=0)
    xml_path = os.path.join(dir_path, name + ".xml")
    with open(xml_path, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
        tree.write(f)


@win.event
def on_key_press(symbol, modifiers):
    global is_recording, has_started
    if symbol == window.key.SPACE:
        is_recording = False
        has_started = True
    elif symbol == window.key.R:
        is_recording = True
        has_started = True
    elif symbol == window.key.BACKSPACE:
        is_recording = False
        has_started = False

@win.event
def on_mouse_press(x, y, button, modifiers):
    dots.clear()
    points.clear()

@win.event
def on_mouse_release(x, y, button, modifiers):
    global input_gesture, is_recording
    if is_valid_gesture(points):
        input_gesture = recognize([(x, y) for x, y, _ in points])
        if is_recording:
            save_to_xml(points, input_gesture)
    else:
        input_gesture = None

@win.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if has_started:
        if buttons & window.mouse.LEFT:
            dots.append(shapes.Rectangle(x, y, LINE_THICKNESS, LINE_THICKNESS, (255, 255, 255)))
            points.append((int(x), WINDOW_HEIGHT - int(y), int(time.time() * 1000)))
        

@win.event
def on_draw():
    win.clear()
    if not has_started:
        y = WINDOW_HEIGHT // 2 + 40
        text.Label("GESTURE RECOGNIZER", font_size=24, x=WINDOW_WIDTH // 2, y=y + 40, anchor_x='center').draw()
        text.Label("Press 'R' to record gestures.", font_size=16, x=WINDOW_WIDTH // 2, y=y - 30, anchor_x='center').draw()
        text.Label("Press SPACE to test the recognizer.", font_size=16, x=WINDOW_WIDTH // 2, y=y - 2 * 30, anchor_x='center').draw()
        text.Label("At any point, press BACKSPACE to get back to the main menu.", font_size=12, x=WINDOW_WIDTH // 2, y=y - 3 * 30, anchor_x='center').draw()
    elif has_started:
        for i in range(0, len(dots)):
            if i == 0:
                dots[i].draw()
            else:
                dots[i].draw()
                if dots[i].x - dots[i-1].x != 0 or dots[i].y - dots[i-1].y != 0:
                    shapes.Line(dots[i].x, dots[i].y, dots[i-1].x, dots[i-1].y, LINE_THICKNESS).draw()
        text.Label(f'Input: {input_gesture}', font_size=20, x=150, y=WINDOW_HEIGHT-30, anchor_x='center').draw()
        if is_recording:
            text.Label('REC', font_size=20, x=WINDOW_HEIGHT - 30, y=WINDOW_HEIGHT-30, anchor_x='center', color=(255, 0, 0)).draw()

threading.Thread(target=detector.run, daemon=True).start()
pyglet.app.run()