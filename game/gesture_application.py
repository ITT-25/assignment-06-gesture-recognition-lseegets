import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyglet
from pyglet import window, shapes, text
import time
from recognizer import recognize
import threading
from mediapipe_sample import HandDetection
from game_manager import GameManager

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
LINE_THICKNESS = 3

restart_scheduled = False
detector = HandDetection()
win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
dots = []
points = []
input_gesture = None
game = GameManager()

com_button = pyglet.shapes.Rectangle(x=(WINDOW_WIDTH // 2) - 80 // 2, y=((WINDOW_HEIGHT // 2 + 40) - 30) - 40 // 2, width=100, height=50, color=(100, 100, 100))
multi_button = pyglet.shapes.Rectangle(x=(WINDOW_WIDTH // 2) - 90 // 2, y=((WINDOW_HEIGHT // 2 + 40) - 5 * 30) - 40 // 2, width=110, height=50, color=(100, 100, 100))
restart_button = pyglet.shapes.Rectangle(x=(WINDOW_WIDTH // 2) - 120 // 2, y=((WINDOW_HEIGHT // 2 + 40) - 4 * 30) - 40 // 2, width=120, height=60, color=(100, 100, 100))

def restart_upon_tie(dt):
    global restart_scheduled
    game.start(game.mode)
    restart_scheduled = False

# Check if a gesture is valid: It has to contain at least two points and the points cannot all be the same
def is_valid_gesture(points):
    if len(points) < 2:
        return False
    first = points[0]
    for p in points[1:]:
        if p != first:
            return True
    return False


def update(dt):
    global restart_scheduled
    if game.tie and not restart_scheduled:
        pyglet.clock.schedule_once(restart_upon_tie, 1.0)
        restart_scheduled = True

pyglet.clock.schedule_interval(update, 0.1)

def start_game_com(dt):
    game.start("com")

def start_game_multi(dt):
    game.start("multi")

@win.event
def on_mouse_motion(x, y, dx, dy):
    if com_button.x <= x <= com_button.x + com_button.width and com_button.y <= y <= com_button.y + com_button.height:
        com_button.color = (0, 255, 0)
    else:
        com_button.color = (100, 100, 100)
    if multi_button.x <= x <= multi_button.x + multi_button.width and multi_button.y <= y <= multi_button.y + multi_button.height:
        multi_button.color = (0, 255, 0)
    else:
        multi_button.color = (100, 100, 100)
    if restart_button.x <= x <= restart_button.x + restart_button.width and restart_button.y <= y <= restart_button.y + restart_button.height:
        restart_button.color = (0, 255, 0)
    else:
        restart_button.color = (100, 100, 100)

@win.event
def on_key_press(symbol, modifiers):
    if symbol == window.key.SPACE:
        if not game.has_started:
            start_game_com()
        else:
            game.restart()
    elif symbol == window.key.M:
        start_game_multi()


@win.event
def on_mouse_press(x, y, button, modifiers):
    if com_button.x <= x <= com_button.x + com_button.width and com_button.y <= y <= com_button.y + com_button.height:
        pyglet.clock.schedule_once(start_game_com, 1)
    elif multi_button.x <= x <= multi_button.x + multi_button.width and multi_button.y <= y <= multi_button.y + multi_button.height:
        pyglet.clock.schedule_once(start_game_multi, 1)
    elif restart_button.x <= x <= restart_button.x + restart_button.width and restart_button.y <= y <= restart_button.y + restart_button.height:
        game.restart()

@win.event
def on_mouse_release(x, y, button, modifiers):
    if is_valid_gesture(points) and len(game.game_gestures) < 2:
        input_gesture = recognize([(x, y) for x, y, _ in points])
        game.game_gestures.append(input_gesture)
        dots.clear()
        points.clear()
        if len(game.game_gestures) == 2:
            game.determine_winner()
            if game.winner == None:
                game.tie = True
            else:
                game.has_finished = True
    else:
        game.input_gesture = None

@win.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if game.has_started:
        if buttons & window.mouse.LEFT:
            dots.append(shapes.Rectangle(x, y, LINE_THICKNESS, LINE_THICKNESS, (255, 255, 255)))
            points.append((int(x), WINDOW_HEIGHT - int(y), int(time.time() * 1000)))
        
@win.event
def on_draw():
    win.clear()
    y = WINDOW_HEIGHT // 2 + 40
    if not game.has_started:
        com_button.draw()
        multi_button.draw()
        text.Label("ROCK PAPER SCISSORS", font_size=28, x=WINDOW_WIDTH // 2, y=y + 40, anchor_x='center').draw()
        text.Label("COM", font_size=24, x=WINDOW_WIDTH // 2, y=y - 30, anchor_x='center').draw()
        text.Label("1 vs. 1", font_size=24, x=WINDOW_WIDTH // 2, y=y - 5 * 30, anchor_x='center').draw()
    elif game.has_started and not game.has_finished:
        if game.tie:
            dots.clear()
            points.clear()
            text.Label("It's a tie! Restarting...", font_size=24, x=WINDOW_WIDTH // 2, y=y + 40, anchor_x='center').draw()
        for i in range(0, len(dots)):
            if i == 0:
                dots[i].draw()
            else:
                dots[i].draw()
                if dots[i].x - dots[i-1].x != 0 or dots[i].y - dots[i-1].y != 0:
                    shapes.Line(dots[i].x, dots[i].y, dots[i-1].x, dots[i-1].y, LINE_THICKNESS).draw()
        game.draw_game_info(WINDOW_HEIGHT)
    elif game.has_finished:
        dots.clear()
        points.clear()
        game.draw_finish_screen(WINDOW_WIDTH, WINDOW_HEIGHT, y)
        restart_button.draw()
        text.Label("Restart", font_size=24, x=WINDOW_WIDTH // 2, y=y - 4 * 30, anchor_x='center').draw()

threading.Thread(target=detector.run, daemon=True).start()
pyglet.app.run()